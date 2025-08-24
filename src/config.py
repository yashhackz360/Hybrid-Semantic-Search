import os
from dotenv import load_dotenv

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")



# --- Model & Index Configuration ---
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
PINECONE_INDEX_NAME = "laptop-semantic-search-v2"
VECTOR_DIMENSION = 768
VECTOR_METRIC = "cosine"