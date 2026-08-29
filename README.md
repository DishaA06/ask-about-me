# 💬 Ask About Me

An AI-powered personal assistant that answers questions about my **background, skills, projects, certifications, and experience** using information from my actual documents.

Instead of relying on generic LLM knowledge, the application uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from my personal data and generate grounded answers.

---

## ✨ Features

- 🤖 Ask questions about my background, skills, projects, and certifications
- 🔎 Retrieval-Augmented Generation (RAG) for grounded responses
- 📄 Supports information from resumes, project descriptions, and certifications
- 🧠 Semantic search using Hugging Face embeddings
- ⚡ FAISS vector database for fast document retrieval
- 💬 Interactive Streamlit chat interface
- 🔌 FastAPI backend for serving the RAG pipeline
- 📚 Displays the sources used to generate an answer
- 🛡️ Designed to avoid hallucinating information outside the provided context

---

## 🏗️ Architecture

```text
                 Personal Documents
                        │
        ┌───────────────┼────────────────┐
        │               │                │
      Resume         Projects       Certifications
        │               │                │
        └───────────────┼────────────────┘
                        ↓
              Document Ingestion
                        ↓
              Text Chunking
                        ↓
             Hugging Face Embeddings
                        ↓
                  FAISS Index
                        ↓
                   Retriever
                        ↓
              Relevant Context
                        ↓
                  RAG Prompt
                        ↓
                 Groq LLM
                        ↓
                    Answer
                        ↑
                 User Question
                        │
                  Streamlit UI
