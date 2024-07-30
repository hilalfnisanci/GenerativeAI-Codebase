from openai import OpenAI
import os
import streamlit as st
import time

# Set up OpenAI client with API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# -----------------------------------------------
# Check for Existing Assistants
# -----------------------------------------------

def check_assistant():
    # Retrieve the list of existing assistants
    existing_assistants = client.beta.assistants.list()
    desired_assistant_name = 'Nicholas Mark Hair Salon Assistant'
    
    # Look for the assistant with the desired name
    for assistant in existing_assistants.data:
        if assistant.name == desired_assistant_name:
            return assistant.id
    
    # Return False if no assistant is found
    return False

# -----------------------------------------------
# Get Tool Outputs from the Run
# -----------------------------------------------

def get_tool_outputs(run):
    tool_outputs = []

    # Extract tool outputs from the run
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

# -----------------------------------------------
# Run the Assistant
# -----------------------------------------------

def run_assistant(assistant_id, user_content):
    # Create a new thread for the conversation
    thread = client.beta.threads.create()
    
    # Send user content to the assistant
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_content,
    )

    # Start the assistant run and poll for status
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, 
        assistant_id=assistant_id
    )

    while True:
        time.sleep(5)

        # Retrieve the run status
        run_status = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )

        # If the run is completed, get messages from the assistant
        if run_status.status == 'completed': 
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )

            for msg in messages.data:
                role = msg.role
                content = msg.content[0].text.value
                if role == 'assistant':
                    response = content
                print(f"{role.capitalize()}: {content}")

            break
        elif run_status.status == 'requires_action':
            print("Function calling!")
            tool_outputs = get_tool_outputs(run)
            
            print(f'\nTool Outputs\n{tool_outputs}\n\n')
            print("Submitting outputs back to the Assistant...")

            # Submit tool outputs back to the assistant
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        else:
            print("Waiting for the Assistant to process...")
            time.sleep(5)
        
        print("\n\nRun status: ", run.status)

    return response

# -----------------------------------------------
# Streamlit Application
# -----------------------------------------------

def streamlit_app(assistant_id):
    st.title("Nicholas Mark Hair Salon Assistant")
    st.write("Please ask your question")

    # User input and sending request
    user_input = st.text_input("Q:")
    if st.button("Send"):
        response = run_assistant(assistant_id=assistant_id, user_content=user_input)
        st.write(response)

# Check if the assistant exists and run the Streamlit app
if not check_assistant() == False:
    assistant_id = check_assistant()
    streamlit_app(assistant_id=assistant_id)
else:
    print("Couldn't find assistant!")
