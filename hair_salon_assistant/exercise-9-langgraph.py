import os
import random
import pprint
from langchain_core.tools import tool
from typing import Annotated, Sequence, TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.messages import (BaseMessage, ToolMessage,)
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.tools.retriever import create_retriever_tool
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from langgraph.graph import END, StateGraph, START
from IPython.display import Image, display
from langgraph.prebuilt import ToolNode
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.prebuilt import tools_condition


openai_api_key = os.getenv('OPENAI_API_KEY')

# -----------------------------------------------
# Load pdf file
# -----------------------------------------------

def pdf_loader():
    """
    Loads a PDF file, splits its content into chunks, and creates a Chroma vectorstore retriever.
    
    Returns:
        retriever: A retriever for the PDF document.
    """

    pdf_path = "./information_pdf.pdf"

    loader = PyPDFLoader(pdf_path)
    data = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=250,
            chunk_overlap=0,
    )

    chunks = text_splitter.split_documents(data)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        collection_name="rag-chroma",
        embedding= OpenAIEmbeddings()
    )
    retriever = vectorstore.as_retriever()

    return retriever

# -----------------------------------------------
# Define Tools
# -----------------------------------------------

retriever = pdf_loader()

retriever_tool = create_retriever_tool(
    retriever,
    "retrieve_information",
    "Search and return information from Nicholas Mark Hair Salon's PDF document."
)

# Create Appointment Tool
@tool
def create_appointment(service_name: str, customer_name: str, phone_number: str, appointment_date: str) -> str:

    """
    Creates an appointment for a given service and customer.

    Args:
        service_name (str): The name of the service for which the appointment is being made.
        customer_name (str): The name of the customer requesting the appointment.
        phone_number (str): The phone number of the customer.
        appointment_date (str): The desired date for the appointment.

    Returns:
        str: A message indicating whether the appointment was successfully created or if the date is unavailable.
    """

    # Check informations
    if not service_name or not customer_name or not phone_number or not appointment_date:
        return "Missing information. Please provide all details."
    
    # Create fake appointment
    if random.choice([True, False]):
        return f"Your appointment on {appointment_date} for {service_name} has been successfully created. Thank you, {customer_name}!"
    else:
        return "We are not available on the specified date. Please choose another date."

# Create Contact Tool
@tool
def send_contact_message(customer_name: str, phone_number: str, message: str) -> str:
    """
    Sends a message to a customer.

    Args:
        customer_name (str): The name of the customer receiving the message.
        phone_number (str): The phone number of the customer.
        message (str): The message to be sent to the customer.

    Returns:
        str: A message indicating whether the contact message was successfully sent.
    """

    # check infos
    if not customer_name or not phone_number or not message:
        return "Missing information. Please provide all details."
    
    # send fake message
    return f"Your message has been successfully sent. Thank you, {customer_name}!"


# -----------------------------------------------
# State Class
# -----------------------------------------------

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]

# -----------------------------------------------
# Helper Functions
# -----------------------------------------------

def handle_tool_error(state) -> dict:
    """
    Handles errors that occur during tool execution.

    Args:
        state (dict): The current state of the conversation.

    Returns:
        dict: A response indicating the error.
    """
  
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }

def show_graph(graph):
    """
    Displays the state graph.

    Args:
        graph: The state graph to be displayed.
    """

    filename="graph.png"
    try:
        print("here image")
        graph_image = graph.get_graph(xray=True).draw_mermaid_png()
        
        # Save the image
        with open(filename, "wb") as f:
            f.write(graph_image)
        
        # Display the image
        display(Image(filename))
        display(Image(graph.get_graph(xray=True).draw_mermaid_png()))
        print("OK!")
    except Exception as e:
        # This requires some extra dependencies and is optional
        print(f"Error: {e}")
        pass

def greet_user():
    """
    Greets the user.

    Returns:
        str: A greeting message.
    """

    return "Merhaba! Bu, Nicholas Mark Hair Salon için bir AI asistanıdır. Size nasıl yardımcı olabilirim?"

def say_goodbye():
    """
    Says goodbye to the user.

    Returns:
        str: A goodbye message.
    """

    return "Görüşmek üzere! Nicholas Mark Hair Salon'u tercih ettiğiniz için teşekkür ederiz."

def handle_user_input(user_input):
    """
    Handles the user's input and generates responses.

    Args:
        user_input (str): The user's input message.

    Returns:
        list: A list of responses from the assistant.
    """

    inputs = {
        "messages": [
            ("user", user_input),
        ]
    }
    responses = []
    for output in graph.stream(inputs):
        for key, value in output.items():
            responses.append(f"Output from node '{key}': {value}")
    return responses

# -----------------------------------------------
# Nodes
# -----------------------------------------------

tools = [create_appointment, send_contact_message, retriever_tool]

def agent(state):
    """
    Defines the agent's behavior.

    Args:
        state (dict): The current state of the conversation.

    Returns:
        dict: The agent's response.
    """

    messages = state["messages"]

    llm = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0, streaming=True)

    agent_instructions = """You are a multi-language customer support assistant for Nicholas Mark Hair Salon. \
    You assist customers with booking appointments, obtaining information, and answering other questions in their own language. 

        Please follow these guidelines:

        1 - You will always respond to the user in the language they use to write their message. 

        2 - Greeting and Introduction:
        - Greet the user and introduce yourself in the initial conversation.
        - Inform the user that this assistant is an AI.

        3 - Booking Appointments and Communication:
        - When the user wants to book an appointment or wants to communication, collect the informations.
        - If any information is missing, ask the user to provide the missing details.

        4 - Providing Information:
        - When the user asks for information, use the information file to provide answers.
        - Provide short and concise answers and ensure that your responses do not exceed 500 characters.
        
        5 - Complaint Handling:
        - When the user reports a complaint or issue, respond empathetically and provide a reassuring message.
        
        6 - Farewell:
        - At the end of the conversation, thank the user and say goodbye politely.

        7 - Error Messages:
        - If the assistant does not understand something or there is an issue, acknowledge it politely and \
    ask the user to clarify or rephrase their question.

        8 - Note that we only provide services for human clients. We do not offer grooming or other services for pets.
        """
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", agent_instructions),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    prompt = prompt.partial(name="Nicholas Mark Hair Salon Assistant")
    agent = prompt | llm.bind_tools(tools)
    response = agent.invoke(messages)
    return {"messages": [response]}

def create_tool_node_with_fallback(tools: list) -> dict:
    """
    Creates a ToolNode with fallback mechanisms.

    Args:
        tools (list): A list of tools to be included in the ToolNode.

    Returns:
        dict: A ToolNode with fallback mechanisms.
    """

    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )

graph_builder = StateGraph(AgentState)

graph_builder.add_node("agent", agent)
graph_builder.add_node("tools", create_tool_node_with_fallback(tools))

graph_builder.add_edge(START, "agent")

graph_builder.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        END: END,
    },
)
graph_builder.add_edge("tools", "agent")

graph = graph_builder.compile()

show_graph(graph=graph)

def main():
    """
    Main function to run the assistant.
    """

    print(greet_user())
    while True:
        user_input = input("Siz: ")
        if user_input.lower() in ["exit", "quit", "çıkış", "q"]:
            print(say_goodbye())
            break
        responses = handle_user_input(user_input)
        for response in responses:
            pprint.pprint(response)

if __name__ == "__main__":
    main()