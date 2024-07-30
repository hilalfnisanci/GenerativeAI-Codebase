# Exercise 8: Research Paper Summarization

This repository contains two Python scripts for processing and summarizing research papers using vector databases and a Streamlit application.

## Requirements

- Python 3.9+
- `pinecone-client`
- `unstructured`
- `sentence-transformers`
- `streamlit`
- `langchain`
- `openai`

## Installation

1. Clone the repository or download the `exercise-8` folder.
2. Install the required Python packages using pip:
   ```bash
    pip install pinecone-client unstructured sentence-transformers streamlit langchain openai
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
    PINECONE_API_KEY=your_pinecone_api_key
    ```

## Usage

1. Run the scripts:
- Firstly:
    ```bash
    python exercise-8.py
    ```
- Secondly:
    ```bash
    streamlit run exercise-8-streamlitApp.py
    ```

## Scripts

1. `exercise-8.py`

    This script performs the following tasks:

    - Vector Database Setup: Initializes Pinecone with indexes for different sections of research papers (abstract, introduction, methodology, results, conclusion).

    - Document Processing: Reads PDFs from the research_papers directory, partitions them into sections, and splits sections into chunks.

    - Vector Storage and Retrieval: Uses Sentence Transformers to create vectors for each chunk and uploads them to the respective Pinecone indexes.

2. `exercise-8-streamlitApp.py`

    This Streamlit app provides a user interface to:

    - Query Input: Enter a query to specify which section of the research paper to summarize.

    - Summary Retrieval: Identifies the relevant section, queries the Pinecone index for relevant content, and uses OpenAI's model to generate a summary.

