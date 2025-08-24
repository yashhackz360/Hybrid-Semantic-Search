# app/api.py

import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

# This allows the script to find the 'src' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.pipeline.semantic_pipeline import SemanticPipeline

# Initialize the FastAPI app
app = FastAPI(
    title="Semantic Search API",
    description="An API for the Hybrid Semantic Search Engine.",
    version="1.0.0"
)

# Load the pipeline at startup
# The DataFrame is not needed for search mode, so we pass df=None
pipeline = SemanticPipeline(df=None)

# Define the request body model
class SearchQuery(BaseModel):
    query: str
    top_k: int = 5

# Define the API endpoint
@app.post("/search", response_model=List[Dict])
def search(search_query: SearchQuery):
    """
    Performs a semantic search.
    
    - **query**: The user's search query string.
    - **top_k**: The number of top results to return.
    """
    results = pipeline.search(query=search_query.query, top_k_rerank=search_query.top_k)
    return results

@app.get("/", summary="Root endpoint for health check")
def read_root():
    return {"status": "API is running"}