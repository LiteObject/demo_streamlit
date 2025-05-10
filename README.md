# Streamlit Demo - AI Chatbot
This is a simple Streamlit application that allows users to interact with a chatbot powered by the Llama 3.2 model. Users can ask questions and upload PDF files for context.

### What is Streamlit?
[Streamlit](https://streamlit.io/) is an open-source app framework for Machine Learning and Data Science projects. It allows you to create beautiful web applications with minimal effort.

## Installation

1. **Clone the repository** (if you haven't already):
   ```sh
   git clone <your-repo-url>
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
   - Create a `.env` file in the project directory (optional, but recommended for model configuration).
   - Example `.env` content:
     ```env
     MODEL_NAME=llama3.2:latest
     MODEL_PROVIDER=ollama
     TEMPERATURE=0.7
     ```

## Running the App

To start the chatbot app, run:

```sh
streamlit run ask_app.py
```

- The app will open in your browser at `http://localhost:8501` by default.
- You can ask questions and optionally upload a PDF file for context.

---

- For any issues, ensure all dependencies are installed and your environment variables are set correctly.