# app/streamlit_ui.py

import streamlit as st
import sys
import os

# This allows the app to find the 'src' module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.pipeline.semantic_pipeline import SemanticPipeline

# --- Page Configuration ---
st.set_page_config(
    page_title="Semantic Product Discovery",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Caching the Pipeline ---
# This is a critical step for performance. It loads the models only once.
@st.cache_resource
def load_pipeline():
    """Loads and caches the SemanticPipeline instance."""
    # df=None is used because we are only in search mode
    return SemanticPipeline(df=None)

# Load the pipeline from the cache
pipeline = load_pipeline()

# --- Sidebar ---
with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This project delivers a state-of-the-art search solution engineered to bridge the critical gap between conversational human language and structured product data.
        
        This **Hybrid Semantic Search Engine** transcends the limitations of traditional keyword search to create an intelligent and intuitive product discovery experience.
        """
    )
    st.divider()
    st.header("Controls")
    top_k = st.slider(
        "Number of results to display:",
        min_value=3,
        max_value=10,
        value=5,
        step=1
    )
    st.divider()
    st.write("Project by Yashwanth")
    st.markdown("[Connect on LinkedIn](https://www.linkedin.com/in/yashwanth-k-939883219/)")

# --- Main Page ---
st.title("💻 Semantic Product Discovery Engine")

query = st.text_input(
    "Search for laptops using natural language...",
    placeholder="e.g., a lightweight ultrabook with 16gb ram for travel",
)

# --- Search Execution and Results ---
if query:
    try:
        with st.spinner("🧠 Performing semantic search..."):
            # Call the pipeline directly instead of making an API request
            results = pipeline.search(query=query, top_k_rerank=top_k)
        
        if results:
            st.success(f"Found {len(results)} relevant results.")
            for i, res in enumerate(results, 1):
                with st.expander(f"**Rank {i}** | {res.get('text', 'N/A')[:70]}..."):
                    col_meta, col_desc = st.columns([1, 4])
                    with col_meta:
                        st.metric(label="Relevance Score", value=f"{res.get('rerank_score', 0.0):.4f}")
                    with col_desc:
                        st.markdown("#### Description")
                        st.write(res.get('text', 'No description available.'))
        else:
            st.warning("No relevant results found. Try rephrasing your query.")

    except Exception as e:
        st.error(f"An error occurred during the search: {e}")
