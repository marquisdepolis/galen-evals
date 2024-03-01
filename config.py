import json
import importlib

class Config:
    def __init__(self):
        self.config_file = 'configfile.json'
        self.configuration = self.load_config()
        self.F_NAME = self.configuration["name"]
        self.INSTRUCTION = self.configuration['instructions']
        self.GPT_MODEL = self.configuration["GPT_4"]
        self.perturbations = 'utils/perturbations.json'
        self.knowledgebase = 'utils/knowledgebase.json'
        self.db_layout = 'utils/database_description.json'
        self.db_schema = 'utils/combined_schema.json'
        # Define file paths for each mode
        self.file_paths = {
            'default': {
                'questions': 'files/questions.xlsx',
                'q_original': 'files/questions_original.xlsx',
                'llmresults_file_path': 'files/{F_NAME}_results_grouped_by_model.xlsx',
                'gpt4results_csv_path': 'files/{F_NAME}_results_gpt4.xlsx',
                'results_file_path': 'files/{F_NAME}_allresults_grouped_by_model.xlsx',
                'combined_file_path': 'files/{F_NAME}_results_grouped_by_question.xlsx',
                'llmeval_results': 'files/{F_NAME}_llmeval_results.xlsx',
                'model_rankings': 'files/{F_NAME}_model_rankings.xlsx',
            },
            'rag': {
                'questions': 'files/questions_rag.xlsx',
                'q_original': 'files/questions_original_rag.xlsx',
                'llmresults_file_path': 'files/{F_NAME}_results_grouped_by_model_rag.xlsx',
                'gpt4results_csv_path': 'files/{F_NAME}_results_gpt4_rag.xlsx',
                'results_file_path': 'files/{F_NAME}_allresults_grouped_by_model_rag.xlsx',
                'combined_file_path': 'files/{F_NAME}_results_grouped_by_question_rag.xlsx',
                'llmeval_results': 'files/{F_NAME}_llmeval_results_rag.xlsx',
                'model_rankings': 'files/{F_NAME}_model_rankings_rag.xlsx',
            },
            'dbs': {
                'questions': 'files/questions_db.xlsx',
                'q_original': 'files/questions_original_db.xlsx',
                'llmresults_file_path': f'files/{self.F_NAME}_results_grouped_by_model_db.xlsx',
                'gpt4results_csv_path': f'files/{self.F_NAME}_results_gpt4_db.xlsx',
                'results_file_path': f'files/{self.F_NAME}_allresults_grouped_by_model_db.xlsx',
                'combined_file_path': f'files/{self.F_NAME}_results_grouped_by_question_db.xlsx',
                'llmeval_results': f'files/{self.F_NAME}_llmeval_results_db.xlsx',
                'model_rankings': f'files/{self.F_NAME}_model_rankings_db.xlsx',
            },
            'dynamic': {
                'questions': 'files/questions_dynamic.xlsx',
                'q_original': 'files/questions_original_dynamic.xlsx',
                'llmresults_file_path': f'files/{self.F_NAME}_results_grouped_by_model_dynamic.xlsx',
                'gpt4results_csv_path': f'files/{self.F_NAME}_results_gpt4_dynamic.xlsx',
                'results_file_path': f'files/{self.F_NAME}_allresults_grouped_by_model_dynamic.xlsx',
                'combined_file_path': f'files/{self.F_NAME}_results_grouped_by_question_dynamic.xlsx',
                'llmeval_results': f'files/{self.F_NAME}_llmeval_results_dynamic.xlsx',
                'model_rankings': f'files/{self.F_NAME}_model_rankings_dynamic.xlsx',
            }
        }
        self.current_mode = None
        # self.set_mode('default')  # Set default mode initially

    def load_config(self):
        with open(self.config_file, 'r') as file:
            return json.load(file)
            
    def get_file_path(self, key):
        # Ensure current mode is set, fallback to 'default' if not
        mode = self.current_mode if self.current_mode in self.file_paths else 'default'
        path_template = self.file_paths[mode].get(key, '')
        return path_template.format(F_NAME=self.F_NAME)

    def __getattr__(self, item):
        # Check if the requested item is a key in the current mode's file_paths
        if item in self.file_paths.get(self.current_mode, {}):
            # Return the dynamically resolved file path
            return self.get_file_path(item)
        else:
            # If the item is not a file path key, raise an AttributeError
            raise AttributeError(f"'Config' object has no attribute '{item}'")

    def set_mode(self, mode):
        if mode in self.file_paths:
            if mode != self.current_mode:
                self.current_mode = mode
                # No need to dynamically set attributes here since file paths are generated on demand
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
