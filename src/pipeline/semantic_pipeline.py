import os
import json
import pandas as pd
import hashlib
from typing import List, Dict

# --- Local Module Imports ---
from src.retrieval.embedder import Embedder
from src.retrieval.vector_index import VectorIndex
from src.retrieval.reranker import Reranker
from src.preprocessing.wordnet_controlled import expand_terms
from src.preprocessing.query_parser import parse_query_for_specs
from src.config import (
    PINECONE_API_KEY,
    PINECONE_ENV,
    EMBEDDING_MODEL,
    RERANKER_MODEL,
    PINECONE_INDEX_NAME,
    VECTOR_DIMENSION,
    VECTOR_METRIC,
)

class SemanticPipeline:
    def __init__(self, df: pd.DataFrame = None, id_col="id", text_col="text", index_dir="artifacts/index"):
        self.df = df
        self.id_col = id_col
        self.text_col = text_col
        self.index_dir = index_dir
        self.manifest_path = os.path.join(self.index_dir, "manifest.json")
        self.doc_store_path = os.path.join(self.index_dir, "doc_store.json")
        os.makedirs(self.index_dir, exist_ok=True)

        # --- Initialize models and services once for efficiency ---
        print("Initializing models and services...")
        self.embedder = Embedder(EMBEDDING_MODEL)
        self.reranker = Reranker(RERANKER_MODEL)
        self.vector_index = VectorIndex(
            index_name=PINECONE_INDEX_NAME,
            dimension=VECTOR_DIMENSION,
            metric=VECTOR_METRIC,
            api_key=PINECONE_API_KEY,
            environment=PINECONE_ENV
        )
        # Load doc store if it exists
        try:
            with open(self.doc_store_path, 'r') as f:
                self.doc_store = json.load(f)
        except FileNotFoundError:
            self.doc_store = None
        print("Initialization complete.")

    def _hash_df(self) -> str:
        return hashlib.md5(pd.util.hash_pandas_object(self.df).values).hexdigest()

    def _hash_config(self) -> str:
        config_str = f"{EMBEDDING_MODEL}-{RERANKER_MODEL}-{PINECONE_INDEX_NAME}-{VECTOR_DIMENSION}-{VECTOR_METRIC}"
        return hashlib.md5(config_str.encode()).hexdigest()

    def _write_manifest(self):
        manifest = {
            "df_hash": self._hash_df(),
            "config_hash": self._hash_config()
        }
        with open(self.manifest_path, 'w') as f:
            json.dump(manifest, f)

    def _is_index_fresh(self) -> bool:
        if not os.path.exists(self.manifest_path):
            return False
        with open(self.manifest_path, 'r') as f:
            manifest = json.load(f)
        return manifest.get("df_hash") == self._hash_df() and manifest.get("config_hash") == self._hash_config()

    def build_index(self, force: bool = False):
        if self.df is None:
            raise ValueError("DataFrame must be provided to build the index.")
        if not force and self._is_index_fresh():
            print("✅ Index is already up-to-date. Skipping build.")
            return

        print("🚀 Building new index...")
        self.doc_store = self.df.set_index(self.id_col).to_dict('index')
        with open(self.doc_store_path, 'w') as f:
            json.dump(self.doc_store, f)
        
        texts = self.df[self.text_col].tolist()
        ids = self.df[self.id_col].tolist()
        embeddings = self.embedder.encode(texts, normalize=True)
        
        metadatas = [{"text": text} for text in texts]
        self.vector_index.upsert(ids=ids, vectors=embeddings, metadatas=metadatas)

        self._write_manifest()
        print("✅ Index build complete.")

    def _matches_specs(self, doc_id: str, specs: Dict) -> bool:
        doc = self.doc_store.get(doc_id)
        if not doc:
            return False
        for key, value in specs.items():
            if value and str(doc.get(key, 'N/A')).lower() != str(value).lower():
                return False
        return True

    def search(self, query: str, top_k_retrieve: int = 50, top_k_rerank: int = 5) -> List[Dict]:
        if not self.doc_store:
            raise RuntimeError("Document store not found. Please build the index first.")
        
        # --- Models are already initialized, so we use them directly ---
        expanded_query = expand_terms(query)
        query_specs = parse_query_for_specs(query)
        print(f"🔎 Expanded Query: {expanded_query}")
        print(f"⚙️  Parsed Specs: {query_specs}")

        query_embedding = self.embedder.encode([expanded_query], normalize=True)[0]
        retrieved_docs = self.vector_index.query(query_embedding, top_k=top_k_retrieve)
        print(f"Retrieved {len(retrieved_docs)} semantic candidates.")

        filtered_candidates = [doc for doc in retrieved_docs if self._matches_specs(doc['id'], query_specs)]
        print(f"Filtered down to {len(filtered_candidates)} candidates matching exact specs.")

        reranked_docs = self.reranker.rerank(query, filtered_candidates, top_k=top_k_rerank)
        print(f"Reranked to top {len(reranked_docs)} results.")
        
        return reranked_docs