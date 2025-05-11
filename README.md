# Streamlit AI Chatbot & Q&A Demo

This repository contains two Streamlit web applications: an AI Chatbot and a Question Answering (Q&A) app. Both apps leverage large language models via LangChain, allowing users to interact with an AI assistant, ask questions, and optionally upload PDF files for context-aware answers. Chat history is maintained for a seamless conversational experience.

## Features

- **AI Chatbot:** Engage in multi-turn conversations with an AI assistant.
- **Q&A App:** Ask questions and get answers, with optional PDF upload for context.
- **PDF Support:** Upload documents to provide additional context for your queries.
- **Configurable Models:** Easily switch models and providers using environment variables.
- **Session History:** Chat and Q&A history is preserved during your session.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/LiteObject/demo_streamlit.git
   cd demo_streamlit
   ```

2. **(Recommended) Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Create a `.env` file in the project directory (optional, for model configuration).
   - Example `.env`:
     ```
     MODEL_NAME=llama3.2:latest
     MODEL_PROVIDER=ollama
     TEMPERATURE=0.7
     ```

## Running the Apps

- **Chatbot App:**
  ```sh
  streamlit run chat_app.py
  ```

- **Q&A App:**
  ```sh
  streamlit run ask_app.py
  ```

The app will open in your browser at `http://localhost:8501` by default.

## Requirements

- Python 3.10+
- See `requirements.txt` for Python dependencies.

---

For any issues, ensure all dependencies are installed and your environment variables are set correctly.