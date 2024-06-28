import os
import json
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Updated prompt to enforce JSON output
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

# Define a function to parse JSON output
parser = JsonOutputParser()

def generate_story_ideas(topic):
    response = idea_chain.run({"topic": topic})
    # print("Raw JSON response:", response)
    ideas = parser.parse(response)
    ideas_json = json.dumps({"ideas": [idea['idea'] for idea in ideas]})
    return ideas_json

def develop_story(story_idea):
    response = story_chain.run({"story_idea": story_idea})
    return response.strip()

def main():
    topic = input("Enter a topic for a children's story: ")

    print("\nGenerating story ideas...\n")
    ideas_json = generate_story_ideas(topic)
    ideas = json.loads(ideas_json)["ideas"]
    for i, idea in enumerate(ideas):
        print(f"{idea}")

    choice = int(input("\nEnter the number of the story idea you want to develop: ")) - 1
    selected_idea = ideas[choice]

    print("\nDeveloping the story...\n")
    story = develop_story(selected_idea)

    print("\nTopic:", topic)
    print("\nChosen Story Idea:", selected_idea)
    print("\nFull Story:\n", story)

    with open("children_story.txt", "w") as file:
        file.write(f"Topic: {topic}\n")
        file.write(f"Chosen Story Idea: {selected_idea}\n")
        file.write(f"Full Story:\n{story}\n")

if __name__ == "__main__":
    main()