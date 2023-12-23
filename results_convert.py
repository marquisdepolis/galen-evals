import re
import pandas as pd
from difflib import SequenceMatcher

def clean_text(text):
    """
    Remove non-ASCII characters from the text.
    """
    return ''.join(char for char in text if char.isascii())

def create_combined_csv(original_csv_path, interim_csv_path, combined_csv_path):
    # Read the original and interim data
    original_data = pd.read_excel(original_csv_path) #, encoding='utf-8-sig'
    interim_data = pd.read_excel(interim_csv_path)

    # Combine the data
    combined_data = pd.concat([original_data, interim_data], ignore_index=True)

    # Save the combined data to a new CSV file
    combined_data.to_excel(combined_csv_path, index=False)

def merge_on_contains(big_df, small_df, big_col, small_col):
    # Lowercase and strip whitespace for more effective matching
    big_df[big_col] = big_df[big_col].str.lower().str.strip()
    small_df[small_col] = small_df[small_col].str.lower().str.strip()

    # Check if 'category' column exists in small_df
    if 'category' in small_df.columns:
        # Create a new column for the merged category in big_df
        big_df['category'] = ''

        # Iterate over the small dataframe and update the category in the big dataframe
        for _, row in small_df.iterrows():
            contains_mask = big_df[big_col].str.contains(row[small_col])
            big_df.loc[contains_mask, 'category'] = row['category']
    else:
        # Handle the case when 'category' column does not exist
        # For example, you can set a default category or leave it as it is
        big_df['category'] = 'default_category'  # or any other handling logic

    return big_df

# Load the files
questions_file_path = 'questions.xlsx' 
llmresults_file_path = 'results_grouped_by_model.xlsx'
gpt4results_csv_path = 'results_gpt4.xlsx'
results_file_path = 'allresults_grouped_by_model.xlsx'

create_combined_csv(llmresults_file_path, gpt4results_csv_path, results_file_path)

# Reading the files
questions_df = pd.read_excel(questions_file_path)
results_df = pd.read_excel(results_file_path)

# Ensure the total number of questions in results_grouped_by_model.xlsx is a multiple of the number in questions.xlsx
if len(results_df) % len(questions_df) != 0:
    raise ValueError("The total number of questions in results_grouped_by_model.xlsx must be a multiple of the number in questions.xlsx.")

# Replace questions in results_grouped_df with those from questions_df
num_repetitions = len(results_df) // len(questions_df)
repeated_questions = pd.concat([questions_df['Question']] * num_repetitions, ignore_index=True)
results_df['Question'] = repeated_questions

# Save the modified DataFrame to a new Excel file
results_df.to_excel(results_file_path, index=False)  # Replace with your desired path

# Applying the merge_on_contains function
merged_df = merge_on_contains(results_df, questions_df, 'Question', 'Question')

# CLEAN DATA
# # Define a regular expression pattern to match unwanted characters and sequences
# pattern = r'(\\n|\\|")'
# # Use the pattern to replace matched characters with a single space
# merged_df['Question'] = merged_df['Question'].str.replace(pattern, ' ', regex=True)
# # Apply the clean_text function to remove non-ASCII characters
# merged_df['Question'] = merged_df['Question'].apply(clean_text)
# # Replace multiple white spaces with a single space
# merged_df['Question'] = merged_df['Question'].str.replace(r'\s+', ' ', regex=True)
# # Remove leading and trailing whitespaces
# merged_df['Question'] = merged_df['Question'].str.strip()

# Pivoting the data
pivoted_data = merged_df.pivot(index=['Question', 'category'], columns='Model', values='Response')

# Resetting index to make 'Question' and 'category' columns again
pivoted_data.reset_index(inplace=True)

pivoted_data.to_excel('results_grouped_by_question.xlsx', index=False)
