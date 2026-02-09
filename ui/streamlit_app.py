import streamlit as st
import os
from app.chatbot import get_ai_answer, collection

st.set_page_config(page_title="Customer Support Chatbot")
st.title("Customer Support Chatbot 🤖")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("Ask a question:")

if st.button("Send") and user_input:
    try:
        answer = get_ai_answer(user_input, collection)
        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append(("AI", answer))
    except Exception as e:
        st.error(f"Error: {e}")

# Display chat history
for speaker, msg in st.session_state.messages:
    if speaker == "You":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**AI:** {msg}")
