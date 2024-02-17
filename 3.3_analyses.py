# Create a master file to do analyses
import os
import pandas as pd
from config import config
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

config.set_mode("default")
F_NAME = config.F_NAME

# Load the datasets
allresults_combined_df = pd.read_excel(f'files/{F_NAME}_allresults_combined.xlsx')
model_rankings_df = pd.read_excel(f'files/{F_NAME}_model_rankings.xlsx')
analysis_df_path = f'files/{F_NAME}_analysis.xlsx'

# Preliminary cleaning to ensure consistency in model names and question texts
# allresults_combined_df['Model'] = allresults_combined_df['Model'].str.lower().str.replace(' ', '').str.replace('-', '').str.replace('.', '')

# Remove "Question: " part and other preprocessing in model_rankings_df
model_rankings_df['Question'] = model_rankings_df['Question'].str.replace('question: ', '', case=False).str.split('|').str[0].str.strip()

# Reshape model_rankings_df to long format
model_rankings_long_df = pd.melt(model_rankings_df, id_vars=['Question', 'Reasoning', 'Category'], var_name='Model', value_name='Ranking')

# Clean 'Model' column to ensure consistency
model_rankings_long_df['Model'] = model_rankings_long_df['Model'].str.lower().replace({'falcon40b': 'falcon-40b', 'gpt35turbo1106': 'gpt-3.5-turbo-1106', 'mistral7b': 'mistral-7b', 'mixtralinstruct': 'mixtral-instruct', 'noushermes2': 'noushermes2', 'yi34b': 'yi-34b'})

# Merge the datasets
combined_data = pd.merge(allresults_combined_df, model_rankings_long_df, on=['Question', 'Model'], how='inner')

combined_data.to_excel(analysis_df_path, index=False)
