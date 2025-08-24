import streamlit as st
import requests

# --- Page Configuration ---
st.set_page_config(
    page_title=" Semantic Product Discovery Engine",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Sidebar ---
with st.sidebar:
    st.header("About")
    # --- Start of Updated Description ---
    st.markdown(
        """
        This project delivers a state-of-the-art search solution engineered to bridge the critical gap between conversational human language and structured product data. 
        
        This **Hybrid Semantic Search Engine** transcends the limitations of traditional keyword search to create an intelligent and intuitive product discovery experience.
        """
    )
    # --- End of Updated Description ---
    st.divider()
    st.write("""Project by \\
                Yashwanth Sai Kasarabada""")
    st.markdown("[Connect on LinkedIn](https://www.linkedin.com/in/yashwanth-kasarabada-ba4265258/)") # Remember to add your profile link


# --- Main Page ---

# --- Header ---
st.title(" 🔍 Hybrid Semantic Search: A Product Discovery Engine for E-Commerce ")
st.markdown(" *Using a Laptops E-commerce Dataset For Testing* ")
st.markdown(
    """
    <style>
    .stTextInput > div > div > input {
        font-size: 1.1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
query = st.text_input(
    "Search for laptops using natural language...",
    placeholder="e.g., a lightweight ultrabook with 16gb ram for travel",
    label_visibility="collapsed"
)

# --- Example Queries ---
st.markdown("##### Try an example:")
col1, col2, col3 = st.columns([1,1,1])
with col1:
    if st.button("Gaming laptop with Nvidia GPU"):
        query = "Gaming laptop with Nvidia GPU"
        st.rerun()
with col2:
    if st.button("Dell ultrabook with an i7 processor"):
        query = "Dell ultrabook with an i7 processor"
        st.rerun()
with col3:
    if st.button("A cheap notebook for a student"):
        query = "A cheap notebook for a student"
        st.rerun()

st.divider()

# --- Search Execution and Results ---
if query:
    API_URL = "http://127.0.0.1:8000/search"
    payload = {"query": query, "top_k": top_k}
    
    try:
        with st.spinner("🧠 Performing semantic search..."):
            response = requests.post(API_URL, json=payload)
            response.raise_for_status()
            results = response.json()
        
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

    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: Could not connect to the API. Please ensure the backend is running. Details: {e}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")