import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from src.config import VECTORSTORE_DIR, EMBEDDING_MODEL, LLM_MODEL, SYSTEM_PROMPT, GROQ_API_KEY
def load_chain():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.load_local(
        VECTORSTORE_DIR,
        embeddings,
        allow_dangerous_deserialization=True
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

    llm = ChatGroq(model=LLM_MODEL, temperature=0, api_key=GROQ_API_KEY)
    prompt = PromptTemplate.from_template(SYSTEM_PROMPT)

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever


def ask(question: str, chain, retriever) -> dict:
    answer = chain.invoke(question)
    sources = retriever.invoke(question)
    return {
        "answer": answer,
        "sources": [doc.metadata.get("source", "unknown") for doc in sources]
    }

        
if __name__ == "__main__":
    chain, retriever = load_chain()

    while True:
        q = input("\nAsk a question (or 'quit'): ")
        if q.lower() == "quit":
            break
        answer = chain.invoke(q)
        sources = retriever.invoke(q)
        print("\nAnswer:", answer)
        print("Sources:", [doc.metadata.get("source", "unknown") for doc in sources])