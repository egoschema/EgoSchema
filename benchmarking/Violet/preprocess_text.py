import json
import random
import argparse
import os
import pandas as pd

def preprocess_text(input_file_path):
    output_file_path = os.path.dirname(input_file_path) + "/txt_egoSchema-mc.json"
    df = pd.read_csv(input_file_path)

    # Create output JSON file data
    output_data = {"train": [], "val": [], "test": []}
    output_set_data = []
    for _, row in df.iterrows():
        clip_id = row["clip_id"]
        question = row["question"]
        correct_ans = row["correct_answer"]
        wa_1 = row["wrong_answer_1"]
        wa_2 = row["wrong_answer_2"]
        wa_3 = row["wrong_answer_3"]
        wa_4 = row["wrong_answer_4"]
        all_answers = [correct_ans, wa_1, wa_2, wa_3, wa_4]
        random.shuffle(all_answers)
        correct_ans_idx = all_answers.index(correct_ans)

        # Assign options in shuffled order
        output_row = {
            "question": question,
            "option_0": all_answers[0],
            "option_1": all_answers[1],
            "option_2": all_answers[2],
            "option_3": all_answers[3],
            "option_4": all_answers[4],
            "answer": correct_ans_idx,
            "video": clip_id
        }

        # Add processed data to output set
        output_set_data.append(output_row)
    output_data["test"] = output_set_data
    # Save output JSON file
    with open(output_file_path, 'w') as output_file:
        json.dump(output_data, output_file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process JSON input file and create shuffled output JSON file')
    parser.add_argument('--input_file', type=str, help='Path to input CSV file')
    args = parser.parse_args()

    # Process input file and save output files
    preprocess_text(args.input_file)