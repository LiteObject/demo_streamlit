"""
Streamlit AI Chatbot App

This app allows users to ask questions and optionally upload a PDF file. 
If a PDF is uploaded, its text is included in the prompt to the language 
model. The app uses environment variables for model configuration and 
provides user-friendly error handling and feedback.
"""
import os
from dotenv import load_dotenv  # For loading environment variables from a .env file
import streamlit as st  # Streamlit for building the web UI
# For initializing the chat model
from langchain.chat_models import init_chat_model
from langchain.prompts import PromptTemplate  # For prompt templates
from pypdf import PdfReader  # For reading PDF files
from pypdf.errors import PdfReadError  # For handling PDF read errors

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
st.title("✨ Ask AI")

# File uploader widget for PDF files
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# Text area for user to enter their question
user_input = st.text_area(
    "Ask me anything!",  # Label for the input box
    placeholder="Type your question here...",  # Placeholder text
    key="user_input",  # Key for session state
    value=""  # Default value
)

# Button to submit the question
button = st.button("Submit")

# When the button is pressed and the input is not empty
if button and user_input.strip():
    # Show a spinner while processing
    with st.spinner("Processing..."):
        text = ""  # Will hold extracted PDF text if any
        if uploaded_file:
            try:
                pdf_reader = PdfReader(uploaded_file)  # Read the uploaded PDF
                # Limit to first 10 pages and max 8000 characters to avoid model input overflow
                for i, page in enumerate(pdf_reader.pages[:10]):
                    page_text = page.extract_text() or ""  # Extract text from each page
                    text += page_text
                    if len(text) > 8000:
                        text = text[:8000] + "..."  # Truncate if too long
                        break
            except PdfReadError as e:
                # Show error if PDF can't be read
                st.error(f"Failed to read PDF: {e}")
                text = ""
            except FileNotFoundError as e:
                # Show error if file not found
                st.error(f"File not found: {e}")
                text = ""
        # Choose prompt template based on whether PDF text is present
        if text:
            prompt_template = PromptTemplate.from_template("""
                            You are a helpful assistant. Answer the question based on the provided text:

                            <question>
                            {question}
                            </question>
                            <text>
                            {text}
                            </text>
                            """)
        else:
            prompt_template = PromptTemplate.from_template("""
                            You are a helpful assistant. Answer the question:

                            <question>
                            {question}
                            </question>
                            """)
        # Fill the prompt template with user input and PDF text (if any)
        formatted_prompt = prompt_template.format(
            question=user_input,
            text=text
        )
        try:
            # Send the prompt to the language model
            response = llm.invoke(formatted_prompt)
            st.write(response.content)  # Display the model's response
        except llm.ModelInvocationError as e:
            # Show error if model fails
            st.error(f"Model invocation failed: {e}")
        except TimeoutError as e:
            # Show error if model times out
            st.error(f"Model invocation timed out: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")  # Show any other errors
            raise  # re-raise the exception
