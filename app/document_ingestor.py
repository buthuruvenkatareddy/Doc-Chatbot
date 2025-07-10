import os
import pickle
from typing import List
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
from dotenv import load_dotenv

load_dotenv()

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
VECTOR_STORE_PATH = "app/vector_data.pkl"
model = SentenceTransformer(EMBEDDING_MODEL)

class Document:
    def __init__(self, page_content: str, metadata: dict):
        self.page_content = page_content
        self.metadata = metadata

def read_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_pdf(file_path):
    text = ""
    reader = PdfReader(file_path)
    for i, page in enumerate(reader.pages):
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=500):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def ingest_docs(folder_path: str) -> List[Document]:
    docs = []
    embeddings = []
    files = [f for f in os.listdir(folder_path) if f.endswith((".txt", ".pdf", ".md"))]

    for file_name in files:
        path = os.path.join(folder_path, file_name)

        try:
            if file_name.endswith(".txt") or file_name.endswith(".md"):
                text = read_txt(path)
            elif file_name.endswith(".pdf"):
                text = read_pdf(path)
            else:
                continue

            chunks = chunk_text(text)

            for i, chunk in enumerate(chunks):
                doc = Document(
                    page_content=chunk,
                    metadata={"source": file_name, "chunk": i + 1}
                )
                docs.append(doc)
                embedding = model.encode(chunk)
                embeddings.append((embedding, doc))

        except Exception as e:
            print(f"❌ Failed to read {file_name}: {e}")

    with open(VECTOR_STORE_PATH, "wb") as f:
        pickle.dump(embeddings, f)

    print(f"Ingested {len(docs)} chunks from {len(files)} files.")
    return docs  # ✅ return so Streamlit and Jupyter can use it
