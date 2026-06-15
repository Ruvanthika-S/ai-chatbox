import google.generativeai as genai
import os
import json
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="You are a rude,mean, sarcastic assistant who explains things simply and keeps responses short but that doesn't mean your responses are wrong , you give give correct information ."
)

chat = model.start_chat()

print("Chatbot ready! Type 'quit' to exit.")

while True:
    user_input = input("You: ")
    if user_input == "quit":
        break
    response = chat.send_message(user_input)
    print("Bot:", response.text)


history_data = []
for message in chat.history:
    history_data.append({"role": message.role, "text": message.parts[0].text})

with open("chat_history.json", "w") as f:
    json.dump(history_data, f, indent=2)

print("Saved to chat_history.json")