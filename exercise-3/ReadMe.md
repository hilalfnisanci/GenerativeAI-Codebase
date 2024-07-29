# Exercise 3: Sentiment Analysis on Product Reviews

This script performs sentiment analysis on a list of product reviews using the OpenAI GPT-4 model. It classifies each review as "positive", "negative", or "neutral" and saves the results to a CSV file.

## Requirements

- Python 3.9+
- `pandas`
- `langchain`
- `python-dotenv`

## Installation

1. Clone the repository or download the `exercise-3.py` file.
2. Install the required Python packages using pip:
   ```bash
    pip install pandas langchain python-dotenv
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
    python exercise-3.py
    ```
2. The script will analyze the sentiment of each review and save the results to a file named sentiment_analysis_results.csv.

