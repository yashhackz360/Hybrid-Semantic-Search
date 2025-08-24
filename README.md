````markdown
# Hybrid Semantic Search: A Product Discovery Engine for E-Commerce

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![Pinecone](https://img.shields.io/badge/Pinecone-Vector_DB-orange?style=for-the-badge&logo=pinecone)
![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Models-yellow?style=for-the-badge&logo=huggingface)

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)  
2. [How It Works](#-how-it-works)  
3. [Key Features](#-key-features)  
4. [Tech Stack](#-tech-stack)  
5. [Setup and Installation](#-setup-and-installation)  
6. [Usage](#-usage)  
7. [Project Structure](#-project-structure)  
8. [Future Improvements](#-future-improvements)  
9. [Connect with Me](#-connect-with-me)  

---

## 🚀 Project Overview

This project tackles the limitations of traditional keyword-based search. While standard search finds exact matches, it often fails to understand user intent, context, and nuance. This **Hybrid Semantic Search Engine** provides a more intelligent and intuitive product discovery experience.

By combining the power of dense vector search (semantic understanding) with precise, attribute-based filtering (keyword matching), the system can interpret complex, conversational queries and return results that are not just similar, but **truly relevant**.

This engine's capabilities are demonstrated using a **sample dataset of laptop specifications**, showcasing its effectiveness in a real-world technical e-commerce scenario.

---

## 🔎 How It Works

The engine follows a multi-stage pipeline to process a user's query and retrieve the most relevant results:

1. **Query Processing** – Expand the raw query with relevant synonyms using WordNet; parse out structured specs (RAM, brand, CPU, storage, GPU, price caps, screen size, etc.).  
2. **Semantic Retrieval** – Encode the processed query with a sentence-transformer; query Pinecone to fetch the top-`k` semantically similar items.  
3. **Hard Filtering** – Apply exact spec filters extracted in step 1 (e.g., *ram_gb >= 16* or *brand in {dell, acer}*).  
4. **Reranking** – Pass the remaining candidates through a cross-encoder (bi-encoder for fast retrieval, cross-encoder for precision) to sort by fine-grained relevance.  

> ⚡️ Result: fast recall + precise ordering.

---

## ✨ Key Features

- **Hybrid Search Architecture**: Semantic vector search + rule/regex/keyword filters.  
- **Retrieve-and-Rerank Pipeline**: Balanced for latency and quality.  
- **Dynamic Query Expansion**: NLTK + WordNet to capture synonyms and related terms.  
- **Advanced Query Parsing**: Regex + lightweight heuristics for specs like RAM/CPU/SSD/GPU.  
- **Extensible**: Swap models, databases, or add business rules (boost brand, penalize OOS items).  

---

## ⚙️ Tech Stack

- **Backend**: Python 3.10+  
- **Vector DB**: Pinecone  
- **Embeddings**: Sentence-Transformers (e.g., `all-MiniLM-L6-v2`)  
- **Reranking**: Cross-encoders (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`)  
- **NLP**: NLTK (WordNet) for query expansion  
- **Data**: Pandas  
- **Env**: `python-dotenv`  

---

## 🔧 Setup and Installation

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd semantic-search
````

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # macOS/Linux
   # .venv\Scripts\activate   # Windows PowerShell
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK Data (first run only)**

   ```bash
   python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
   ```

5. **Configure Environment Variables**
   Create a `.env` file in the project root:

   ```env
   PINECONE_API_KEY=YOUR_API_KEY
   PINECONE_ENV=YOUR_ENV
   PINECONE_INDEX=semantic-laptops
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   CROSS_ENCODER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2
   TOP_K=50
   RERANK_K=10
   ```

> ℹ️ For local experiments without Pinecone, you can switch to a FAISS fallback (see `config.yaml`).

---

## ▶️ Usage

1. **Build the Vector Index**

   ```bash
   python scripts/01_build_index.py
   ```

2. **Run the Interactive Search**

   ```bash
   python scripts/02_search.py
   ```

---

## 📂 Project Structure

```
semantic-search/
├── scripts/
│   ├── 01_build_index.py        # Builds and populates the vector index
│   └── 02_search.py             # Runs the interactive search CLI
├── src/
│   ├── pipeline/
│   │   └── semantic_pipeline.py   # Main orchestrator for the search logic
│   ├── processing/
│   │   ├── query_parser.py        # Extracts structured specs from queries
│   │   └── wordnet_controlled.py  # Expands queries with synonyms
│   └── retrieval/
│       ├── embedder.py            # Handles text-to-vector encoding
│       ├── reranker.py            # Reranks retrieved results for accuracy
│       └── vector_index.py        # Manages interaction with Pinecone
├── artifacts/                       # Stores the index manifest and doc store
├── data/
│   └── laptop_data_cleaned.csv    # The sample dataset
├── .env                             # Stores API keys
└── README.md                        # Project documentation
```

---

## 💡 Future Improvements

* **Implement Filter Fallback**: If no exact matches are found after filtering, gracefully fall back to showing the best semantic results.
* **Centralize Configuration**: Move keyword maps and lists from the parser into a central `config.py` file to improve code structure.
* **Web Interface**: Build a user-friendly UI (using Streamlit or Flask) to make the search engine more accessible.
* **Fine-Tune Models**: Fine-tune the embedding and reranker models on a domain-specific dataset to further improve their understanding of technical jargon.

---

## 📬 Connect with Me

Feel free to reach out to me on LinkedIn to discuss this project, potential collaborations, or anything else!

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Yashwanth-blue?style=for-the-badge\&logo=linkedin)](https://www.linkedin.com/in/your-linkedin-profile/)

*(Remember to replace `https://www.linkedin.com/in/your-linkedin-profile/` with your actual LinkedIn profile link.)*

```
```
