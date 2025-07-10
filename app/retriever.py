import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

VECTOR_STORE_PATH = "app/vector_data.pkl"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
model = SentenceTransformer(EMBEDDING_MODEL)

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def retrieve(query: str, top_k: int = 3):
    with open(VECTOR_STORE_PATH, "rb") as f:
        embeddings = pickle.load(f)

    query_embedding = model.encode(query)

    scores = []
    for emb, doc in embeddings:
        sim = cosine_similarity(query_embedding, emb)
        scores.append((sim, doc))

    top_chunks = sorted(scores, key=lambda x: x[0], reverse=True)[:top_k]
    return [doc for _, doc in top_chunks]
