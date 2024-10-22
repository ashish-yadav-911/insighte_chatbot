from openai import OpenAI

from dotenv import load_dotenv
import os, time, json, shelve #,logging
from dotenv import find_dotenv, load_dotenv
from datetime import datetime
from flask import Flask, render_template, request, jsonify

load_dotenv()
#OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))


# def create_assistant():

#     assistant = client.beta.assistants.create(
#         name="insighte_demo_001",
        
#         instructions="""
        
" |||| PROMPT MISSING  ||||"
        
#         """,
        
#         model="gpt-4o-mini"

#     )
#     return assistant

# assistant = create_assistant()

# print("Assistant ID: ", assistant.id)

# #      === Thread (uncomment this to create your Thread) ===
# thread = client.beta.threads.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "Hello?",
#         }
#     ]
# )
# thread_id = thread.id
# print("Thread ID",thread_id)


app = Flask(__name__)


# === Hardcode our ids ===
assistant_id = os.getenv('assistant_id')
thread_id = os.getenv('thread_id')


def run_assistant(thread,assist):
    #asistant_id = "asst_vpJaoIF25w4IlhVTC2Rwmwhy"
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve(assist)

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread,
        assistant_id=assist,
    )

    # Wait for completion
    while run.status != "completed":
        # Be nice to the API
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread)
    new_message = messages.data[0].content[0].text.value
    print(f"{new_message}")
    return new_message


@app.route('/')
def home():
    return render_template('index.html')
@app.route('/chat', methods=['POST'])
def generate_response():
    assist = os.getenv('assistant_id')
    data = request.json
    user_body = data.get('message')
    print(user_body)
    
    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=user_body,
    )

    # Run the assistant and get the new message
    new_message = run_assistant(thread_id,assist)

    return new_message

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",port=4000)