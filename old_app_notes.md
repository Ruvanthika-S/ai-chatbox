THIS IS WHERE WE THIS LINE 116 IS REMOVED( ACTUALLY REMVING IS BETTER)
# Day 5 Notes - Understanding `st.chat_input()` and Streamlit Reruns

## The Big Confusion

I was imagining:

```python
user_input = input("Type your message: ")
```

But:

```python
user_input = st.chat_input("Type your message...")
```

does NOT work like that.

That misunderstanding was causing most of my confusion about Streamlit.

---

# Normal Python Input

Example:

```python
name = input("Enter name: ")

print("Hello")
```

Flow:

```
Program starts
↓
Reaches input()
↓
Stops completely
↓
WAITS
WAITS
WAITS
↓
User types Ruvanthika
↓
Presses Enter
↓
input() returns "Ruvanthika"
↓
Program continues
↓
print("Hello")
```

Mental model:

```
Line 1
Line 2
STOP HERE
WAIT FOR USER
CONTINUE
```

The program is frozen until the user enters something.

---

# Streamlit Chat Input

Example:

```python
user_input = st.chat_input("Type your message...")
```

This does NOT mean:

```
Stop execution and wait
```

Instead, it means:

```
Hey Streamlit,
draw a chat box at the bottom of the page.
```

It creates the chat input widget.

Example:

```
--------------------------------
| Type your message...        |
--------------------------------
```

---

# What Happens When The App First Opens?

The app starts running from line 1.

Eventually it reaches:

```python
user_input = st.chat_input("Type your message...")
```

At this moment:

No message has been submitted.

Therefore:

```python
user_input = None
```

Then:

```python
if user_input:
```

becomes:

```python
if None:
```

which is:

```python
False
```

So the Gemini code does not run.

The script reaches the end and finishes.

Now Streamlit waits for user interaction.

---

# What Happens When User Types "What is Python?"

User types:

```
What is Python?
```

and presses Enter.

This is the important part.

The app is NOT waiting at line 96.

The previous run already ended.

Instead:

```
User presses Enter
↓
Streamlit notices widget interaction, and STORES THAT WIDGET INTERACTION THAT 
IS "WHAT IS PYTHON" SOMEWHERE

↓
Streamlit starts app.py from line 1 again
```

This is called a rerun.

---

# During The Rerun

The entire file starts again.

Eventually Streamlit reaches:

```python
user_input = st.chat_input("Type your message...")
```

Now Streamlit checks its widget state and sees:

```
The user just submitted:
"What is Python?"
```

Therefore:

```python
user_input = "What is Python?"
```

NOT:

```python
user_input = None
```

Then:

```python
if user_input:
```

becomes:

```python
if "What is Python?":
```

which is:

```python
True
if user_input:
    try:
        with st.chat_message("user"):
            st.write(user_input) #JUST WRITES THAT QUESTION WE ASKED IN THE SCREEN TO MAKE IT LOOK PRESENTABLE.

        response = st.session_state.chat.send_message(
        user_input,
        request_options={"timeout": 10}
    )

        with st.chat_message("assistant"):
            st.write(response.text)
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        st.session_state.chat_history.append({"role": "model", "text": response.text})

        if not st.session_state.current_chat: #that is if st.session_state.current_chat=None , this indicates its a new chat so no file name is assigned yet
            title = generate_chat_title(user_input)
            st.session_state.current_chat = title
            st.rerun() #NOTE THIS RERUN IS NOT ACTUALLY NEEDED

        save_chat(st.session_state.current_chat, st.session_state.chat_history)
       
    except Exception as e:
        st.error(f"Something went wrong: {e}")

```

NOW THIS PART RUNS

---

# Important Mental Model

Do NOT think:

```python
st.chat_input()
```

=

```python
input()
```

Think:

```python
st.chat_input()
```

=

```
A textbox widget
that sometimes returns a submitted value
```

Similar to:

```python
st.button()
```

which returns:

```python
True
```

when clicked,

and

```python
False
```

otherwise.

Similarly:

```python
st.chat_input()
```

returns:

```python
"What is Python?"
```

when the user submits a message,

and

```python
None
```

otherwise.

---

# Better Analogy

Think:

```python
user_input = st.chat_input(...)
```

as:

```python
user_input = get_latest_submitted_message()
```

NOT:

```python
user_input = wait_until_user_types()
```

That is the key difference.

---

# Full Conversation Flow

Assume user starts a completely new chat.

---

## Step 1

App starts.

```python
user_input = None
```

because nothing was submitted.

Script finishes.

Streamlit waits.

---

## Step 2

User types:

```
What is Python?
```

and presses Enter.

This triggers a rerun.

---

## Step 3

App starts from line 1 again.

Eventually:

```python
user_input = "What is Python?"
```

because Streamlit remembers the submitted widget value.

---

## Step 4

This becomes true:

```python
if user_input:
```

Gemini receives:

```
What is Python?
```

and generates a response.

Example:

```
Python is a programming language...
```

---

## Step 5

History is updated:

```python
st.session_state.chat_history.append(
    {"role": "user", "text": "What is Python?"}
)

st.session_state.chat_history.append(
    {"role": "model", "text": "Python is a programming language..."}
)
```

Now:

```python
st.session_state.chat_history
```

contains:

```python
[
    {"role": "user", "text": "What is Python?"},
    {"role": "model", "text": "Python is a programming language..."}
]
```

---

## Step 6

*if* not st.session_state.current_chat:

            title = generate_chat_title(user_input)

            st.session_state.current_chat = title

         

A title is generated.

Example:

```
Python Learning Help
```

Stored as:

```python
st.session_state.current_chat
```

---

## Step 7 SINCE WE DIDNT PUT MANUAL RERUN, NO RERUN HAPPENS

    save_chat(st.session_state.current_chat, st.ses

Chat is saved to JSON file.

Example:

```
chats/Python Learning Help.json
```

---

## Step 8

Script reaches the end.

Run finishes.

Streamlit waits again.

---

# User Sends Another Message

User types:

```
What is C++?
```

and presses Enter.

Again:

```
Widget interaction
↓
Entire app reruns
```

---

# Why Can I Still See The Old Messages?

This was another major confusion.

The old messages do NOT come from:

```python
st.chat_input()
```

They come from:

```python
st.session_state.chat_history
```

using this loop:

```python
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(message["text"])
```

This loop redraws every message stored in history.

---

# What This Loop Actually Does

Suppose history contains:

```python
[
    {"role": "user", "text": "What is Python?"},
    {"role": "model", "text": "Python is a programming language..."}
]
```

The loop draws:

```
User: What is Python?
Assistant: Python is a programming language...
```

on the screen.

Every rerun.

---

# Most Important Realization

The screen is NOT preserved.

Instead:

```
Rerun
↓
Read chat_history
↓
Redraw all messages
↓
Screen looks identical
```

Therefore:

```
chat_history = data storage

for message in chat_history = display logic
```

The data survives because of:

```python
st.session_state.chat_history
```

The messages appear because the loop redraws them every rerun.

---

# Final Answers

Q: When the app first opens, before the user types anything, what is stored in `user_input`?

Answer:

```python
user_input = None
```

because no message has been submitted.

---

Q: After the user submits:

```
What is Python?
```

what is stored in `user_input` during that rerun?

Answer:

```python
user_input = "What is Python?"
```

because Streamlit remembers the widget submission and returns it during that rerun.
