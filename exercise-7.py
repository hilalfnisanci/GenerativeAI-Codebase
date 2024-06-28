import os
import requests
from bs4 import BeautifulSoup
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.schema import Document
from langchain_core.output_parsers import JsonOutputParser
import json
import streamlit as st

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

summarizer_prompt_template = """Write a concise summary of the following:
"{content}"
CONCISE SUMMARY:"""
summarizer_prompt = PromptTemplate.from_template(summarizer_prompt_template)
summarizer_llm = ChatOpenAI()
summarizer_llm_chain = LLMChain(prompt=summarizer_prompt, llm=summarizer_llm)
summarizer_stuff_chain = StuffDocumentsChain(
    llm_chain=summarizer_llm_chain,
    document_variable_name="content"
)

story_idea_prompt_template = """
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
story_idea_prompt = PromptTemplate.from_template(story_idea_prompt_template)

story_detail_prompt_template = """
You are an AI assistant for creating children's stories. Based on the story idea provided, write a detailed and engaging story for children.
Story Idea: "{story_idea}"
Full Story:
"""
story_detail_prompt = PromptTemplate.from_template(story_detail_prompt_template)

story_llm = ChatOpenAI()
idea_chain = LLMChain(prompt=story_idea_prompt, llm=story_llm)
story_chain = LLMChain(prompt=story_detail_prompt, llm=story_llm)

story_parser = JsonOutputParser()

def fetch_article_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    article_content = ' '.join(p.get_text() for p in soup.find_all('p'))
    return article_content

def summarize_article(url):
    content = fetch_article_content(url)
    doc = Document(page_content=content)
    docs = [doc]
    summary = summarizer_stuff_chain.run(docs)
    return summary

def generate_story_ideas(topic):
    response = idea_chain.run({"topic": topic})
    ideas = story_parser.parse(response)
    ideas_json = json.dumps({"ideas": [idea['idea'] for idea in ideas]})
    return ideas_json

def develop_story(story_idea):
    response = story_chain.run({"story_idea": story_idea})
    return response.strip()

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

def main():
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

if __name__ == "__main__":
    main()
