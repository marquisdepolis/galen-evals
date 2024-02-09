# Start ollama according to the script if you need to 
import pandas as pd
import json
import requests
from pydantic import BaseModel, ValidationError, conint
import importlib
import config
importlib.reload(config)
from config import config, reset_config
from dotenv import load_dotenv
load_dotenv()
reset_config()
# import os
# import subprocess

# current_directory = os.getcwd()
# shell_script = os.path.join(current_directory, 'ollama_script.sh')
# result = subprocess.run(['bash', shell_script], check=True)

INSTRUCTION = config.INSTRUCTION
F_NAME = config.F_NAME

class ModelRanking(BaseModel):
    Name: str
    Ranking: conint(ge=0)  # conint(ge=0) means a constrained integer greater than or equal to 0

class ResponseModel(BaseModel):
    Model: list[ModelRanking]

class Ranking(BaseModel):
    name: str
    ranking: int

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
model = "llama2:7b"
def generate_text(data):
    r = requests.post("http://localhost:11434/api/generate", json=data, stream=False)
    full_response = json.loads(r.text)
    resp = json.loads(full_response["response"])
    # resp = (json.dumps(json.loads(full_response["response"]), indent=2))
    print(f"/n/n Response is: /n {resp}")
    return resp

def read_excel(filepath, column_name):
    df = pd.read_excel(filepath)
    return df[column_name].tolist()

def validate_response(response):
    try:
        ResponseModel(**response)
        return True
    except ValidationError:
        return False
    
def make_json(data):
    response_full = []
    for index, info in enumerate(data, start=1):  # Start indexing from 1
        valid_response = False
        attempts = 0
        while not valid_response and attempts < 3:
            print(f"The data is: /n {info}")
            prompt = f"Extract the model rankings from {info} and give me the response as a JSON. \nUse the following template: {json.dumps(template)}."
            print("/n/n We're starting! /n")
            response_data = {
                "model": model,
                "prompt": prompt,
                "format": "json",
                "stream": False,
                "options": {"temperature": 0.1, "top_p": 0.99, "top_k": 100},
                # response_model=Ranking
            }
            print(f"response data is: {response_data}")
            response = generate_text(response_data)
            valid_response = validate_response(response)
            attempts += 1
        if valid_response:
            response_full.append({"index": index, "response": response})
        else:
            print("Failed to get a valid response after 3 attempts.")
            response = ''.join([str(item) for item in response])
            response_full.append({"index": index, "response": {"Model": []}})
    return response_full

# Read the JSON file
def write_data():
    with open("output.json", "r") as f:
        json_strings = json.load(f)

    unique_models = set()
    for item in json_strings:
        response_obj = item["response"]  # Directly use the response object
        for model in response_obj["Model"]:
            unique_models.add(model['Name'])

    # Convert the set to a list and sort it
    unique_models = sorted(list(unique_models))

    data = []
    for item in json_strings:
        row = {model: '' for model in unique_models}  # Initialize all model rankings as empty
        row['ID'] = item['index']  # Use the index from the original data
        for model in item["response"]["Model"]:
            row[model['Name']] = model.get('Ranking', '')
        data.append(row)

    # Create DataFrame and write to Excel
    df = pd.DataFrame(data)
    excel_file = config.model_rankings
    df.to_excel(excel_file, index=False)

    print(f"Data written to {excel_file}")

def main():
    filepath = config.get_file_path('llmeval_results')
    print(f"filepath is: {filepath}")
    column = 'Evaluation of responses from GPT-4'
    dataframe = read_excel(filepath, column)
    json_output = make_json(dataframe)
    with open("output.json", "w") as f:
        json.dump(json_output, f)

if __name__ == "__main__":
    # config.set_mode("default")
    main()
    write_data()


