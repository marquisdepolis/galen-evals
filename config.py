import json
import importlib

class Config:
    def __init__(self):
        self.config_file = 'config.json'
        self.config = self.load_config()
        self.F_NAME = self.config["name"]
        self.INSTRUCTION = self.config['instructions']
        self.GPT_MODEL = self.config["GPT_MODEL"]
        self.perturbations = 'utils/perturbations.json'
        self.knowledgebase = 'utils/knowledgebase.json'
        self.db_layout = 'utils/database_description.json'
        # Define file paths for each mode
        self.file_paths = {
            'default': {
                'questions': 'files/questions.xlsx',
                'q_original': 'files/questions_original.xlsx',
                'llmresults_file_path': f'files/{self.F_NAME}_results_grouped_by_model.xlsx',
                'gpt4results_csv_path': f'files/{self.F_NAME}_results_gpt4.xlsx',
                'results_file_path': f'files/{self.F_NAME}_allresults_grouped_by_model.xlsx',
                'combined_file_path': f'files/{self.F_NAME}_results_grouped_by_question.xlsx',
                'llmeval_results': f'{self.F_NAME}_llmeval_results.xlsx',
                'model_rankings': f'{self.F_NAME}_model_rankings.xlsx',
            },
            'dbs': {
                'questions': 'files/questions_db.xlsx',
                'q_original': 'files/questions_original_db.xlsx',
                'llmresults_file_path': f'files/{self.F_NAME}_results_grouped_by_model_db.xlsx',
                'gpt4results_csv_path': f'files/{self.F_NAME}_results_gpt4_db.xlsx',
                'results_file_path': f'files/{self.F_NAME}_allresults_grouped_by_model_db.xlsx',
                'combined_file_path': f'files/{self.F_NAME}_results_grouped_by_question_db.xlsx',
                'llmeval_results_db': f'{self.F_NAME}_llmeval_results_db.xlsx',
                'model_rankings_db': f'{self.F_NAME}_model_rankings_db.xlsx',
            },
            'dynamic': {
                'questions': 'files/questions_dynamic.xlsx',
                'q_original': 'files/questions_original_dynamic.xlsx',
                'llmresults_file_path': f'files/{self.F_NAME}_results_grouped_by_model_dynamic.xlsx',
                'gpt4results_csv_path': f'files/{self.F_NAME}_results_gpt4_dynamic.xlsx',
                'results_file_path': f'files/{self.F_NAME}_allresults_grouped_by_model_dynamic.xlsx',
                'combined_file_path': f'files/{self.F_NAME}_results_grouped_by_question_dynamic.xlsx',
                'llmeval_results_dy': f'{self.F_NAME}_llmeval_results_dynamic.xlsx',
                'model_rankings_dy': f'{self.F_NAME}_model_rankings_dynamic.xlsx',
            }
        }
        self.current_mode = None
        self.set_mode('default')  # Set default mode initially

    def load_config(self):
        with open(self.config_file, 'r') as file:
            return json.load(file)

    def set_mode(self, mode):
        if mode in self.file_paths and mode != self.current_mode:
            self.current_mode = mode
            for key, value in self.file_paths[mode].items():
                setattr(self, key, value)
        else:
            raise ValueError(f"Invalid mode: {mode}")

    def reset(self):
        # Re-initialize or redefine the configuration settings
        self.__init__()

# Create a global instance
config = Config()
# Function to reset the config - can be called from other scripts
def reset_config():
    global config
    config = Config()
