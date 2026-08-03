from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.rag_chain import load_chain

app = FastAPI(title="Ask About Me API")

# Allow the Streamlit app (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the chain ONCE when the server starts, not per-request
chain, retriever = load_chain()


class Question(BaseModel):
    question: str


@app.get("/")
def root():
    return {"status": "Ask About Me API is running"}


@app.post("/ask")
def ask(payload: Question):
    answer = chain.invoke(payload.question)
    sources = retriever.invoke(payload.question)
    return {
        "answer": answer,
        "sources": [doc.metadata.get("source", "unknown") for doc in sources]
    }