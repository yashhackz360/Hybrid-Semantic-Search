# src/retrieval/vector_index.py

from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict
import numpy as np

class VectorIndex:
    def __init__(self, index_name: str, dimension: int, metric: str, api_key: str, environment: str):
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        
        if index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=index_name,
                dimension=dimension,
                metric=metric,
                spec=ServerlessSpec(cloud="aws", region=environment)
            )
        self.index = self.pc.Index(index_name)

    def upsert(self, ids: List[str], vectors: np.ndarray, metadatas: List[Dict]):
        items = [
            {"id": str(i), "values": v.tolist(), "metadata": m}
            for i, v, m in zip(ids, vectors, metadatas)
        ]
        # Upsert in batches of 100 for efficiency
        for i in range(0, len(items), 100):
            self.index.upsert(items[i:i+100])

    def query(self, vector: np.ndarray, top_k: int = 10) -> List[Dict]:
        results = self.index.query(vector=vector.tolist(), top_k=top_k, include_metadata=True)
        matches = results.get("matches", [])
        return [
            {"id": m.id, "score": float(m.score), "text": m.metadata.get("text", "")}
            for m in matches
        ]