# Exercise 4: Article Summarizer

This script fetches content from a list of article URLs, summarizes the articles using the OpenAI GPT-4 model, and prints the summaries. It utilizes BeautifulSoup for web scraping and Langchain for managing the summarization process.

## Requirements

- Python 3.9+
- `requests`
- `beautifulsoup4`
- `langchain`
- `python-dotenv`

## Installation

1. Clone the repository or download the `exercise-4.py` file.
2. Install the required Python packages using pip:
   ```bash
    pip install requests beautifulsoup4 langchain python-dotenv
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
    python exercise-4.py
    ```
2. The script will fetch and summarize the articles from the provided URLs and print the summaries to the console.

