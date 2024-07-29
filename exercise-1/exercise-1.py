# Import required libraries and modules
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the ChatOpenAI model with the API key and specify the GPT-4 model
model = ChatOpenAI(api_key=api_key, model='gpt-4o')

# Create a prompt template for the chat model
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a knowledgeable AI assistant. Your task is to answer questions about the latest developments in artificial intelligence."),
    ("human", "{user_prompt}"),
])

# Initialize the output parser
output_parser = StrOutputParser()

# Create a chain that connects the prompt, model, and output parser
chain = prompt | model | output_parser

# Define a user prompt
user_prompt = "Can you provide a summary of the latest advancements in artificial intelligence as of 2024?"

# Invoke the chain with the user prompt and get the response
response = chain.invoke({"user_prompt": user_prompt})

# Print the response
print(response)

# Write the response to a text file
with open('ai_advancements_summary.txt', 'w') as file:
    file.write(response)