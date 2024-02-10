# %%
import pandas as pd
import json
import openai
import requests
from config import config
from openai import OpenAI
import time
from dotenv import load_dotenv
load_dotenv()
import os
folder_path = 'files'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

INSTRUCTION = config.INSTRUCTION
F_NAME = config.F_NAME
GPT_MODEL = config.GPT_MODEL

INPUT_CSV_PATH = config.questions
OUTPUT_CSV_PATH = config.gpt4results_csv_path

client = OpenAI()
def show_json(obj):
    print(json.loads(obj.model_dump_json()))

assistant = client.beta.assistants.create(
    name=f"{F_NAME} AI Evaluator",
    instructions=INSTRUCTION,
    model=GPT_MODEL,
)
show_json(assistant)

# Utility functions
def read_csv(file_path):
    return pd.read_excel(file_path)

def process_data_for_gpt(data):
    prompts = []
    for _, row in data.iterrows():
        question = row['Question']
        prompt = f"Please answer the following question in detail, accurately, exactly as asked:\n\n{question}"
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
        new_rows.append({'Model': model_name, 'Question': question, 'Response': response, 'Latency': latency})
    new_data = pd.DataFrame(new_rows)
    new_data.to_excel(interim_csv_path, index=False)

data = read_csv(INPUT_CSV_PATH)
prompts = process_data_for_gpt(data)
ASSISTANT_ID = assistant.id

responses = []
latencies = []  # Initialize a list to store latencies

for prompt in prompts:
    start_time = time.time()  # Capture start time
    run, thread = submit_message_and_create_run(ASSISTANT_ID, prompt)
    response = wait_on_run_and_get_response(run, thread)
    end_time = time.time()  # Capture end time
    latency = end_time - start_time  # Calculate latency
    latencies.append(latency)  # Store latency
    if isinstance(response, list):
        response = ' '.join(map(str, response))
    response = response.replace("\\\\n", "\\n")
    response = response.strip()
    print(response)
    responses.append(response)

create_output_csv(data, responses, latencies, GPT_MODEL, OUTPUT_CSV_PATH)




