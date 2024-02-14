# Updated code for evaluation
import pandas as pd
import marvin
from marvin import ai_model, ai_fn
from pydantic import BaseModel, Field
from typing import List
from config import config
config.set_mode("default")

marvin.settings.openai.chat.completions.model = 'gpt-4'

class Answer(BaseModel):
    index: int = Field(..., description='Index of the answer')
    answer: str = Field(..., description='The answer')

class RankingResults(BaseModel):
    reasoning: str = Field(..., description='Give some thoughts on the quality of the answers')
    ranked_answers: List[int] = Field(..., description='The ranked answer indexes')

@ai_fn
def rank_answers(question: str, answers: List[Answer]) -> RankingResults:
    '''Rank the answers to the question from best to worst'''

def read_excel(file_path):
    return pd.read_excel(file_path)

def process_data(data):
    results = []
    n = 1
    additional_columns = ['category', 'type']  # Add any other additional columns here
    for _, row in data.head(n).iterrows():
        question = row['Question']
        models = [col for col in data.columns if col not in ['Question'] + additional_columns]
        answers = [row[model] for model in models if pd.notna(row[model])]
        answer_objects = [Answer(index=i, answer=a) for i, a in enumerate(answers)]
        result = rank_answers(question, answer_objects)
        result_dict = {'Question': question}
        for col in additional_columns:
            if col in row:
                result_dict[col] = row[col]

        for idx, rank in enumerate(result.ranked_answers):
            result_dict[models[idx]] = rank + 1  # +1 to start ranking from 1 instead of 0
        results.append(result_dict)
    return results

input_file_path = config.combined_file_path
output_file_path = config.model_rankings
data = read_excel(input_file_path)
ranking_results = process_data(data)

for result in ranking_results:
    print(result)

ranking_df = pd.DataFrame(ranking_results)
ranking_df.to_excel(output_file_path, index=False)
print(f"Ranking results saved to {output_file_path}")
