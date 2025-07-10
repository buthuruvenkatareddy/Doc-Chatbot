# app/utils.py

import re

def chunk_text(text, chunk_size=500, overlap=100):
    """
    Splits text into overlapping chunks of given size.
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i + chunk_size]
        chunks.append(" ".join(chunk))

    return chunks
