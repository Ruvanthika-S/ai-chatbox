import streamlit as st
import google.generativeai as genai
import os
import json

CHATS_FOLDER = "chats"
 #You never create the chats folder.Your code assumes:CHATS_FOLDER = "chats" already exists.If I clone your GitHub repo and run:streamlit run app.pyit crashes.
os.makedirs(CHATS_FOLDER, exist_ok=True)  #If folder exists → do nothing . If folder doesn't exist →create it

def get_all_chats():

    files = [f for f in os.listdir(CHATS_FOLDER)
             if f.endswith(".json")]

    files.sort(
        key=lambda f: os.path.getmtime(
            os.path.join(CHATS_FOLDER, f)
        ),
        reverse=True
    )
    chats = [f.replace(".json", "") for f in files]
    return chats

def load_chat(chat_name):
    path = f"{CHATS_FOLDER}/{chat_name}.json" # builds path like "chats/python help.json"
    if os.path.exists(path):      # checks if file exists
        with open(path, "r") as f:
            return json.load(f)   # reads file, returns conversation as Python list
    return []

def save_chat(chat_name, history):
    path = f"{CHATS_FOLDER}/{chat_name}.json"
    with open(path, "w") as f:
        json.dump(history, f, indent=2)      # writing history of that particular chat

def generate_chat_title(first_message):
    title_model = genai.GenerativeModel("gemini-2.5-flash")      # creates a fresh Gemini model with no personality, just for generating titles
    response = title_model.generate_content(
        f"Generate a short 3-4 word title for a conversation that starts with: '{first_message}'. Return ONLY the title, nothing else.")   # sends a one-time message to Gemini (not a chat, just a single request) asking it to generate a title
    title = response.text.strip()
    title = "".join(c for c in title if c not in r'\/:*?"<>|')
    return title

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("GEMINI_API_KEY not found!")
    st.stop()
genai.configure(api_key=api_key)
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="You are a rude,mean, sarcastic assistant who explains things simply and keeps responses short but that doesn't mean your responses are wrong , you give give correct information ."
)

st.title("My AI Chatbot")

with st.sidebar: #everything indented inside this block appears in the left sidebar panel
    st.title("My Chats")

    #!!!!!!!!!PEAKK!!!!!!!
    
    if st.button("+ New Chat"):   #creates a button, returns True when clicked
        st.session_state.current_chat = None #resets current chat name to none (fresh start)
        st.session_state.chat_history = [] #clears chat history
        st.session_state.chat = model.start_chat(history=[]) #fresh Gemini chat object
        st.rerun() #forces Streamlit to rerun the script immediately so the UI updates
    
    st.divider() #draws a horizontal line to separate New Chat button from chat list
    
    all_chats = get_all_chats() 

    for chat_name in all_chats:

        #!!!!!PEAKK!!!!!!! THIS IS EXACTLY WHAT HAPPENS IF U CLICK ON OLD CHATS AND ATLAST RERUN IS GIVE SO APART FROM THIS IF BLOCK (NOTE THIS IF STATEMENT 
        #BECOMES TRUE ONLY IF U PRESS A OLD CHAT),NOW ANOTHER DOUBT WHAT IF WE DIDNT PRESS AN OLD CHAT EXACTLY DURING THAT ITERATION OF THAT CHAT DURING 
        #THE FOR LOOP(IK ITS IMPOSSIBLE) THAT'S COZ EVERYTIME U DO SMTG THE ENTIRE STREMLIT RUNS AGAIN SO NOW U SAY U CLICKED CHAT 2 NOW OUR 
        #ENITRE CODE RUNS AGAIN AND NOW WHEN THE ITERATIION OF CHAT2 COMES , IT WILL BE CONSIDERED AS TRUE !!!!!! , 
        #THE ENTIRE CODE IS FOR THIS CHAT WE CLICKED ( RENAMED AS CURRENT_CHAT) IN THAT FOR LOOP WE WILL HAVE TO MODIFY THE IF STATEMENT TO MAKE IT TRUE 
        
        if st.button(chat_name): #creates a button for each chat, if clicked loads that chat
            st.session_state.current_chat = chat_name
            st.session_state.chat_history = load_chat(chat_name)
            gemini_history = []
            for message in st.session_state.chat_history:
                gemini_history.append({"role": message["role"], "parts": [message["text"]]})
            st.session_state.chat = model.start_chat(history=gemini_history)
            st.rerun()

#st.session_state is just a dictionary . 
#eg: st.session_state["name"] = "app"st.session_state.name = "app". 
#Streamlit reruns your entire script every time you send a message. Normal variables reset to nothing on every rerun. st.session_state survives reruns 

if "current_chat" not in st.session_state:
    st.session_state.current_chat = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat" not in st.session_state:
    gemini_history = []
    st.session_state.chat = model.start_chat(history=gemini_history)

#this is responsible for older conversation of the same chat to be appearing on the screen, even no matter how many reruns happens.
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["text"])

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
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        st.session_state.chat_history.append({"role": "model", "text": response.text})

        
        #that is if st.session_state.current_chat=None , this indicates its a new chat so no file name is assigned yet
        if not st.session_state.current_chat:

            title = generate_chat_title(user_input)
            # Make title unique here. That if there is someother chat with that title aldready available , we change title of this new chat
            original_title = title
            counter = 1

            while os.path.exists(f"{CHATS_FOLDER}/{title}.json"):
                title = f"{original_title} ({counter})"
                counter += 1

            st.session_state.current_chat = title

            save_chat(st.session_state.current_chat,st.session_state.chat_history)

            st.rerun() # NOTE THIS IS NOT SAME AS OLD_APP 'S RERUN HERE WE ARE SAVING THE FIRST CAHT ITESELF TO THE FILE AND ONLY THEN RERUNNING ONLY BECOZ ONLY THEN THIS all_chats = get_all_chats() WILL BE TRIGERRED AND A NEW BUTTON FOR THIS NEW CHAT WITH THIS NEW NAME WILL BE ON THE SIDE BAR DURING THE FIRST CONVERSTAION ITSELF
        else:
            save_chat(st.session_state.current_chat,st.session_state.chat_history)
       
    except Exception as e:
        st.error(f"Something went wrong: {e}")




