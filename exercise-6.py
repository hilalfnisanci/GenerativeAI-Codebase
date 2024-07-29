# Import required libraries and modules
import os
import json
import requests
import streamlit as st
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain

# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the ChatOpenAI model with the API key and specify the GPT-4 model
model = ChatOpenAI(api_key=api_key, model='gpt-4o')

# Initialize the output parsers
output_parser = StrOutputParser()
story_parser = JsonOutputParser()

# -----------------------------------------------
# Article Summarizer
# -----------------------------------------------

# Define the system message for summarizing articles
summarizer_system = """
You are an AI assistant that summarizes articles found on the internet. 
Write a brief summary of the given article.
Article:\n\n"{context}"
"""

# Create a prompt template for summarizing articles
summarizer_prompt = ChatPromptTemplate.from_messages([
    ("system", summarizer_system),
])

# Create a chain for summarizing documents
stuff_chain = create_stuff_documents_chain(llm=model, prompt=summarizer_prompt)

# Function to fetch the content of an article from a given URL
def fetch_article_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract and return the text content from all paragraphs
    article_content = ' '.join(p.get_text() for p in soup.find_all('p'))
    return article_content

# Function to summarize an article given its URL
def summarize_article(url):
    content = fetch_article_content(url)
    doc = Document(page_content=content)
    docs = [doc]
    summary = stuff_chain.invoke({"context": docs})
    return summary

# Streamlit app for displaying article summarizer
def display_article_summarizer():
    st.header("Article Summarizer")
    with st.form(key='summarize_form'):
        url = st.text_input("Enter the URL of the article you want to summarize:")
        submit_button = st.form_submit_button(label='Summarize')
    if submit_button:
        if url:
            try:
                summary = summarize_article(url)
                st.markdown(f"## Summary\n**URL:** {url}\n\n{summary}")
            except Exception as e:
                st.error(f"Error processing the URL: {e}")
        else:
            st.error("Please enter a valid URL.")

# -----------------------------------------------
# Story Generator
# -----------------------------------------------

# Define the system message for generating story ideas
idea_system = """
You are an AI assistant that generates ideas for children's stories. You should generate 5 story ideas suitable for children based on the given topic. The ideas should be fun and appropriate for kids. The ideas should be formatted as a JSON list.
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
You are an AI assistant that writes stories for children. Based on the story idea, you should write an engaging and interesting story for children.
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
    ideas = story_parser.parse(response)
    ideas_json = json.dumps({"ideas": [idea['idea'] for idea in ideas]})
    return ideas_json

# Function to develop a story based on a story idea
def develop_story(story_idea):
    response = story_chain.invoke({"story_idea": story_idea})
    return response.strip()

# Streamlit app for displaying story creation
def display_story_creation():
    st.header("Story Creation with AI Model Chaining")
    with st.form(key='story_ideas_form'):
        topic = st.text_input("Enter a topic for a children's story:")
        ideas_button = st.form_submit_button(label='Generate Story Ideas')
    if ideas_button:
        if topic:
            try:
                ideas_json = generate_story_ideas(topic)
                st.session_state.ideas = json.loads(ideas_json)["ideas"]
                for i, idea in enumerate(st.session_state.ideas):
                    st.write(f"{idea}")
            except Exception as e:
                st.error(f"Error generating story ideas: {e}")
        else:
            st.error("Please enter a valid topic.")
    if st.session_state.ideas:
        with st.form(key='develop_story_form'):
            choice = st.number_input("Enter the number of the story idea you want to develop:", min_value=1, max_value=5, step=1)
            develop_button = st.form_submit_button(label='Develop Story')
            if develop_button:
                if choice > 0 and choice <= len(st.session_state.ideas):
                    st.session_state.selected_idea = st.session_state.ideas[choice-1]
                    st.write(f"Developing story for idea: {st.session_state.selected_idea}")
                    story = develop_story(st.session_state.selected_idea)
                    st.markdown(f"##### Topic:\n{topic}\n\n##### Chosen Story Idea:\n{st.session_state.selected_idea}\n\n##### Full Story:\n{story}")
                else:
                    st.warning("Please select a valid story idea number.")

# Main function to run the Streamlit app
def main():
    # Initialize session state variables if they do not exist
    if 'ideas' not in st.session_state:
        st.session_state.ideas = []
    if 'selected_idea' not in st.session_state:
        st.session_state.selected_idea = ""

    st.title("Streamlit Exercises")

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ["Article Summarizer", "Story Creation"])

    if selection == "Article Summarizer":
        display_article_summarizer()
    elif selection == "Story Creation":
        display_story_creation()

# Run the Streamlit app
if __name__ == "__main__":
    main()

# To run it, you can type "streamlit run exercise-7.py" into the terminal.