import streamlit as st
from openai import OpenAI
import os

# Load your OpenAI API key from Streamlit Secrets
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("💬 Chat with GPT-3.5")

# User input
user_input = st.text_input("You:", "")

# Chat history stored in session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show past messages
for msg in st.session_state.messages:
    st.markdown(f"**{msg['role'].capitalize()}**: {msg['content']}")

# On submit
if user_input:
    # Add user message to session
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get GPT-3.5 response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages
    )

    # Add assistant response to session
    assistant_msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": assistant_msg})

    # Display response
    st.markdown(f"**Assistant**: {assistant_msg}")
