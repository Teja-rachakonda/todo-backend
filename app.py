import streamlit as st
from utils import extract_elements
from rag import add_docs, rag_query

st.set_page_config(page_title="Multi-Modal RAG App", layout="wide")
st.title("📰 Multi-Modal RAG App - Text, Tables & Images with GROQ LLaMA3 🤖")

pdf_file = st.file_uploader("Upload a PDF file:", type=["pdf"])
user_query = st.text_input("Enter your query:")

if pdf_file:
    elements = extract_elements(pdf_file)
    add_docs(elements["texts"], elements["tables"], elements["images"])
    st.success("✅ Document processed and added to database.")

if user_query:
    answer = rag_query(user_query)
    st.write("### Answer:\n", answer)

st.markdown("""
---
**Powered by:**
- 🤗 Hugging Face (Blip, All-mpnet-base-v2)
- 💻 GROQ LLaMA3 (Free API!)
- 🐍 Streamlit
- ⚡️ Langchain Architecture
""")
