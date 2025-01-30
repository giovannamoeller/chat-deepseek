import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up the DeepSeek API key
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
OPENAI_API_KEY = os.getenv("OPEN_AI_API_KEY")
MODEL_NAME = "deepseek-chat"

# Initialize the OpenAI client
client = OpenAI(api_key=DEEPSEEK_API_KEY,
                base_url="https://api.deepseek.com")

st.title("Simple Chat")

# Initialize chat history
if "messages" not in st.session_state:
  st.session_state.messages = [
    {"role": "system", "content": "You are a helpful assistant specialized in software engineering. Always give clean code, provide clean architecture, etc."}
  ]

# Display chat messages from history on app rerun (skip system messages)
for message in st.session_state.messages:
  if message["role"] != "system":  # Skip rendering the system message
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
  # Add user message to chat history
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)
    
  # Display assistant response dynamically
  with st.chat_message("assistant"):
    try:
      # Create a stream response from DeepSeek AI
      stream = client.chat.completions.create(
        model=MODEL_NAME,
        messages=st.session_state.messages,
        stream=True
      )

      # Collect the response dynamically
      response = ""
      message_container = st.empty()  # Dynamic container for assistant response
      for chunk in stream:
        if chunk.choices[0].delta.content is not None:
          response += chunk.choices[0].delta.content
          message_container.markdown(response)  # Update dynamically

      # Add assistant response to chat history
      st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
      st.error(f"Error: {str(e)}")
