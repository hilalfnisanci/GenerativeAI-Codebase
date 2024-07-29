# Import required libraries and modules
import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser

# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the ChatOpenAI model with the API key and specify the GPT-4 model
model = ChatOpenAI(api_key=api_key, model='gpt-4o')

# Initialize the output parsers
output_parser = StrOutputParser()
parser = JsonOutputParser()

# Define the system message for generating story ideas
idea_system = """
You are an AI assistant that generates ideas for children's stories. You should generate 5 story ideas that are suitable and fun for children. The ideas should be formatted as a JSON list.
For example;
Topic: "{topic}"
Story Ideas:
[
{"idea": "1. "}, 
{"idea": "2. "}, 
{"idea": "3. "}, 
{"idea": "4. "}, 
{"idea": "5. "}
]
"""

# Create a prompt template for generating story ideas
idea_prompt = ChatPromptTemplate.from_messages([
    ("system", idea_system),
    ("human", "{topic}")
])

# Create a chain for generating story ideas
idea_chain = idea_prompt | model | output_parser

# Define the system message for developing a story
story_system = """
You are an AI assistant that creates stories for children. Based on the story idea, you should write an engaging and interesting story for children.
For example;
Story Idea: "{story_idea}"
Full Story:
"""

# Create a prompt template for developing a story
story_prompt = ChatPromptTemplate.from_messages([
    ("system", story_system)
])

# Create a chain for developing a story
story_chain = story_prompt | model | output_parser

# Function to generate story ideas based on a topic
def generate_story_ideas(topic):
    response = idea_chain.invoke({"topic": topic})
    ideas = parser.parse(response)
    ideas_json = json.dumps({"ideas": [idea['idea'] for idea in ideas]})
    return ideas_json

# Function to develop a story based on a story idea
def develop_story(story_idea):
    response = story_chain.invoke({"story_idea": story_idea})
    return response.strip()

# Main function to interact with the user and generate a story
def main():
    # Get the topic from the user
    topic = input("Enter a topic for a children's story: ")

    # Generate story ideas based on the topic
    print("\nGenerating story ideas...\n")
    ideas_json = generate_story_ideas(topic)
    ideas = json.loads(ideas_json)["ideas"]
    
    # Print the generated story ideas
    for i, idea in enumerate(ideas):
        print(f"{idea}")

    # Get the user's choice for the story idea to develop
    choice = int(input("\nEnter the number of the story idea you want to develop: ")) - 1
    selected_idea = ideas[choice]

    # Develop the chosen story
    print("\nDeveloping the story...\n")
    story = develop_story(selected_idea)

    # Print and save the topic, chosen story idea, and full story
    print("\nTopic:", topic)
    print("\nChosen Story Idea:", selected_idea)
    print("\nFull Story:\n", story)

    with open("children_story.txt", "w") as file:
        file.write(f"Topic: {topic}\n")
        file.write(f"Chosen Story Idea: {selected_idea}\n")
        file.write(f"Full Story:\n{story}\n")

# Execute the main function when the script is run
if __name__ == "__main__":
    main()