import pandas as pd
import json
import openai
import requests
from openai import OpenAI
import time
from dotenv import load_dotenv
load_dotenv()

GPT_MODEL = "gpt-4-1106-preview"
INPUT_CSV_PATH = 'questions.csv'
OUTPUT_CSV_PATH = 'results_grouped_by_model.csv'

client = OpenAI()
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

INSTRUCTION = config['instructions']

def show_json(obj):
    print(json.loads(obj.model_dump_json()))

assistant = client.beta.assistants.create(
    name="Galen AI Evaluator",
    instructions=INSTRUCTION,
    model=GPT_MODEL,
)
show_json(assistant)

# Utility functions
def read_csv(file_path):
    return pd.read_csv(file_path)

def process_data_for_gpt(data):
    prompts = []
    for _, row in data.iterrows():
        question = row['Question']
        prompt = f"Please answer the following question:\n\n{question}"
        prompts.append(prompt)
    return prompts

def submit_message_and_create_run(assistant_id, prompt):
    thread = client.beta.threads.create() # If you replace this globally it appends all answers to the one before.
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
    return client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id), thread

def wait_on_run_and_get_response(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(0.5)
    messages = client.beta.threads.messages.list(thread_id=thread.id, order="asc")
    return [m.content[0].text.value for m in messages if m.role == 'assistant']

def create_output_csv(data, responses, model_name, interim_csv_path):
    new_rows = []
    for question, response in zip(data['Question'], responses):
        new_rows.append({'Model': model_name, 'Question': question, 'Response': response})

    new_data = pd.DataFrame(new_rows)
    new_data.to_csv(interim_csv_path, index=False)

data = read_csv(INPUT_CSV_PATH)
prompts = process_data_for_gpt(data)
ASSISTANT_ID = assistant.id

responses = []
for prompt in prompts:
    run, thread = submit_message_and_create_run(ASSISTANT_ID, prompt)
    response = wait_on_run_and_get_response(run, thread)
    print(response)
    responses.append(response)

gpt4results_csv_path = 'results_gpt4.csv'
create_output_csv(data, responses, GPT_MODEL, gpt4results_csv_path)

