# Exercise 5: Children's Story Generator

This script generates and develops children's story ideas based on a given topic using the OpenAI GPT-4 model. The script first generates a list of story ideas and then develops a full story based on a selected idea. The results are printed and saved to a text file.

## Requirements

- Python 3.9+
- `langchain`
- `python-dotenv`

## Installation

1. Clone the repository or download the `exercise-5.py` file.
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
    python exercise-5.py
    ```
2. Enter a topic for the children's story when prompted.
3. The script will generate and display 5 story ideas based on the given topic.
4. Select a story idea by entering its number.
5. The script will develop the chosen story and print the topic, chosen story idea, and full story.
6. The results will be saved to a file named children_story.txt.

