# Exercise 7: FAQ Bot with Streamlit

This project is a Streamlit application that provides an FAQ bot using various technologies including Langchain, OpenAI, and LlamaParse. The bot answers user queries based on a parsed FAQ document.

## Requirements

- Python 3.9+
- `streamlit`
- `dotenv`
- `langsmith`
- `llama-parse`
- `langchain`
- `faiss-cpu`
- `openai`

## Installation

1. Clone the repository or download the `exercise-7.py` file.
2. Install the required Python packages using pip:
   ```bash
   pip install streamlit python-dotenv langsmith llama-parse langchain faiss-cpu openai
    ```
3. To add a persistent environment variable, you’ll typically need to edit your user profile files based on the shell you’re using. The most common shells and their respective files are:

    - Bash: ~/.bashrc or ~/.bash_profile
	- Zsh: ~/.zshrc
	- Fish: ~/.config/fish/config.fish

    Open the file with a text editor:
    ```bash
    nano ~/.bashrc
    ```
    And add the following line:
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    LANGCHAIN_API_KEY=your_langchain_api_key
    LLAMA_PARSE_API_KEY=your_llama_parse_api_key
    ```

## Usage

1. Run the script:
    ```bash
    streamlit run exercise-7.py
    ```
2. Navigate to the app in your browser.
3. Enter your query in the text input field and submit. The bot will display the answer based on the relevant section from the FAQ document.

## Features

- Load and parse PDF documents containing FAQs.
- Split document text into manageable chunks.
- Store text chunks in a vector store for similarity search.
- Use OpenAI's GPT-4 model to generate responses based on the most relevant FAQ section.
