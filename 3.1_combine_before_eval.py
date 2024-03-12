# Combine files before Eval
import pandas as pd
from config import config

F_NAME = config.F_NAME
# File paths
db_file_path = f'files/{F_NAME}_results_grouped_by_question_db.xlsx'
dynamic_file_path = f'files/{F_NAME}_results_grouped_by_question_dynamic.xlsx'
rag_file_path = f'files/{F_NAME}_results_grouped_by_question_rag.xlsx'

# Load the Excel files
db_df = pd.read_excel(db_file_path)
dynamic_df = pd.read_excel(dynamic_file_path)
rag_df = pd.read_excel(rag_file_path)

# Selecting only the relevant columns
relevant_columns = ['Question', 'Model', 'Response', 'Latency', 'Category', 'Type']
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
combined_df = pd.concat([db_df, dynamic_df, rag_df], ignore_index=True)
# Fill missing 'Response' values right after concatenation
combined_df['Response'].fillna('No response', inplace=True)
combined_df['Category'].fillna('No category', inplace=True)
# Removing duplicates
final_combined_df = combined_df.drop_duplicates(subset=['Question', 'Model', 'Category', 'Type'])

# Save the cleaned and combined DataFrame to a new Excel file
output_file_path = f'files/{F_NAME}_allresults_combined.xlsx'
combined_df.to_excel(output_file_path, index=False)

print(f"Combined file saved to: {output_file_path}")

# Step 1: Ensure consistent "Category" for each "Question"
combined_df['Category'] = combined_df.groupby('Question')['Category'].transform('first')
# Check for missing values in key columns
missing_values_check = combined_df[['Question', 'Model', 'Response']].isnull().sum()
print("Missing values check:\n", missing_values_check)

# Pivot the DataFrame
pivot_df = combined_df.pivot_table(index=['Question', 'Category'], columns='Model', values='Response', aggfunc=lambda x: ' | '.join(x.dropna().unique())).reset_index()

# Clean up the DataFrame for saving
pivot_df.reset_index(drop=True, inplace=True)
pivot_df.columns.name = None  # Remove the index/columns level name for a cleaner output

output_pivot_file_path = f'files/{F_NAME}_combined_questions_responses.xlsx'
pivot_df.to_excel(output_pivot_file_path, index=False)

print(f"Pivoted file saved to: {output_pivot_file_path}")
