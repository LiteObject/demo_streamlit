"""
AI Chatbot Streamlit App with Tool Integration

This module provides a simple web-based chatbot interface using Streamlit and LangChain.
Users can interact with an AI assistant, and the chat history is maintained in the session state.
A custom tool (get_weather) is integrated using LangChain's agent framework.
Model configuration is loaded from environment variables or defaults.
"""
import logging
import os

import psycopg2
import streamlit as st  # Streamlit for building the web UI
# Load environment variables from a .env file
from dotenv import load_dotenv
from langchain.agents import AgentType, initialize_agent
# Import LangChain chat model and message types
from langchain.chat_models import init_chat_model
from langchain.tools import Tool
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

logging.basicConfig(level=logging.DEBUG)
logging.debug("This is a debug message")

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
    description="Use this tool to provide current weather information for a specified city or location."
)

# Initialize the chat language model using environment variables or defaults
llm = init_chat_model(
    model=os.getenv("MODEL_NAME", "llama3.2:latest"),
    model_provider=os.getenv("MODEL_PROVIDER", "ollama"),
    temperature=float(os.getenv("TEMPERATURE", "0.7")),
)

# Read DB_ values
db_host = os.getenv("DB_HOST")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_name = os.getenv("DB_NAME")
db_port = os.getenv("DB_PORT")

conn_str = (
    f"postgresql+psycopg2://"
    f"{db_user}:{db_password}"
    f"@{db_host}:{db_port}/"
    f"{db_name}?connect_timeout=5"
)

sqltoolkit = None
db_error = None

try:
    db = SQLDatabase.from_uri(conn_str)
    sqltoolkit = SQLDatabaseToolkit(db=db, llm=llm)
    # tools.extend(sqltoolkit.get_tools())
except psycopg2.Error as e:
    db_error = e
    st.write(f"DB connection error: {e}")


def general_chat_tool(query: str) -> str:
    """
    Use the LLM to answer general questions.

    Args:
        query (str): The question to be answered.

    Returns:
        str: The answer to the question.
    """
    return llm.invoke(query).content


general_chat = Tool(
    name="general_chat",
    func=general_chat_tool,
    description=(
        "Use this tool to answer any question or engage in conversation when the user's request does not match another tool. "
        "This is the default for general conversation or open-ended questions."
    )
)

# List of tools to provide to the agent
tools = [general_chat, weather_tool]
tools.extend(sqltoolkit.get_tools())

# Initialize the agent with whatever tools are available
try:
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
except (ValueError, RuntimeError) as e:
    st.error(f"Agent initialization error: {e}")
    st.stop()

# Set the title of the Streamlit app
st.title("✨ AI Chatbot Agent")

# Show DB error if it occurred
if db_error:
    st.error(f"Database error: {db_error}")

# Initialize the chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(
            content=(
                "You are a helpful assistant. "
                "For general conversation or questions, use the 'general_chat' tool. "
                "Only use the database tools if the user asks about the database. "
                "Do not list the tools to the user. Choose the best tool yourself and provide a direct answer."
            )
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
            try:
                response = agent.run(st.session_state.messages)
            except agent.AgentError as e:
                st.session_state.messages.append(
                    AIMessage(content="Sorry, something went wrong. Please try again."))
                st.error("Agent error. Please check logs for details.")
                logging.exception("Agent run failed")
            except ValueError as e:
                # Handle value errors
                st.error("Invalid input. Please try again.")
                logging.exception("Invalid input")
            else:
                st.markdown(response)
                st.session_state.messages.append(AIMessage(content=response))
