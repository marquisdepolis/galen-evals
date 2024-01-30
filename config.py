import json
# filepath
config_file = 'config.json'
with open(config_file, 'r') as config_file:
    config = json.load(config_file)

INSTRUCTION = config['instructions']
F_NAME = config["name"]
GPT_MODEL = config["GPT_MODEL"]

perturbations = 'utils/perturbations.json'
knowledgebase = 'utils/knowledgebase.json'
db_layout = 'utils/database_description.json'

q_file_path = 'files/questions.xlsx'
q_original = 'files/questions_original.xlsx'
llmresults_file_path = f'files/{F_NAME}_results_grouped_by_model.xlsx'
gpt4results_csv_path = f'files/{F_NAME}_results_gpt4.xlsx'
results_file_path = f'files/{F_NAME}_allresults_grouped_by_model.xlsx'
combined_file_path = f'files/{F_NAME}_results_grouped_by_question.xlsx'
llmeval_results = f'{F_NAME}_llmeval_results.xlsx'
model_rankings = f'{F_NAME}_model_rankings.xlsx'

q_dynamic = 'files/questions_dynamic.xlsx'
q_orig_dynamic = 'files/questions_original_dynamic.xlsx'
llmresults_file_path_dy = f'files/{F_NAME}_results_grouped_by_model_dynamic.xlsx'
gpt4results_csv_path_dy = f'files/{F_NAME}_results_gpt4_dynamic.xlsx'
results_file_path_dy = f'files/{F_NAME}_allresults_grouped_by_model_dynamic.xlsx'
combined_file_path_dy = f'files/{F_NAME}_results_grouped_by_question_dynamic.xlsx'
llmeval_results_dy = f'{F_NAME}_llmeval_results_dynamic.xlsx'
model_rankings_dy = f'{F_NAME}_model_rankings_dynamic.xlsx'