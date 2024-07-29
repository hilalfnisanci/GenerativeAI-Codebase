# Exercise 9: Hair Salon Assistant

This project demonstrates a customer support assistant for Nicholas Mark Hair Salon. It includes functionalities for appointment booking, sending contact messages, and retrieving information from a PDF document. The system uses OpenAI's API for language processing and various tools for handling customer interactions.

## Files
- `exercise-9.py`: Initializes the OpenAI assistant with specific instructions and tools, and provides functions for appointment creation and message sending.
- `exercise-9-streamlitApp.py`: A Streamlit application to interact with the assistant through a web interface. It checks if the assistant exists and manages user interactions.
- `exercise-9-langgraph.py`: Defines the assistant's behavior using LangChain, including tools for appointment creation, message sending, and PDF document retrieval. It also includes the state graph for managing the conversation flow.
- `information_pdf.pdf`: Contains the information used by the assistant to answer user queries.

## Requirements

- Python 3.9+
- `openai`
- `streamlit`
- `langchain-core`
- `langchain-openai`
- `langchain-community`
- `pypdf`

## Installation

1. Clone the repository or download the `exercise-9` folder.
2. Install the required Python packages using pip:
   ```bash
    pip install openai streamlit langchain-core langchain-openai langchain-community pypdf
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

1. Initialize the Assistant:

    Run `exercise-9.py` to create and configure the OpenAI assistant with tools for appointment management and contact messaging.
    ```bash
    python exercise-9.py
    ```

2. Streamlit Application:

    Start the Streamlit application using `exercise-9-streamlitApp.py`. This will open a web interface where users can interact with the assistant.
    ```bash
    streamlit run exercise-9-streamlitApp.py
    ```

3. LangChain Integration:

    Run `exercise-9-langgraph.py` to utilize LangChain for defining the assistant's behavior, handling user inputs, and managing conversation flow.
    ```bash
    python exercise-9-langgraph.py
    ```

## Scripts

1. `exercise-9.py`

    This script initializes the OpenAI assistant with tools for handling appointments and contact messages. It performs the following tasks:

    - API Key Setup: Loads the OpenAI API key from environment variables.
    - Tool Functions: Defines functions for creating appointments and sending contact messages, simulating success or failure.
    - Assistant Creation: Configures the assistant with instructions, tools, and the information PDF.
    - Run Function: Manages the conversation with the assistant, handling responses and tool outputs.

2. `exercise-9-streamlitApp.py`

    This script sets up a Streamlit application for interacting with the assistant:

    - API Key Setup: Configures the OpenAI client with the API key.
    - Assistant Check: Verifies if the assistant exists.
    - Run Assistant: Manages conversation with the assistant and handles responses.
    - Streamlit Interface: Provides a user interface for inputting questions and receiving responses from the assistant.

3. `exercise-9-langgraph.py`

    This script defines the assistant's behavior using LangChain:

    - PDF Loading: Loads and processes the PDF document to create a Chroma vectorstore retriever.
    - Tool Definitions: Implements tools for creating appointments and sending contact messages.
    - State Management: Uses LangChain to manage conversation flow and handle user inputs.
    - Graph Visualization: Builds and displays the state graph for the assistant's behavior.

## Notes
- Ensure that the PDF document (information_pdf.pdf) is available in the same directory as the scripts.

- The assistant is designed to respond in the language of the user's input and handle various customer interactions.