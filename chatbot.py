import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6Idq2FHpem4UnnU1UMBwwgBJHc_w-7GvzxDSpQVD9T2ZA")

model = genai.GenerativeModel("gemini-2.5-flash")
chat = model.start_chat()

print("Chatbot ready! Type 'quit' to exit.")

while True:
    user_input = input("You: ")
    if user_input == "quit":
        break
    response = chat.send_message(user_input)
    print("Bot:", response.text)