from langsmith.evaluation import evaluate
from openai import OpenAI
import os
import time
from langchain.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langsmith.schemas import Example, Run
from langchain_core.output_parsers import StrOutputParser
import re

openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)
model = ChatOpenAI(api_key=openai_api_key, model='gpt-3.5-turbo-0125')

inputs = [
    "What are the salon's opening hours?",
    "Can I get an urgent haircut appointment for today?",
    "I want to file a complaint. I was very dissatisfied with my last haircut and I want a refund.",
    "Can I get information about women's haircut prices?",
    "Which hair care products do you use?",
    "I would like to make an appointment for a haircut.",
    "I lost my wallet in your salon, can I get information about lost and found items?",
    "I want my dog to get a haircut, can I make an appointment for my dog?",
    "Do you dye children's hair?",
    "I was very dissatisfied with the service I received yesterday."
]

inputs=[{"input":q} for q in inputs]

# Check assistant
def check_assistant():
    existing_assistants = client.beta.assistants.list()
    desired_assistant_name = 'Nicholas Mark Hair Salon Assistant'
    for assistant in existing_assistants.data:
        if assistant.name == desired_assistant_name:
            return assistant.id
    return False

# Get Tool Outputs
def get_tool_outputs(run):
    tool_outputs = []

    for tool in run.required_action.submit_tool_outputs.tool_calls:
        if tool.function.name == "create_appointment":
            tool_outputs.append({
                "tool_call_id": tool.id,
                "output": "True"
            })
        elif tool.function.name == "send_contact_message":
            tool_outputs.append({
                "tool_call_id": tool.id,
                "output": "True"
            })
    
    return tool_outputs

# Run Assistant
def run_assistant(user_content):
    print("user content: ", user_content)
    assistant_id = check_assistant()

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_content["input"],
    )

    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, 
        assistant_id=assistant_id
    )

    response = None
    tool_outputs = []

    while True:
        # retrieve the run status
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        # if run is completed get messages
        if run_status.status == 'completed': 
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            for msg in messages.data:
                role = msg.role
                if role == 'assistant':
                    response = msg.content[0].text.value
                    break
            break
        elif run_status.status == 'requires_action':
            print("Function calling!")
            tool_outputs = get_tool_outputs(run)
                
            print(f'\nTool Outputs\n{tool_outputs}\n\n')
            print("Submitting outputs back to the Assistant...")

            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )
        else:
            print("Waiting for the Assistant to process...")
            time.sleep(5)
        print("\n\nrun status: ", run_status.status)

    if response:
        response_data = {'output': response}
    else:
        response_data = {'output': tool_outputs}

    #response_json = json.dumps(response_data)
    return response_data

# Evaluator
dataset_name = "Nicholas-Mark-Hairdressing-Test-Dataset"

def predict(inputs: dict) -> dict:
    response = run_assistant(inputs)
    return response

def evaluate_function_call(prediction: dict, reference: dict) -> dict:
    notes = ""
    score = 0

    if prediction == reference:
        score = 1
        notes = "Correct function call."
    else:
        score = 0
        notes = "Incorrect function call."

    return {"score": score, "notes": notes}

def llm_evaluate_response(prediction: str, reference: str) -> dict:
    system_prompt = """
You are an expert in evaluating the accuracy of AI-generated responses. Evaluate the following responses according to following guideline:

If the predicted answer is completely correct, give it a score of 1. 
If the predicted answer is related to the reference but not entirely correct, give it a score of 0.5.
If the predicted answer is completely incorrect, give it a score of 0.

Here is the data

Here is the reference answer:
{reference}
You are grading the following predicted answer:
{prediction}

Provide a score and detailed notes explaining your evaluation.

Score:

Notes:
"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
    ])

    output_parser = StrOutputParser()

    chain = prompt | model | output_parser

    response = chain.invoke({"reference": reference, "prediction": prediction})

    print(f"\nresponse: {response}\n")

    # Extract score and notes using regex
    score_match = re.search(r'Score:\s*(\d+\.?\d*)', response)
    notes_match = re.search(r'Notes:\s*(.*)', response, re.DOTALL)

    score = float(score_match.group(1)) if score_match else 0
    notes = notes_match.group(1).strip() if notes_match else ""

    # print(f"\nscore: {score}, \nnotes: {notes}")

    return {"score": score, "notes": notes}

def evaluator(run: Run, example: Example) -> dict:
    prediction = run.outputs['output']
    reference = example.outputs['output']

    evaluation_result = llm_evaluate_response(prediction, reference)

    return {"key": "EvaluationScore", "score": evaluation_result['score'], "notes": evaluation_result['notes']}

evaluate(
    predict,
    data=dataset_name,
    evaluators=[evaluator], # Evaluator
    experiment_prefix="Nicholas-Mark-Hairdressing-Eval-gpt-3.5-turbo-0125",
    metadata={"version": "1.0.0"}
)