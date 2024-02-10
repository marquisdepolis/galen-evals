import time
import pandas as pd
import json
import openai
import requests
from config import config
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

INSTRUCTION = config['instructions']
F_NAME = config["name"]
GPT_MODEL = config["GPT_MODEL"]

def show_json(obj):
    print(json.loads(obj.model_dump_json()))

assistant = client.beta.assistants.create(
    name=f"{F_NAME} LLM Evaluator",
    instructions=INSTRUCTION,
    model=GPT_MODEL,
)
show_json(assistant)

def read_csv(file_path):
    return pd.read_excel(file_path)

template = {
 "Model": [
  {"Name": "mistral-7b", "Ranking": ""},
  {"Name": "llama2-70b", "Ranking": ""},
  {"Name": "qwen-14b", "Ranking": ""},
  {"Name": "yi-34b", "Ranking": ""},
  {"Name": "mixtral-instruct", "Ranking": ""},
  {"Name": "falcon-40b", "Ranking": ""},
  {"Name": "gpt-4-1106", "Ranking": ""},
  {"Name": "deepseek_33bq", "Ranking": ""}
 ]
}
def process_data_for_function(data):
    prompts = []
    for _, row in data.iterrows():
        question = row['Question']
        answers = [f"Model {model}: {answer}" for model, answer in row.items() if model != 'Question' and pd.notna(answer)]
        prompt = (f"{INSTRUCTION} Please read the following question and the replies from different Models. Then I need you to give a ranking like \n {template}. \n Add a very short succinct summary sentence at the end about overall impressions and pros/cons.\n\nQuestion: {question}\n" + "\n".join(answers))
        prompts.append(prompt)
    return prompts

def submit_message_and_create_run(assistant_id, prompt):
    thread = client.beta.threads.create()
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=prompt)
    return client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id), thread

def wait_on_run_and_get_response(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        time.sleep(0.5)
    messages = client.beta.threads.messages.list(thread_id=thread.id, order="asc")
    return [m.content[0].text.value for m in messages if m.role == 'assistant']

def write_responses_to_csv(responses, output_file_path):
    # Clean and format each response
    formatted_responses = []
    for response in responses:
        # Replace newline characters with a space
        response_clean = ' '.join(response.splitlines())
        # Trim leading and trailing whitespace
        response_clean = response_clean.strip()
        # Escape commas (or other special characters if necessary) and enclose in quotes
        response_clean = '"' + response_clean.replace('"', '""') + '"'
        formatted_responses.append(response_clean)

    # Save to file
    pd.DataFrame({'Evaluation of responses from GPT-4': formatted_responses}).to_excel(output_file_path, index=False)

def write_responses_to_csv(responses, output_file_path):
    # Replace newline characters with a delimiter
    formatted_responses = [' '.join(response.splitlines()) for response in responses]
    pd.DataFrame({'Evaluation of responses from GPT-4': formatted_responses}).to_excel(output_file_path, index=False)

file_path = f'files/{F_NAME}_results_grouped_by_question.xlsx'
data = read_csv(file_path)
prompts = process_data_for_function(data)

ASSISTANT_ID = assistant.id

responses = []
for prompt in prompts:
    run, thread = submit_message_and_create_run(ASSISTANT_ID, prompt)
    response = wait_on_run_and_get_response(run, thread)
    print(response)
    responses.append(' '.join(response))

output_file_path = f'files/{F_NAME}_gpteval_output.xlsx'
write_responses_to_csv(responses, output_file_path)

# Post processing and combining all files
results_grouped_path = f'files/{F_NAME}_results_grouped_by_question.xlsx'
gpteval_output_df = pd.read_excel(output_file_path)
results_grouped_df = pd.read_excel(results_grouped_path)

if len(gpteval_output_df) == len(results_grouped_df):
    combined_df = pd.concat([results_grouped_df, gpteval_output_df], axis=1)
    combined_csv_path = f'files/{F_NAME}_llmeval_results.xlsx'
    combined_df.to_excel(combined_csv_path, index=False)
else:
    print("The lengths of the dataframes do not match. Cannot combine.")
