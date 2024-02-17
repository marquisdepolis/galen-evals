# Archive the intermediate files
import os
import glob
from config import config
directory = 'files/'
archive_directory = os.path.join(directory, '#Archive')

# Create the #Archive directory if it doesn't exist
if not os.path.exists(archive_directory):
    os.makedirs(archive_directory)

# List all files that start with F_NAME and exclude the specified files
files_to_move = [f for f in glob.glob(f"{directory}/{config.F_NAME}_*") 
                 if '_model_rankings' not in f and '_llmeval_results' not in f and 'questions' not in f and 'analysis' not in f and '_allresults_' not in f]

# Move the files to the #Archive folder
for file in files_to_move:
    os.rename(file, os.path.join(archive_directory, os.path.basename(file)))
    print(f"Moved file: {file} to {archive_directory}")
