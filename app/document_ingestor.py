# app/document_ingestor.py

import os
import faiss
import pickle
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from app.utils import chunk_text

model = SentenceTransformer("all-MiniLM-L6-v2")

def parse_file(filepath):
    if filepath.endswith(".pdf"):
        pdf = PdfReader(filepath)
        return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif filepath.endswith((".txt", ".md")):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    else:
        return ""

def ingest_docs(folder_path):
    docs, sources = [], []

    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        content = parse_file(filepath)

        if content.strip():
            chunks = chunk_text(content)
            docs.extend(chunks)
            sources.extend([f"{filename}"] * len(chunks))

    # Encode chunks into vectors
    embeddings = model.encode(docs, show_progress_bar=True)

    # Build FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save everything
    with open("app/vector_data.pkl", "wb") as f:
        pickle.dump((docs, sources, embeddings), f)
    faiss.write_index(index, "app/faiss_index.index")

    print(f"Ingested {len(docs)} chunks from {len(os.listdir(folder_path))} files.")
