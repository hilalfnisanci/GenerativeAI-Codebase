# Exercise 2: AI Business Ideas Generator

This script utilizes the OpenAI GPT-4 model to generate a list of business ideas based on AI technologies. The Langchain library is used to manage the chat prompt and handle the model's output.

## Requirements

- Python 3.9+
- `langchain`
- `python-dotenv`

## Installation

1. Clone the repository or download the `exercise-2.py` file.
2. Install the required Python packages using pip:
   ```bash
   pip install langchain python-dotenv
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
    python exercise-2.py
    ```
2. The script will generate 5 business ideas based on AI technologies and save them to a file named ai_business_ideas.txt.