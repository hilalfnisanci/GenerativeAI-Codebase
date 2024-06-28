import os
import json
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langsmith import Client, traceable

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
langsmith_api_key = os.getenv("LANGCHAIN_API_KEY")

langsmith_client = Client(api_key=langsmith_api_key)

idea_prompt_template = """
You are an AI assistant for creating children's stories. Based on the topic provided, generate five different story ideas in the format of a JSON list.
Topic: "{topic}"
Story Ideas:
[
{{"idea": "1. "}}, 
{{"idea": "2. "}}, 
{{"idea": "3. "}}, 
{{"idea": "4. "}}, 
{{"idea": "5. "}}
]
"""
idea_prompt = PromptTemplate.from_template(idea_prompt_template)

story_prompt_template = """
You are an AI assistant for creating children's stories. Based on the story idea provided, write a detailed and engaging story for children.
Story Idea: "{story_idea}"
Full Story:
"""
story_prompt = PromptTemplate.from_template(story_prompt_template)

llm = ChatOpenAI()

idea_chain = LLMChain(prompt=idea_prompt, llm=llm)
story_chain = LLMChain(prompt=story_prompt, llm=llm)

parser = JsonOutputParser()

@traceable
def story_creation():
    topic = input("Enter a topic for a children's story: ")

    print("\nGenerating story ideas...\n")
    ideas_response = idea_chain.run({"topic": topic})
    ideas = parser.parse(ideas_response)
    ideas_list = [idea['idea'] for idea in ideas]

    for i, idea in enumerate(ideas_list):
        print(f"{idea}")

    choice = int(input("\nEnter the number of the story idea you want to develop: ")) - 1
    selected_idea = ideas_list[choice]

    print("\nDeveloping the story...\n")
    story_response = story_chain.run({"story_idea": selected_idea})
    full_story = story_response.strip()

    print("\nTopic:", topic)
    print("\nChosen Story Idea:", selected_idea)
    print("\nFull Story:\n", full_story)

    with open("children_story.txt", "w") as file:
        file.write(f"Topic: {topic}\n")
        file.write(f"Chosen Story Idea: {selected_idea}\n")
        file.write(f"Full Story:\n{full_story}\n")

story_creation()
