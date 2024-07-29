from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import fitz  # PyMuPDF
import pandas as pd
import os
import json

openai_api_key = os.getenv("OPENAI_API_KEY")

def extract_faq_from_pdf(pdf_path):
    # Open PDF file
    pdf_document = fitz.open(pdf_path)
    faq_data = []

    # Process each page
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        
        # Extract text by identifying questions and answers
        lines = text.split('\n')
        question = None
        answer_lines = []

        for line in lines:
            line = line.strip()
            if line.endswith('?'):
                if question and answer_lines:
                    answer = ' '.join(answer_lines).strip()
                    faq_data.append({'Question': question, 'Answer': answer})
                question = line
                answer_lines = []
            elif line:  # Skip blank lines
                answer_lines.append(line)
        
        # Adding the latest Q&A
        if question and answer_lines:
            answer = ' '.join(answer_lines).strip()
            faq_data.append({'Question': question, 'Answer': answer})
    
    # Creating a DataFrame
    faq_df = pd.DataFrame(faq_data)
    return faq_df

def get_question_and_answer():
    # Specify the PDF file path
    pdf_path = './FAQ.pdf'
    faq_df = extract_faq_from_pdf(pdf_path)

    # Checking DataFrame
    print(faq_df)

    qa_pairs = []

    for _, row in faq_df.iterrows():
        question = row['Question']
        answer = row['Answer']
        new_qa_pairs = create_dataset(question, answer)
        for new_question, new_answer in new_qa_pairs:
            qa_pairs.append({"question": new_question, "answer": new_answer})

    with open('Nicholas-Mark-Hairdressing-Dataset.json', 'w', encoding='utf-8') as f:
        json.dump(qa_pairs, f, ensure_ascii=False, indent=4)

def create_dataset(question: str, answer: str):

    model = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo-0125')
    system_prompt = """
    You are an assistant that helps generate related questions and answers based on given input. \
    For the provided question and answer, generate 5 new, related question-answer pairs.
        
    Original Question: {question}
    Original Answer: {answer}
        
    Please create 5 related question-answer pairs based on the context and information given in the original pair.
      
    Question: 
    Answer: 

    Question: 
    Answer: 

    Question: 
    Answer: 

    Question: 
    Answer: 

    Question: 
    Answer: 
    """

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
    ])
    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    response = chain.invoke({"question": question, "answer": answer})

    print(f"\nOriginal Question: {question}\nOriginal Answer: {answer}")
    print(f"\nResponse\n{response}\n\n")

    new_qa_pairs = []
    lines = response.split("\n")
    current_question = None
    current_answer = None

    for line in lines:
        if line.startswith("Question:"):
            if current_question and current_answer:
                new_qa_pairs.append((current_question.strip(), current_answer.strip()))
            current_question = line.replace("Question:", "").strip()
            current_answer = None
        elif line.startswith("Answer:"):
            current_answer = line.replace("Answer:", "").strip()
        elif current_answer is not None:
            current_answer += " " + line.strip()

    if current_question and current_answer:
        new_qa_pairs.append((current_question.strip(), current_answer.strip()))

    return new_qa_pairs

get_question_and_answer()