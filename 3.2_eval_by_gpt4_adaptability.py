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
    # index: int = Field(..., description='Index of the answer')
    answer: str = Field(..., description='The response to analyse')

class RankingResults(BaseModel):
    reasoning: str = Field(..., description='Reason out loud on the qualities of the Responses and how well the Model shows adaptability with respect to changes in circumstances via perturbations.json and given knowledgebase.json')
    rating: List[int] = Field(..., description='Answer rating 1 to 5')

@marvin.ai_fn
def rate_responses(question: str, answers: List[Answer]) -> RankingResults:
    """
    Analyse how well the Perturbed Response and Final Analysis Response take into account the perturbations and knowledgebase, and give ratings from 1 to 5 for Perturbation Response and Final Analysis Response. 1 is the lowest and 5 is the highest.
    For instance, if the Final Question Response is empty, or has "I am a language model and I don't know" that is very bad."
    If the subsequent answers take new information into account and apply them appropriately, then it's very good.
    """

def read_excel(file_path):
    return pd.read_excel(file_path)

def concatenate_question_model_response(row, df):
    question_part = f"Question: {row['Final Analysis Question']} | "
    model_response_part = f"Question: {row['Final Analysis Response']} | "
    return question_part + model_response_part

def process_data(data):
    results = []
    n=10
    additional_columns = ['Category', 'Type', 'Model', 'Question', 'Latency']
    for _, row in data.iterrows():
        qn_resp = []
        qn_resp = concatenate_question_model_response(row, data)
        print(f"The questions re: \n{qn_resp}\n")
        answer_objects = [Answer(answer = qn_resp)]
        result = rate_responses(qn_resp, answer_objects)
        result_dict = {'Final Analysis Question': qn_resp, 'Reasoning': result.reasoning, 'Rating': result.rating}
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
print(ranking_df['Rating'])

def clean_and_average_rating(rating):
    if isinstance(rating, str):
        ratings = rating.strip('[]').split(',')
        average = sum([float(r) for r in ratings]) / len(ratings)
    elif isinstance(rating, list):
        average = sum([float(r) for r in rating]) / len(rating)
    else:
        average = None
    return average

ranking_df['Rating_Single'] = ranking_df['Rating'].apply(clean_and_average_rating)
ranking_df.to_excel(output_file_path, index=False)
print(f"Ranking results saved to {output_file_path}")
