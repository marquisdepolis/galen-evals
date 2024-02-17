# Updated code for evaluation
import pandas as pd
import marvin
import os
from marvin import ai_model, ai_fn
from pydantic import BaseModel, Field
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
from config import config
config.set_mode("default")
F_NAME = config.F_NAME

marvin.settings.openai.chat.completions.model = 'gpt-4-turbo-preview'

class Answer(BaseModel):
    index: int = Field(..., description='Index of the answer')
    answer: str = Field(..., description='The answer')

class RankingResults(BaseModel):
    reasoning: str = Field(..., description='Give some thoughts on the quality of the response from the LLM and its level of adaptability with respect to changes in circumstances and given knowledgebase')
    rating: List[int] = Field(..., description='The ranked answer indexes')

@ai_fn
def rank_answers(question: str, answers: List[Answer]) -> RankingResults:
    '''Analyse how well the Perturbed Response and Final Analysis Response take into account the perturbations and knowledgebase, and give a rating from 1 to 5.'''

def read_excel(file_path):
    return pd.read_excel(file_path)

def concatenate_question_model_response(row, df):
    question_part = f"Question: {row['Final Analysis Question']} | "
    model_response_part = ' | '.join([f"{col}: {row[col]}" for col in df.columns[7:]])
    return question_part + model_response_part

def process_data(data):
    results = []
    reasons = []
    n=6
    i = 0
    additional_columns = ['Category', 'Type', 'Model']
    for _, row in data.iterrows():
        question = []
        i = i+1
        question = concatenate_question_model_response(row, data)
        # models = [col for col in data.columns if col not in ['Question'] + additional_columns]
        # answers = [row[model] for model in models if pd.notna(row[model])]
        answer_objects = [Answer(index=i, answer = question)]
        result = rank_answers(question, answer_objects)
        result_dict = {'Final Analysis Question': question, 'Reasoning': result.reasoning, 'Rating': result.rating}
        for col in additional_columns:
            if col in row:
                result_dict[col] = row[col]
        results.append(result_dict)
    return results

input_file_path = f'files/{F_NAME}_allresults_grouped_by_model_dynamic.xlsx'
output_file_path = f'files/{F_NAME}_analysis_adaptability.xlsx'
data = read_excel(input_file_path)
ranking_results = process_data(data)

for result in ranking_results:
    print(result)

ranking_df = pd.DataFrame(ranking_results)
print(ranking_df)
ranking_df.to_excel(output_file_path, index=False)
print(f"Ranking results saved to {output_file_path}")
