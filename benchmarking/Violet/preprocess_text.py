import json
import random
import argparse
import os
import pandas as pd

EGOSCHEMA = "../../../../"

def preprocess_text():
    output_file_path = "./txt_egoSchema-mc.json"
    questions_f = open(f"{EGOSCHEMA}/questions_with_correct.json")
    questions = json.load(questions_f)

    # Create output JSON file data
    output_data = {"train": [], "val": [], "test": []}
    output_set_data = []
    for row in questions:
        q_uid = row["q_uid"]
        question = row['question']
        options = [row['option 0'], row['option 1'], row['option 2'], row['option 3'], row['option 4']]
        correct_answer = row['correct_answer']

        # Assign options in shuffled order
        output_row = {
            "question": question,
            "option_0": options[0],
            "option_1": options[1],
            "option_2": options[2],
            "option_3": options[3],
            "option_4": options[4],
            "answer": correct_answer,
            "video": q_uid
        }

        # Add processed data to output set
        output_set_data.append(output_row)
    output_data["test"] = output_set_data
    # Save output JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(output_data, output_file)

if __name__ == '__main__':
    preprocess_text()