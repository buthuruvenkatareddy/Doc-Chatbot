# web_ui.py

import streamlit as st
import time
import os
from app.document_ingestor import ingest_docs
from app.retriever import retrieve
from app.generator import generate

st.set_page_config(page_title="📄 Document Chatbot", layout="wide")
st.title("📄 Document-Based Chatbot using Cohere")

# Sidebar: Upload files
with st.sidebar:
    st.header("📁 Upload Documents")
    uploaded_files = st.file_uploader("Upload your .txt, .pdf, .md files", accept_multiple_files=True)

    if uploaded_files and st.button("Ingest Uploaded Files"):
        from io import BytesIO
        temp_folder = "uploaded_docs"
        os.makedirs(temp_folder, exist_ok=True)

        for file in uploaded_files:
            file_path = os.path.join(temp_folder, file.name)
            with open(file_path, "wb") as f:
                f.write(file.read())

        ingest_docs(temp_folder)
        st.success("✅ Documents ingested successfully!")

# Main: Ask questions
st.subheader("💬 Ask a Question from the Ingested Documents")
query = st.text_input("Enter your question")

if st.button("Get Answer") and query:
    with st.spinner("🔍 Retrieving and generating answer..."):
        start_time = time.time()
        top_chunks = retrieve(query)
        answer = generate(query, top_chunks)
        latency = round(time.time() - start_time, 2)

    st.markdown("### 💡 Answer")
    st.success(answer)
    st.markdown(f"⏱️ **Latency**: {latency} seconds")

    # Show retrieved sources
    with st.expander("📚 View Retrieved Sources"):
        for i, (chunk, source) in enumerate(top_chunks):
            st.markdown(f"**Source {i+1}** - `{source}`")
            st.write(chunk)
            st.markdown("---")
