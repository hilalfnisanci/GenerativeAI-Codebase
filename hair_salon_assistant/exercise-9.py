import os
import random
from openai import OpenAI

# Load API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# -----------------------------------------------
# Create Tools (fake)
# -----------------------------------------------

# Function to create a fake appointment
def create_appointment(service_name, customer_name, phone_number, appointment_date):
    # Check if all information is provided
    if not service_name or not customer_name or not phone_number or not appointment_date:
        return "Missing information. Please provide all details."
    
    # Randomly decide if the appointment is successful or not
    if random.choice([True, False]):
        return f"Your appointment on {appointment_date} for {service_name} has been successfully created. Thank you, {customer_name}!"
    else:
        return "We are not available on the specified date. Please choose another date."

# Function to send a fake contact message
def send_contact_message(customer_name, phone_number, message):
    # Check if all information is provided
    if not customer_name or not phone_number or not message:
        return "Missing information. Please provide all details."
    
    # Simulate sending the message
    return f"Your message has been successfully sent. Thank you, {customer_name}!"

# -----------------------------------------------
# Create Assistant
# -----------------------------------------------

def create_assistant():

    # Define the assistant's instructions
    instructions = """You are a multi-language customer support assistant for Nicholas Mark Hair Salon. \
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

    # Create a vector store for the assistant
    vector_store = client.beta.vector_stores.create(name="Nicholas Mark Hairdressing")

    # Upload information files to the vector store
    file_paths = ["./information_pdf.pdf"]
    file_streams = [open(path, "rb") for path in file_paths]

    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    # Create the assistant with the specified tools and instructions
    assistant = client.beta.assistants.create(
        name="Nicholas Mark Hair Salon Assistant",
        instructions=instructions,
        tools=[
            {"type": "function",
                "function" : {
                    "name": "create_appointment",
                    "description": "Creates an appointment for a given service and customer.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "service_name": {"type": "string"},
                            "customer_name": {"type": "string"},
                            "phone_number": {"type": "string"},
                            "appointment_date": {"type": "string"}
                        },
                        "required": ["service_name", "customer_name", "phone_number", "appointment_date"]
                    }
                }
            },
            {"type" : "function",
                "function" :{
                    "name": "send_contact_message",
                    "description": "Sends a message to a customer.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "customer_name": {"type": "string"},
                            "phone_number": {"type": "string"},
                            "message": {"type": "string"}
                        },
                        "required": ["customer_name", "phone_number", "message"]
                    }
                }
            },
            {"type" : "file_search"}
        ],
        model="gpt-3.5-turbo-0125",
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    return assistant


# -----------------------------------------------
# Create Run
# -----------------------------------------------

def run_assistant(assistant_id, user_content):
    # Create a new conversation thread
    thread = client.beta.threads.create()

    # Send the user's message to the assistant
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_content,
    )

    # Execute the assistant's run and wait for the result
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, 
        assistant_id=assistant_id
    )

    # If the run is completed, return the messages
    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        return messages
    else:
        return run.status

# Create the assistant
create_assistant()