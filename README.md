

###  `README.md`

```markdown
#  Document-Based Chatbot using Cohere

This is an intelligent chatbot that answers user questions **only** based on the content of uploaded documents. It uses Retrieval-Augmented Generation (RAG) with Cohere's language model and supports `.pdf`, `.txt`, and `.md` files.

---

##  Features

- 📁 Upload documents and ingest them into a vector store.
- 🔍 Retrieves top-k most relevant chunks using semantic search.
- 💬 Generates accurate, grounded answers with inline citations.
- ⚡ Fast response (≤ 3 seconds).
- 🌐 Streamlit Web UI & CLI support.
- 📓 Jupyter/Colab demo for presentations.

---

##  Project Structure

```

doc-chatbot/
├── app/
│   ├── document\_ingestor.py   # Extracts and embeds documents
│   ├── retriever.py           # Searches top-k relevant chunks
│   ├── generator.py           # Generates answer using Cohere
│   └── utils.py               # Helper functions
├── sample\_docs/               # Demo documents for testing
├── app.py                     # CLI interface
├── web\_ui.py                  # Streamlit Web UI
├── demo.ipynb                 # Google Colab/Jupyter notebook
├── requirements.txt
└── .env                       # Environment variables (Cohere API Key)

````

---

##  Installation

```bash
git clone https://github.com/your-username/doc-chatbot.git
cd doc-chatbot
pip install -r requirements.txt
````

---

##  Environment Setup

Create a `.env` file in the root:

```env
COHERE_API_KEY=your-cohere-api-key
```

---

##  1. Run via CLI

```bash
python app.py --docs_path sample_docs
```

 Type your question in the terminal after ingestion.

---

##  2. Run via Streamlit Web UI

```bash
streamlit run web_ui.py
```

* Upload your `.pdf`, `.txt`, or `.md` documents
* Ask questions interactively
* See cited sources and latency

---

##  3. Run via Google Colab

1. Open `demo.ipynb` or create a new notebook
2. Upload `doc-chatbot.zip` and your resume
3. Run step-by-step cells
4. Ask questions like:

   * *"What are my skills?"*
   * *"Where did I intern?"*

---

##  How It Works

###  Embedding

* Uses `sentence-transformers` (`all-MiniLM-L6-v2`) to convert text into vectors
* Stored with FAISS for fast similarity search

###  Retrieval

* Top-k similar chunks (context) are fetched for a question

### Generation

* Cohere’s `command` model generates an answer grounded in retrieved chunks
* Inline citations are added like: `[filename]`

---

##  Example Questions

> Upload your resume and ask:

* “What projects have I done?”
* “What programming languages do I know?”
* “Where did I study?”

---

##  Sample Demo Files

You can use preloaded files from `sample_docs/` or upload your own:

* `architecture.md`
* `failure_handling.txt`
* `project_goals.pdf`

---

## 🛡 License

MIT License. Feel free to fork and modify!

---

## 🙋‍♂️ Author

Buthuru Venkat Reddy