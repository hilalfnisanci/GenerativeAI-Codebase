# Exercise 1: AI Advancements Summary

This script uses the OpenAI GPT-4 model to provide a summary of the latest advancements in artificial intelligence as of 2024. It utilizes the Langchain library for managing the chat prompt and parsing the output.

## Requirements

- Python 3.9+
- `langchain`
- `python-dotenv`

## Installation

1. Clone the repository or download the `exercise-1.py` file.
2. Install the required Python packages using pip:
   ```bash
   pip install langchain python-dotenv
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
    python exercise-1.py
    ```
2. The script will generate a summary of the latest AI advancements and save it to a file named ai_advancements_summary.txt.


