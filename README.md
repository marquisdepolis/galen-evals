# galen-evals
Evals for Drug Discovery

# What you need to run this
1. OpenAI API key
2. Replicate API key
3. Add them to your .env file

# Steps
1. Update the config.json if needed
2. Run the galen_llm_responses.ipynb to get various OSS LLM responses, choose the ones you want in the code
3. Run galen_gpt_response.py to get gpt4 responses
4. Run results_convert.py to change format, since right now it's using csv files
5. Run galen_eval_gpt4.py to get GPT-4 to evaluate the answers 

# Files
The crucial ones are:
1. questions.csv, which has the list of Questions we want to ask
2. galen_llmeval_results.csv which has the final list of answers and evaluations from GPT-4
3. All other files are intermediate creations, kept for easy auditijg

# To do
There's plenty to do, since it's a simple implementation, but in no order:
1. Change storage from csv to something better
2. Clean up the answer formatting
3. Speed up GPT execution by parallelising the API calls
4. Add checks against local files for specific models
5. Create a "Best Answer" for the questions in case we want to measure the answers against that
