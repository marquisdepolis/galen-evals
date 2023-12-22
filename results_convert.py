import pandas as pd

def create_combined_csv(original_csv_path, interim_csv_path, combined_csv_path):
    # Read the original and interim data
    original_data = pd.read_csv(original_csv_path, encoding='utf-8-sig')
    interim_data = pd.read_csv(interim_csv_path, encoding='utf-8-sig')

    # Combine the data
    combined_data = pd.concat([original_data, interim_data], ignore_index=True)

    # Save the combined data to a new CSV file
    combined_data.to_csv(combined_csv_path, index=False)

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

# Load the CSV files
questions_file_path = 'questions.csv' 
llmresults_file_path = 'results_grouped_by_model.csv'  # File path for results
gpt4results_csv_path = 'results_gpt4.csv'
results_file_path = 'allresults_grouped_by_model.csv'  # File path for results

create_combined_csv(llmresults_file_path, gpt4results_csv_path, results_file_path)

# Reading the CSV files
questions_df = pd.read_csv(questions_file_path)
results_df = pd.read_csv(results_file_path)

# Applying the merge_on_contains function
merged_df = merge_on_contains(results_df, questions_df, 'Question', 'Question')

merged_df['Question'] = merged_df['Question'].str.replace(r'\\"', '', regex=True)
merged_df['Question'] = merged_df['Question'].str.replace(r'"', '', regex=True)

# Pivoting the data
pivoted_data = merged_df.pivot(index=['Question', 'category'], columns='Model', values='Response')

# Resetting index to make 'Question' and 'category' columns again
pivoted_data.reset_index(inplace=True)

pivoted_data.to_csv('results_grouped_by_question.csv', index=False)
