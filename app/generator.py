import os
import cohere
from dotenv import load_dotenv

load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(COHERE_API_KEY)

def generate(question: str, documents: list) -> str:
    if not documents:
        return "I don’t know."

    context = ""
    for doc in documents:
        source = doc.metadata.get("source", "Unknown")
        chunk = doc.metadata.get("chunk", "N/A")
        context += f"[{source}, chunk {chunk}]:\n{doc.page_content}\n\n"

    prompt = f"""Answer the question based only on the documents below. Cite sources as [source, chunk #].

Documents:
{context}

Question: {question}
Answer:"""

    try:
        response = co.generate(
            model="command-r-plus",
            prompt=prompt,
            max_tokens=300,
            temperature=0.3
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print(f"❌ Error during generation: {e}")
        return "Error generating answer."
