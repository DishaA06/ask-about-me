import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(page_title="Ask About Me", page_icon="💬")
st.title("💬 Ask About Me")
st.caption("Ask anything about my background, projects, and skills — grounded in my actual resume, not hallucinated.")

# Suggested questions for a frictionless demo
suggestions = [
    "What programming languages do you know?",
    "Tell me about your projects",
    "What certifications have you done?",
]

cols = st.columns(len(suggestions))
for col, sug in zip(cols, suggestions):
    if col.button(sug):
        st.session_state["pending_question"] = sug

# Keep chat history across turns
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("sources"):
            with st.expander("Sources"):
                for s in msg["sources"]:
                    st.write(s)

# Handle either a typed question or a clicked suggestion
question = st.chat_input("Ask a question...")
if "pending_question" in st.session_state:
    question = st.session_state.pop("pending_question")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"question": question})
                response.raise_for_status()
                data = response.json()
                answer = data["answer"]
                sources = data["sources"]
            except Exception as e:
                answer = f"Error reaching the API: {e}"
                sources = []

            st.markdown(answer)
            if sources:
                with st.expander("Sources"):
                    for s in sources:
                        st.write(s)

    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})