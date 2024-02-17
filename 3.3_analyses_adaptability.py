# Update adaptability excel and run analyses
import pandas as pd
from config import config

config.set_mode("default")
F_NAME = config.F_NAME

# Load the Excel files
galen_analysis_path = f'files/{F_NAME}_analysis.xlsx'
galen_analysis_adaptability_path = f'files/{F_NAME}_analysis_adaptability.xlsx'

# Read the Excel files into DataFrame
galen_analysis_df = pd.read_excel(galen_analysis_path)
galen_analysis_adaptability_df = pd.read_excel(galen_analysis_adaptability_path)

galen_analysis_df['Normalized_Question'] = galen_analysis_df['Question'].str.lower().str.strip()
galen_analysis_adaptability_df['Normalized_Question'] = galen_analysis_adaptability_df['Question'].str.lower().str.strip()

# Perform the merge again, this time including the normalized question for matching
refined_merge_df = pd.merge(
    galen_analysis_adaptability_df,
    galen_analysis_df[['Normalized_Question', 'Model', 'Type', 'Ranking']],
    on=['Normalized_Question', 'Model', 'Type'],
    how='left'
)

# Show the result of the refined merge to check the outcome
analysis_df_path = f'files/{F_NAME}_analysis_adaptability.xlsx'
refined_merge_df.to_excel(analysis_df_path, index=False)

