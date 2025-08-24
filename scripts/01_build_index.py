# scripts/01_build_index.py

import os
import sys
import pandas as pd
import argparse

# This allows the script to find the 'src' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.pipeline.semantic_pipeline import SemanticPipeline

def create_text_column(row: pd.Series) -> str:
    """Creates a descriptive sentence from a row of laptop data."""
    ssd = int(row.get("SSD", 0))
    hdd = int(row.get("HDD", 0))
    storage_parts = []
    if ssd > 0: storage_parts.append(f"{ssd} GB SSD")
    if hdd > 0: storage_parts.append(f"{hdd} GB HDD")
    storage = " and ".join(storage_parts) if storage_parts else "no dedicated storage"
    
    return (
        f"A {row.get('Company', '')} {row.get('TypeName', 'laptop')} with {row.get('Ram', 8)}GB RAM, "
        f"an {row.get('Cpu_brand', 'Intel')} processor, and {storage}. "
        f"It has a {row.get('Gpu_brand', 'Intel')} GPU and runs {row.get('Os', 'Windows')}."
    )

def main():
    parser = argparse.ArgumentParser(description="Build the semantic search index.")
    parser.add_argument("--force", action="store_true", help="Force a rebuild of the index.")
    args = parser.parse_args()

    # --- Data Preparation ---
    df = pd.read_csv("data/laptop_data_cleaned.csv")
    df.fillna(0, inplace=True) # Fill missing values
    df.insert(0, 'id', range(len(df))) # Add a unique ID column
    df['id'] = df['id'].astype(str)
    
    # Create the text column for embedding
    df['text'] = df.apply(create_text_column, axis=1)

    # --- Pipeline ---
    pipeline = SemanticPipeline(df=df, id_col="id", text_col="text")
    pipeline.build_index(force=args.force)

if __name__ == "__main__":
    main()