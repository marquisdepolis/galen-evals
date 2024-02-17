# Combine files before Eval
import pandas as pd

# File paths
db_file_path = 'files/galen_results_grouped_by_question_db.xlsx'
dynamic_file_path = 'files/galen_results_grouped_by_question_dynamic.xlsx'
rag_file_path = 'files/galen_results_grouped_by_question_rag.xlsx'
questions_file_path = 'files/questions.xlsx'

# Load the Excel files
db_df = pd.read_excel(db_file_path)
dynamic_df = pd.read_excel(dynamic_file_path)
rag_df = pd.read_excel(rag_file_path)
questions_df = pd.read_excel(questions_file_path)

# Normalize question texts
def normalize_questions(df):
    df['Question'] = df['Question'].str.lower().str.strip()
    return df

db_df = normalize_questions(db_df)
dynamic_df = normalize_questions(dynamic_df)
rag_df = normalize_questions(rag_df)
questions_df = normalize_questions(questions_df)

# Merge each model-specific DataFrame with the master file based on 'Question'
merged_db_df = pd.merge(db_df, questions_df, on='Question', how='left')
merged_dynamic_df = pd.merge(dynamic_df, questions_df, on='Question', how='left')
merged_rag_df = pd.merge(rag_df, questions_df, on='Question', how='left')

# Combine all merged data into a single DataFrame
combined_df = pd.concat([merged_db_df, merged_dynamic_df, merged_rag_df], ignore_index=True)

# Select relevant columns and remove duplicates
relevant_columns = ['Question'] + [col for col in combined_df.columns if 'Response' in col] + ['Category', 'Type']
cleaned_df = combined_df[relevant_columns].drop_duplicates()

# Save the cleaned and combined DataFrame to a new Excel file
output_file_path = 'files/combined_questions_responses.xlsx'
cleaned_df.to_excel(output_file_path, index=False)

# Output file path for download
print(output_file_path)
