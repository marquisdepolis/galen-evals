#!/bin/bash

# Run Python scripts in sequence
# python3 galen_llm_eval_gpt.py
python3 results_convert.py
python3 galen_eval_gpt4.py
