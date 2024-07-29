# Exercise 6: Streamlit App for Article Summarizer and Story Generator

This Streamlit app provides two functionalities: summarizing articles from the internet and generating children's stories based on a given topic. It uses OpenAI's GPT-4 model for processing and generating responses.

## Requirements

- Python 3.9+
- `streamlit`
- `requests`
- `beautifulsoup4`
- `langchain`
- `python-dotenv`

## Installation

1. Clone the repository or download the `exercise-6.py` file.
2. Install the required Python packages using pip:
   ```bash
   pip install streamlit requests beautifulsoup4 langchain python-dotenv
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
    ```

## Usage

1. Run the script:
    ```bash
    streamlit run exercise-6.py
    ```
2. Navigate to the app in your browser.

## Features

1. Article Summarizer
    - Functionality: Allows users to input the URL of an article to receive a brief summary.
    - Usage:
        - Enter the URL of the article in the text input field.
        - Click "Summarize" to generate and display the summary of the article.
2. Story Generator
    - Functionality: Generates and develops children's story ideas based on a given topic.
    - Usage:
        - Enter a topic for a children's story in the text input field.
        - Click "Generate Story Ideas" to see a list of generated story ideas.
        - Select a story idea number and click "Develop Story" to get the full story based on the selected idea.