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

chat = model.start_chat(history=gemini_history)
print("Chatbot ready! Type 'quit' to exit.")
while True:
    user_input = input("You: ")
    if user_input == "quit":
        break
    try:
        response = chat.send_message(user_input, request_options={"timeout": 10})
        print("Bot:", response.text)
    except Exception as e:
        print(f"[Something went wrong: {e}]")

history_data = []
for message in chat.history:
    history_data.append({"role": message.role, "text": message.parts[0].text})
with open("chat_history.json", "w") as f:
    json.dump(history_data, f, indent=2)
print("Saved to chat_history.json")
