# app.py

import argparse
from app.document_ingestor import ingest_docs
from app.retriever import retrieve
from app.generator import generate
import time

def main():
    parser = argparse.ArgumentParser(description="Document-based Chatbot")
    parser.add_argument("--docs_path", type=str, required=True, help="Path to folder with .pdf/.txt/.md documents")

    args = parser.parse_args()
    print(f"\n📄 Ingesting documents from: {args.docs_path}...\n")
    ingest_docs(args.docs_path)

    print("✅ Documents processed. You can now ask questions.\n")
    
    while True:
        query = input("❓ Your Question (type 'exit' to quit): ").strip()
        if query.lower() in ['exit', 'quit']:
            break

        start = time.time()
        top_chunks = retrieve(query)
        answer = generate(query, top_chunks)
        end = time.time()

        print(f"\n💬 Answer:\n{answer}")
        print(f"⏱️ Latency: {round(end - start, 2)} seconds\n")

if __name__ == "__main__":
    main()
