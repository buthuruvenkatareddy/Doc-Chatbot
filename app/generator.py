# app/generator.py

import os
import cohere
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

def generate(question, top_chunks):
    """
    Generate an answer using Cohere API based on top-k retrieved chunks.
    Adds inline citations in [filename] format.
    """

    if not top_chunks:
        return "I don’t know. No relevant information found."

    # Build the context with inline citations
    context = "\n\n".join([f"{chunk} [{source}]" for chunk, source in top_chunks])
    prompt = f"""You are a helpful assistant that only answers based on the following documents.
Use the context below to answer the question. If the answer is not in the context, say "I don’t know."
Include inline citations in the format [filename].

Context:
{context}

Question: {question}
Answer:"""

    try:
        # Use a valid model
        response = co.generate(
            model='command',  # ✅ Supported model for generate()
            prompt=prompt,
            max_tokens=300,
            temperature=0.3
        )
        return response.generations[0].text.strip()

    except cohere.CohereAPIError as e:
        return f"Error generating answer from Cohere: {e.message}"

    except Exception as e:
        return f"Unexpected error: {e}"
