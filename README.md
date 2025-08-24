# Hybrid Semantic Search: A Product Discovery Engine for E-Commerce

A sophisticated, multi-layered search engine designed to understand natural language queries and provide highly relevant results for technical products like laptops.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-orange?style=for-the-badge&logo=pinecone)
![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Models-yellow?style=for-the-badge&logo=huggingface)
---

## 🚀 Project Overview

This project tackles the limitations of traditional keyword-based search in e-commerce. While standard search can find exact matches, it often fails to understand user intent, context, and nuance. This **Hybrid Semantic Search Engine** was built to provide a more intelligent and intuitive product discovery experience.

By combining the power of dense vector search (semantic understanding) with precise, attribute-based filtering (keyword matching), the system can interpret complex, conversational queries and return results that are not just similar, but truly relevant.



## ✨ Key Features

* **Hybrid Search Architecture**: Utilizes both semantic vector search for contextual relevance and keyword-based filtering for technical precision, ensuring the best of both worlds.
* **Retrieve-and-Rerank Pipeline**: Implements a two-stage process where an initial set of candidates is retrieved quickly, and a more powerful cross-encoder model then reranks them for maximum accuracy.
* **Dynamic Query Expansion**: Leverages the NLTK library and WordNet to intelligently expand user queries with relevant synonyms, broadening the search to better capture user intent.
* **Advanced Query Parsing**: Employs regular expressions to parse and extract specific technical attributes from natural language queries, such as RAM size, storage type, CPU model, and more.

---

## ⚙️ Tech Stack

* **Backend**: Python
* **Vector Database**: Pinecone
* **Embeddings & Reranking**: Sentence-Transformers (from Hugging Face)
* **NLP**: NLTK (for Query Expansion with WordNet)
* **Data Handling**: Pandas

---

## 🔧 Setup and Installation

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd semantic-search
    ```

2.  **Create and Activate a Virtual Environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**
    *(Note: You should create a `requirements.txt` file by running `pip freeze > requirements.txt`)*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a file named `.env` in the root directory and add your Pinecone credentials:
    ```env
    PINECONE_API_KEY="YOUR_API_KEY_HERE"
    PINECONE_ENV="YOUR_ENVIRONMENT_NAME_HERE"
    ```

---

## Usage

1.  **Build the Vector Index**
    First, run the build script to process the dataset and populate your Pinecone vector index.
    ```bash
    python scripts/01_build_index.py
    ```

2.  **Run the Interactive Search**
    Once the index is built, start the interactive search application.
    ```bash
    python scripts/02_search.py
    ```
    You can now type your queries into the terminal.

    **Example Queries:**
    * **Simple**: `a lenovo ultrabook`
    * **Hybrid**: `dell notebook with an i5 processor and 256gb ssd`
    * **Semantic**: `a high-performance machine for video editing`

---

## 📂 Project Structure

semantic-search/
├── scripts/
│   ├── 01_build_index.py      # Builds and populates the vector index
│   └── 02_search.py           # Runs the interactive search CLI
├── src/
│   ├── pipeline/
│   │   └── semantic_pipeline.py # Main orchestrator for the search logic
│   ├── processing/
│   │   ├── query_parser.py      # Extracts structured specs from queries
│   │   └── wordnet_controlled.py# Expands queries with synonyms
│   └── retrieval/
│       ├── embedder.py          # Handles text-to-vector encoding
│       ├── reranker.py          # Reranks retrieved results for accuracy
│       └── vector_index.py      # Manages interaction with Pinecone
├── artifacts/                     # Stores the index manifest and doc store
├── data/
│   └── laptop_data_cleaned.csv  # The dataset
├── .env                           # Stores API keys
└── README.md                      # Project documentation

---

## 💡 Future Improvements

* **Implement Filter Fallback**: If no exact matches are found after filtering, fall back to showing the best semantic results to the user.
* **Centralize Configuration**: Move keyword maps and lists from the parser into the central `config.py` file to improve code structure and maintainability.
