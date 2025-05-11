"""
Streamlit AI Chatbot App

This app provides a web-based chat interface using Streamlit and LangChain. Users can interact with an AI assistant powered by a configurable language model. The chat history is maintained in the session state for a seamless conversational experience. Model configuration is loaded from environment variables or defaults.
"""
import os

# Load environment variables from a .env file
from dotenv import load_dotenv
# Import LangChain chat model and message types
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import streamlit as st  # Streamlit for building the web UI

# Load environment variables (e.g., model name, provider, temperature)
load_dotenv()

# Initialize the chat language model using environment variables or defaults
llm = init_chat_model(
    model=os.getenv("MODEL_NAME", "llama3.2:latest"),
    model_provider=os.getenv("MODEL_PROVIDER", "ollama"),
    temperature=float(os.getenv("TEMPERATURE", "0.7")),
)

# Set the title of the Streamlit app
st.title("✨ AI Chatbot")

# Initialize the chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(
            content="You are a helpful assistant. Answer the user's questions."
        )
    ]

# Display the chat history (user and assistant messages)
for i, message in enumerate(st.session_state.messages):
    if isinstance(message, HumanMessage):
        # Show user messages in the chat UI
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        # Show assistant messages in the chat UI
        with st.chat_message("assistant"):
            st.markdown(message.content)

# Input box for the user to type a new message
prompt = st.chat_input(
    "Ask me anything!",  # Label for the input box
    key="user_input",  # Key for session state
)

# When the user submits a message
if prompt:
    # Display the user's message and add it to the chat history
    with st.chat_message("user"):
        st.markdown(prompt)
        st.session_state.messages.append(HumanMessage(content=prompt))

    # Show a spinner while waiting for the model's response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm(st.session_state.messages)
        st.markdown(response.content)
        st.session_state.messages.append(AIMessage(content=response.content))
