# galen-evals
Evals for Drug Discovery

# What you need to run this
1. OpenAI API key
2. Replicate API key
3. Add them to your .env file

# Steps
1. Update the config.json if needed. Oh and check the knowledgebase.json and perturbations.json to see if they have verisimilitude!
2. Run the responses_llm.ipynb to get various OSS LLM responses, choose the ones you want in the code
3. Run response_gpt4.ipynb to get GPT-4 responses
4. Run results_convert.py to change format
5. Run eval_gpt4.py to get GPT-4 to evaluate the answers
6. Run eval_local_ranking.ipynb to extract rankings from the evaluation

# Files
The crucial ones are:
1. questions.xlsx, which has the list of Questions we want to ask
2. galen_llmeval_results.xlsx which has the final list of answers and evaluations from GPT-4
3. model_rankings.xlsx with the rankings for the final list of answers that were evaluated
4. All other files are intermediate creations, kept for auditing

# To do
There's plenty to do, since it's a simple implementation, but in no order:
1. Change storage from csv to something better, and store them inside folders [Done]
2. Clean up the answer formatting [Done]
3. Speed up GPT execution by parallelising the API calls
4. Add checks against local files for specific models
5. Create a "Best Answer" for the questions in case we want to measure the answers against that - (can also use this to DPO the models later as needed)
6. Create a way to perturb the questions to see how well the LLMs react to new info coming in
7. Create a way to provide a "knowledgebase" to see how good the LLMs are at asking for help from the right quarters