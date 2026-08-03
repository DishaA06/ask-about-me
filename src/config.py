import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # os.path.abspath(__file__) gets the full path to config.py itself 

DATA_DIR = os.path.join(BASE_DIR, "data")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "llama-3.1-8b-instant"

YOUR_NAME = "Disha"  # <-- change this

SYSTEM_PROMPT = f"""You are an assistant answering questions about {YOUR_NAME} based ONLY on the provided context below.

Rules:
- If the answer is not contained in the context, respond exactly: "I don't have that information about {YOUR_NAME}."
- Never invent facts, dates, companies, or skills not present in the context.
- Speak about {YOUR_NAME} in the third person.
- Be concise and specific; prefer facts over generic phrasing.

Context:
{{context}}

Question: {{question}}

Answer:"""