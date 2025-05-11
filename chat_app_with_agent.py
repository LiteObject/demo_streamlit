"""
AI Chatbot Streamlit App with Tool Integration

This module provides a simple web-based chatbot interface using Streamlit and LangChain.
Users can interact with an AI assistant, and the chat history is maintained in the session state.
A custom tool (get_weather) is integrated using LangChain's agent framework.
Model configuration is loaded from environment variables or defaults.
"""
import os

# Load environment variables from a .env file
from dotenv import load_dotenv
# Import LangChain chat model and message types
from langchain.chat_models import init_chat_model
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import streamlit as st  # Streamlit for building the web UI

# Load environment variables (e.g., model name, provider, temperature)
load_dotenv()

# Define a custom tool function for demonstration (returns fake weather info)


def get_weather(place_name: str) -> str:
    """
    Returns a string describing the weather in a given place.
    Args:
        place_name (str): The name of the place.
    Returns:
        str: A string describing the weather in the given place.
    """
    return f"Weather in {place_name} is sunny and 75 degrees fahrenheit."


# Wrap the function as a LangChain Tool
weather_tool = Tool(
    name="get_weather",
    func=get_weather,
    description="Get the weather for a given place."
)

# List of tools to provide to the agent
tools = [weather_tool]

# Initialize the chat language model using environment variables or defaults
llm = init_chat_model(
    model=os.getenv("MODEL_NAME", "llama3.2:latest"),
    model_provider=os.getenv("MODEL_PROVIDER", "ollama"),
    temperature=float(os.getenv("TEMPERATURE", "0.7")),
)

# Initialize the agent with tools and LLM
agent = initialize_agent(
    tools,  # List of tools the agent can use
    llm,    # The language model
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Agent type
    verbose=True  # Print reasoning steps to the console
)

# Set the title of the Streamlit app
st.title("✨ AI Chatbot Agent")

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
    key="user_input",    # Key for session state
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
            # Use the agent to process the chat history and tools
            response = agent.run(st.session_state.messages)
        st.markdown(response)  # Display the agent's response
        st.session_state.messages.append(AIMessage(content=response))
