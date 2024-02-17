# Combine files before Eval
import pandas as pd
from config import config

F_NAME = config.F_NAME
# File paths
db_file_path = 'files/galen_results_grouped_by_question_db.xlsx'
dynamic_file_path = 'files/galen_results_grouped_by_question_dynamic.xlsx'
rag_file_path = 'files/galen_results_grouped_by_question_rag.xlsx'

# Load the Excel files
db_df = pd.read_excel(db_file_path)
dynamic_df = pd.read_excel(dynamic_file_path)
rag_df = pd.read_excel(rag_file_path)

# Selecting only the relevant columns
relevant_columns = ['Question', 'Response', 'Latency', 'Category', 'Type']
db_selected = db_df[relevant_columns]
dynamic_selected = dynamic_df[relevant_columns]
rag_selected = rag_df[relevant_columns]

def normalize_questions(df):
    df_copy = df.copy()
    df_copy.loc[:, 'Question'] = df_copy['Question'].str.lower().str.strip()
    return df_copy

db_df = normalize_questions(db_selected)
dynamic_df = normalize_questions(dynamic_selected)
rag_df = normalize_questions(rag_selected)

# Combining the selected DataFrames
combined_df = pd.concat([db_selected, dynamic_selected, rag_selected], ignore_index=True)

# Removing duplicates
final_combined_df = combined_df.drop_duplicates()

# Save the cleaned and combined DataFrame to a new Excel file
output_file_path = f'files/{F_NAME}_combined_questions_responses.xlsx'
final_combined_df.to_excel(output_file_path, index=False)

print(f"Combined file saved to: {output_file_path}")
