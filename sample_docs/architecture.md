# System Architecture Overview

The chatbot system uses a retrieval-augmented generation pipeline. It begins by parsing and chunking documents, followed by generating vector embeddings using sentence-transformers. These embeddings are stored in a FAISS index for fast similarity search. When a user inputs a query, the top-k relevant chunks are retrieved, and a large language model (Cohere) generates an answer grounded in the retrieved context. The system includes inline citations and measures latency per request.
