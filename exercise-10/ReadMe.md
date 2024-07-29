# Exercise 10: Langsmith Dataset Creation and Evaluation

This exercise involves creating a dataset for the Nicholas Mark Hair Salon AI assistant and evaluating its performance.

## Files

- `create-langsmith-dataset.py`: This script is responsible for creating a dataset of question-answer pairs and uploading it to Langsmith.

- `evaluator.py`: This script evaluates the performance of the AI assistant by comparing its responses to the reference answers. It performs the following tasks:

## Requirements

- Python 3.9+
- `pandas`
- `langsmith`
- `openai`
- `langchain`

## Installation

1. Clone the repository or download the `exercise-10` folder.
2. Install the required Python packages using pip:
   ```bash
    pip install pandas langsmith openai langchain
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
First, you need to run create-langsmith-dataset.py to create the dataset on LangSmith. Then, you should run evaluator.py to evaluate the model using this dataset.

1. `create-langsmith-dataset.py`
- Update the csv_path variable with the desired path for saving the CSV file.
- Run the script to create the dataset and upload it to Langsmith.
    ```bash
    python create-langsmith-dataset.py
    ```

2. `evaluator.py`
- Ensure that the OPENAI_API_KEY environment variable is set.
- Run the script to evaluate the AI assistant's responses.
    ```bash
    python evaluator.py
    ```

## Scripts

1. `create-langsmith-dataset.py`

- Defines a set of question-answer pairs related to the Nicholas Mark Hair Salon.
- Converts these pairs into a Pandas DataFrame.
- Saves the DataFrame as a CSV file.
- Uses the Langsmith client to create a dataset and upload the examples.

2. `evaluator.py`

- Defines a list of inputs (questions) for evaluation.
- Implements functions to interact with the Langsmith client, retrieve tool outputs, and evaluate responses.
- Uses OpenAI's GPT-3.5-turbo to evaluate the responses against reference answers.
- Prints evaluation scores and notes.

## Additional Information

- Ensure that you have access to Langsmith and have created the appropriate account and dataset.
- Modify the dataset path and OpenAI API key in the scripts as needed for your environment.