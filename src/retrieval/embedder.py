# src/retrieval/embedder.py

from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

class Embedder:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: List[str], normalize: bool = True) -> np.ndarray:
        return self.model.encode(
            texts, 
            normalize_embeddings=normalize,
            show_progress_bar=True,
            convert_to_numpy=True
        )