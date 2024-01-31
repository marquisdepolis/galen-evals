# %%
import replicate
import pandas as pd
import json
import os
from config import config
from dotenv import load_dotenv
load_dotenv()
folder_path = 'files'
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# # Load the file
df = pd.read_excel(config.questions)
# Save the original DataFrame
df.to_excel(config.q_original, index=False)

# Trim whitespace and newline characters
df['Question'] = df['Question'].str.strip()  # Removes leading/trailing whitespace

# Check for duplicate questions
duplicates = df.duplicated(subset=['Question'], keep=False)
if duplicates.any():
    print("Duplicates found. Removing duplicates.")

    # Remove duplicates, keeping the first occurrence
    df = df.drop_duplicates(subset=['Question'], keep='first')

    # Save the modified DataFrame, overwriting the original 'questions.xlsx'
    df.to_excel(config.questions, index=False)
else:
    print("No duplicates found.")

# DataFrame to store the results
results_df = pd.DataFrame(columns=['Model', 'Question', 'Response'])

models = {
    # "qwen-14b": "nomagick/qwen-14b-chat:f9e1ed25e2073f72ff9a3f46545d909b1078e674da543e791dec79218072ae70",
    # 3: "01-ai/yi-34b:d83ccf090ccd5c7fe507ca302a558a850468293385d02bb807ee2753d802dd85", # Not the chat model
    # "falcon-40b": "joehoover/falcon-40b-instruct:7d58d6bddc53c23fa451c403b2b5373b1e0fa094e4e0d1b98c3d02931aa07173",
    # "yi-34b": "01-ai/yi-34b-chat:914692bbe8a8e2b91a4e44203e70d170c9c5ccc1359b283c84b0ec8d47819a46",
    # "mistral-7b": "mistralai/mistral-7b-instruct-v0.2:f5701ad84de5715051cb99d550539719f8a7fbcf65e0e62a3d1eb3f94720764e",
    "llama2-70b": "meta/llama-2-70b-chat",
    "openhermes2": "antoinelyset/openhermes-2.5-mistral-7b:d7ccd25700fb11c1787c25b580ac8d715d2b677202fe54b77f9b4a1eb7d73e2b",
    "mixtral-instruct": "mistralai/mixtral-8x7b-instruct-v0.1:2b56576fcfbe32fa0526897d8385dd3fb3d36ba6fd0dbe033c72886b81ade93e",
    "deepseek_33bq": "kcaverly/deepseek-coder-33b-instruct-gguf:ea964345066a8868e43aca432f314822660b72e29cab6b4b904b779014fe58fd",
    }

prompt_for_qwen="""<|im_start|>system\nYou are a helpful assistant. {config.INSTRUCTION}.<|im_end|>\n<|im_start|>user\n{question}<|im_end|>\n<|im_start|>assistant\n"""
prompt_for_hermes = """[
{{
  "role": "system",
  "content": "You are a helpful assistant. {config.INSTRUCTION}." 
}},
{{
  "role": "user",
  "content": {question}
}}
]"""

# Iterate through each model
for model_key, model_value in models.items():
    responses = []

    for index, row in df.iterrows():
        qn = row['Question']
        question = json.dumps(qn)

        if model_key == "yi-34b":  # Yi model
            prompt = prompt_for_qwen.format(INSTRUCTION=config.INSTRUCTION, question=question)
        if model_key == "qwen-14b":  # Qwen model
            prompt = prompt_for_qwen.format(INSTRUCTION=config.INSTRUCTION, question=question)
        elif model_key == "openhermes2":  # Hermes model
            prompt = prompt_for_hermes.format(INSTRUCTION=config.INSTRUCTION, question=question)
        else:
            prompt = f"You are a helpful assistant. {config.INSTRUCTION}. {question}"

        try:
            print(f"{model_key}: {prompt}")
            output = replicate.run(
                model_value,
                input={
                  "debug": False,
                #   "top_k": 50,
                  "top_p": 0.9,
                  "prompt": prompt,
                  "temperature": 0.7,
                  "max_new_tokens": 500,
                  "min_new_tokens": -1
                }
            )
            response = ""
            response_parts = []  # Initialize an empty list to collect string representations

            for item in output:
                item_str = str(item)  # Convert item to string
                response += item_str
                
            response = response.strip()

        except Exception as e:
            response = f"Error: {e}"

        new_row = pd.DataFrame({'Model': [model_key], 'Question': [qn], 'Response': [response]})
        results_df = pd.concat([results_df, new_row], ignore_index=True)

        if index % 20 == 0:  # Save every 10 questions, adjust as needed
            results_df.to_excel(config.llmresults_file_path, index=False, sheet_name='Sheet1')
            
results_df.to_excel(config.llmresults_file_path, index=False, sheet_name='Sheet1')


