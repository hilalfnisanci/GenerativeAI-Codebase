# Import required libraries and modules
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain.schema import Document
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain

# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the ChatOpenAI model with the API key and specify the GPT-4 model
model = ChatOpenAI(api_key=api_key, model='gpt-4o')

# Initialize the output parser
output_parser = StrOutputParser()

# Define the system message for the AI assistant
system = """
You are an AI assistant that summarizes articles found on the internet.
Write a brief summary of the given article.
Article:\n\n"{context}"
"""

# Create a prompt template for the chat model
prompt = ChatPromptTemplate.from_messages([
    ("system", system),
])

# Create a chain that combines documents with the model and prompt
stuff_chain = create_stuff_documents_chain(llm=model, prompt=prompt)

# Function to fetch the content of an article from a given URL
def fetch_article_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract text from all <p> tags
    article_content = ' '.join(p.get_text() for p in soup.find_all('p'))
    return article_content

# Function to summarize an article from a given URL
def summarize_article(url):
    content = fetch_article_content(url)
    doc = Document(page_content=content)
    docs = [doc]
    summary = stuff_chain.invoke({"context": docs})
    return summary

# Main function to process a list of article URLs
def main():
    urls = [
        'https://jeos.edpsciences.org/articles/jeos/full_html/2024/01/jeos20230044/jeos20230044.html'
    ]
    
    for url in urls:
        try:
            summary = summarize_article(url)
            print(f"URL: {url}\nSummary: {summary}\n")
        except Exception as e:
            print(f"Error processing {url}: {e}")

# Execute the main function when the script is run
if __name__ == "__main__":
    main()