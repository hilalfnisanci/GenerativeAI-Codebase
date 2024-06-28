import os
import requests
from bs4 import BeautifulSoup
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.schema import Document

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

prompt_template = """Write a concise summary of the following:
"{content}"
CONCISE SUMMARY:"""
prompt = PromptTemplate.from_template(prompt_template)

llm = ChatOpenAI()

llm_chain = LLMChain(prompt=prompt, llm=llm)
stuff_chain = StuffDocumentsChain(
    llm_chain=llm_chain, 
    document_variable_name="content"
  )

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
    summary = stuff_chain.run(docs)
    return summary

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

if __name__ == "__main__":
    main()