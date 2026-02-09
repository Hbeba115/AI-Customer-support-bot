import streamlit as st
import os
from app.chatbot import get_ai_answer, collection
import json 
from pathlib import Path

st.set_page_config(page_title="Customer Support Chatbot")
st.title("Customer Support Chatbot 🤖")

user_input = st.text_input("Ask a question about the documents:")

# Initialize session state for chat
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if st.button("Send") and user_input:
    try:
        # Generate AI answer
        answer = get_ai_answer(user_input, collection)

        # Append to session state
        st.session_state["messages"].append(("You", user_input))
        st.session_state["messages"].append(("AI", answer))

        # -----------------------------
        # Save chat history to JSON
        # -----------------------------
        chat_file = Path("data/chat_history.json")
        chat_file.parent.mkdir(exist_ok=True)

        if chat_file.exists():
            existing = json.loads(chat_file.read_text())
        else:
            existing = []

        # Append only the latest user+AI pair
        existing.append(st.session_state["messages"][-2:])
        chat_file.write_text(json.dumps(existing, indent=2))

    except Exception as e:
        st.error(f"Error generating answer: {e}")

# -----------------------------
# Display multi-turn conversation
# -----------------------------
st.markdown("### Current Session Conversation")
for speaker, message in st.session_state["messages"]:
    if speaker == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**AI:** {message}")

# -----------------------------
# Optional: View full chat history
# -----------------------------
st.markdown("---")
st.markdown("### Full Chat History")

if st.button("Load Chat History"):
    chat_file = Path("data/chat_history.json")
    if chat_file.exists():
        history = json.loads(chat_file.read_text())
        for i, pair in enumerate(history, 1):
            st.markdown(f"**Conversation {i}:**")
            for speaker, message in pair:
                st.markdown(f"**{speaker}:** {message}")
            st.markdown("---")
    else:
        st.info("No chat history found.")