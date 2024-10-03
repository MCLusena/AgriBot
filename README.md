# AgriBot

## Introduction

---

AgriBot is a project I did during my internship at the University of Colombo School of Computing (UCSC). AgriBot is a Retrieval Augmented Generation (RAG) chatbot made with Python that allows you to chat with multiple PDF documents. You can ask questions about the PDFs using natural language, and the application will provide relevant responses based on the content of the documents. This app utilizes a large language model (LLM) to generate accurate answers to agriculture related queries. Please note that the chatbot will only respond to questions related to the loaded PDFs.

## Dependencies and Installation

---

To install AgriBot, please follow these steps:

1. Clone the repository to your local machine.

2. Install the required dependencies by running the following command:

   ```
   pip install -r requirements.txt
   ```

3. Obtain an API key from OpenAI and add it to the `.env` file in the project directory.

```commandline
OPENAI_API_KEY=your_secret_api_key
```

## Usage

---

To use AgriBot, follow these steps:

1. Ensure that you have installed the required dependencies and added the OpenAI API key to the `.env` file.

2. Run the `main.py` file using the Streamlit CLI. Execute the following command:

   ```
   streamlit run app.py
   ```

3. The application will launch in your default web browser, displaying the user interface.

4. Load multiple PDF documents into the app by following the provided instructions.

5. Ask questions in natural language about the loaded PDFs using the chat interface.
