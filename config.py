import json
# filepath
config_file = 'config.json'
with open(config_file, 'r') as config_file:
    config = json.load(config_file)

INSTRUCTION = config['instructions']
F_NAME = config["name"]
GPT_MODEL = config["GPT_MODEL"]

perturbations_file_path = 'perturbations.json'
knowledgebase = 'knowledgebase.json'
q_file_path = 'files/questions.xlsx'
q_original = 'files/questions_original.xlsx'
q_dynamic = 'files/questions_dynamic.xlsx'
q_orig_dynamic = 'files/questions_original_dynamic.xlsx'
llmresults_file_path = f'files/{F_NAME}_results_grouped_by_model.xlsx'
gpt4results_csv_path = f'files/{F_NAME}_results_gpt4.xlsx'
results_file_path = f'files/{F_NAME}_allresults_grouped_by_model.xlsx'
combined_file_path = f'files/{F_NAME}_results_grouped_by_question_dynamic.xlsx'
llmeval_results = f'{F_NAME}_llmeval_results.xlsx'
model_rankings = f'{F_NAME}_model_rankings.xlsx'