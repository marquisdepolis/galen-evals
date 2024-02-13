import pandas as pd

# Load the questions from the original Excel file
questions_df = pd.read_excel('questions.xlsx')

# Filter questions based on the 'Type' column
rag_questions = questions_df[questions_df['Type'] == 'RAG']
db_questions = questions_df[questions_df['Type'] == 'DB']
dynamic_questions = questions_df[~questions_df['Type'].isin(['RAG', 'DB'])]

# Save the filtered questions into separate Excel files
rag_questions.to_excel('questions_rag.xlsx', index=False)
db_questions.to_excel('questions_db.xlsx', index=False)
dynamic_questions.to_excel('questions_dynamic.xlsx', index=False)
