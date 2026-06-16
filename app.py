import streamlit as st
import google.generativeai as genai
import os
import json
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="You are a rude,mean, sarcastic assistant who explains things simply and keeps responses short but that doesn't mean your responses are wrong , you give give correct information ."
)
if os.path.exists("chat_history.json"):
    with open("chat_history.json", "r") as f:
        saved_history = json.load(f)
else:
    saved_history = []

gemini_history = []
for message in saved_history:
    gemini_history.append({"role": message["role"], "parts": [message["text"]]})

if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=gemini_history)
for message in saved_history:
    with st.chat_message(message["role"]):
        st.write(message["text"])
st.title("My AI Chatbot")
user_input = st.chat_input("Type your message...")

if user_input:
    try:
        with st.chat_message("user"):
            st.write(user_input)

        response = st.session_state.chat.send_message(
        user_input,
        request_options={"timeout": 10}
    )

        with st.chat_message("assistant"):
            st.write(response.text)
        history_data = []
        for message in st.session_state.chat.history:
            history_data.append({"role": message.role, "text": message.parts[0].text})
        with open("chat_history.json", "w") as f:
            json.dump(history_data, f, indent=2)

    except Exception as e:
        st.error(f"Something went wrong: {e}")



