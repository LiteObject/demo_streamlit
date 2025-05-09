import os
from dotenv import load_dotenv  # For loading environment variables from a .env file
import streamlit as st  # Streamlit for building the web UI
# For initializing the chat model
from langchain.chat_models import init_chat_model
# (Not used, but imported for prompt templates)
from langchain.prompts import PromptTemplate

# Load environment variables from a .env file (if present)
load_dotenv()

# Initialize the chat model using environment variables or defaults
llm = init_chat_model(
    # Model name from .env or default
    os.getenv("MODEL_NAME", "llama3.2:latest"),
    # Provider from .env or default
    model_provider=os.getenv("MODEL_PROVIDER", "ollama"),
    # Temperature from .env or default
    temperature=float(os.getenv("TEMPERATURE", "0.7")),
)

# Set the title of the Streamlit app
st.title("AI Chatbot")

# Create a text input box for the user to enter their question
user_input = st.text_input(
    "Ask me anything!",  # Label for the input box
    placeholder="Type your question here...",  # Placeholder text
    key="user_input",  # Key for session state
    value=""  # Default value
)

# Create a submit button
button = st.button("Submit")

# When the button is pressed and the input is not empty
if button and st.session_state.user_input.strip():
    # Send the user's input to the chat model and get a response
    response = llm.invoke(st.session_state.user_input)
    # Display the response in the app
    st.write(response.content)
