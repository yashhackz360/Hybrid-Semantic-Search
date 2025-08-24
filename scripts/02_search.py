# scripts/02_search.py

import os
import sys
from typing import List, Dict

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.pipeline.semantic_pipeline import SemanticPipeline

def display_results(results: List[Dict]):
    if not results:
        print("\n❌ No relevant results found.")
        return

    print("\n✅ Top Search Results:")
    for i, res in enumerate(results, 1):
        print("-" * 20)
        print(f"Rank {i} | Rerank Score: {res['rerank_score']:.4f}")
        print(f"Text: {res['text']}")

def main():
    pipeline = SemanticPipeline(df=None) # Initialize in search mode
    print("✅ Search system ready. Type your query or ':q' to exit.")

    while True:
        try:
            query = input("\nQuery > ").strip()
            if query.lower() in [":q", "exit", "quit"]:
                break
            if not query:
                continue
            
            results = pipeline.search(query)
            display_results(results)

        except (KeyboardInterrupt, EOFError):
            break
    print("\nExiting search. Goodbye!")

if __name__ == "__main__":
    main()