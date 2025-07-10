

import streamlit as st
import os
import time
from app.document_ingestor import ingest_docs
from app.retriever import retrieve
from app.generator import generate
import tempfile

st.set_page_config(page_title="📄 Doc Chatbot", layout="centered")
st.title("📄 Document-Based Chatbot using Cohere")

# Upload documents
uploaded_files = st.file_uploader(
    "📁 Upload .txt, .md, or .pdf files", type=["txt", "pdf", "md"], accept_multiple_files=True
)

if uploaded_files:
    temp_dir = tempfile.mkdtemp()

    for uploaded_file in uploaded_files:
        with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
            f.write(uploaded_file.read())

    if st.button("📥 Ingest Uploaded Documents"):
        ingest_docs(temp_dir)
        st.success("✅ Documents ingested successfully!")

st.markdown("---")
st.subheader("💬 Ask a Question")

question = st.text_input("Type your question and press Enter")

if question:
    start_time = time.time()
    chunks = retrieve(question)
    answer = generate(question, chunks)
    end_time = time.time()

    if answer.strip():
        st.markdown(f"**💬 Answer:** {answer}")

        latency = round(end_time - start_time, 2)
        st.markdown(f"**⏱️ Time:** {latency} s")

        if chunks:
            sources = set(f"[{doc.metadata.get('source')}, chunk {doc.metadata.get('chunk')}]" for doc in chunks)
            st.markdown(f"**📚 Sources:** {', '.join(sources)}")
    else:
        st.warning("🤔 I don’t know.")
