# app/retriever.py

import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# Lazy loading
docs, sources, index = None, None, None

def load_index():
    global docs, sources, index
    if docs is None or sources is None or index is None:
        with open("app/vector_data.pkl", "rb") as f:
            docs, sources, _ = pickle.load(f)
        index = faiss.read_index("app/faiss_index.index")

def retrieve(query, k=3):
    load_index()
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), k)
    return [(docs[i], sources[i]) for i in I[0]]
