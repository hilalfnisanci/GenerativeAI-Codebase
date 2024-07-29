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

# Define the system message for the AI assistant
system = """
You are an AI assistant helping people.
Your task is to generate the requested number of business ideas based on AI technologies.
List each business idea clearly and add understandable explanations for each.
"""

# Create a prompt template for the chat model
prompt = ChatPromptTemplate.from_messages([
    ("system", system),
    ("human", "{user_prompt}"),
])

# Initialize the output parser
output_parser = StrOutputParser()

# Create a chain that connects the prompt, model, and output parser
chain = prompt | model | output_parser

# Define a user prompt
user_prompt = "Can you generate 5 business ideas based on AI technologies?"

# Invoke the chain with the user prompt and get the response
response = chain.invoke({"user_prompt": user_prompt})

# Split the response into individual business ideas
business_ideas = response.split('\n')

# Structure the business ideas into a list
structured_ideas = []
for i, idea in enumerate(business_ideas):
    if idea.strip():
        structured_ideas.append(f"{idea.strip()}")

# Print each structured business idea
for idea in structured_ideas:
    print(idea)

# Write the structured business ideas to a text file
with open('ai_business_ideas.txt', 'w') as file:
    for idea in structured_ideas:
        file.write(f"{idea}\n")