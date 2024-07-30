# Fine-Tuning Dataset Preparation

This project contains scripts to create a fine-tuning dataset from a PDF file and convert it into a JSONL file for OpenAI fine-tuning.

## Files

- `create_dataset.py`: Extracts FAQ question-answer pairs from a PDF and generates additional related Q&A pairs using the OpenAI API.
- `create_jsonl_file.py`: Converts the generated JSON file into a JSONL file format required for OpenAI fine-tuning.
- `FAQ.pdf`: The source PDF file containing FAQ data.

## Requirements

- Python 3.9+
- `langchain_openai`
- `fitz` (PyMuPDF)
- `pandas`
- `os`
- `json`

## Installation

1. Clone the repository or download the `fine-tuning` folder.
2. Install the required Python packages using pip:
   ```bash
    pip install langchain-openai PyMuPDF pandas
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

## Steps to Run the Scripts

### 1. Extract FAQ and Create Dataset

- Run `create_dataset.py` to extract question-answer pairs from `FAQ.pdf` and generate additional related Q&A pairs. The output is saved as `Nicholas-Mark-Hairdressing-Dataset.json`.

   ```bash
    python create_dataset.py
    ```

### 2. Convert JSON to JSONL

- Run `create_jsonl_file.py` to convert the generated JSON file into a JSONL file format.

    ```bash
    python create_jsonl_file.py
    ```

### 3. Fine-Tuning the Model

After generating the JSONL file, follow these steps to fine-tune the model:

1. Go to the [OpenAI Platform](https://platform.openai.com/).
2. Log in to your account.
3. Navigate to the Dashboard.
4. Go to the Fine-tuning section.
5. Upload the JSONL file for fine-tuning.
6. Select the base model (e.g., `gpt-3.5-turbo-0125`).
7. Set the following parameters:
   - Epochs (e.g. 7)
   - Multiplier (e.g. 4)
   - Seed (e.g. 4)
   - Batch Size (e.g. Leave as null)

For more detailed instructions, refer to the [OpenAI Fine-Tuning Guide](https://platform.openai.com/docs/guides/fine-tuning).
