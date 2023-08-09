import os
import torch
import torch.nn.functional as F
import numpy as np
import random
import json
import math
import sys
from typing import Iterable
import argparse
import time
import datetime
from util import dist
import torch
from torch.utils.data import DataLoader, DistributedSampler
from collections import namedtuple
from functools import reduce
import openai

from datasets import build_videoqa_dataset, videoqa_collate_fn
from model import build_model, get_tokenizer
from args import get_args_parser
from util.misc import get_mask, adjust_learning_rate
from util.metrics import MetricLogger
from model.deberta import DebertaV2ForMaskedLM
from transformers import (
    BertTokenizer,
    DebertaV2Tokenizer,
    DebertaV2Config,
    BertConfig,
    GPT2Tokenizer
)
import json
import re
from tqdm import tqdm
import pandas as pd
device = torch.device("cuda")

EGOSCHEMA_FOLDER = "../../EgoSchema"
WEIGHTS_PATH = "/home/raiymbek/frozenbilm_how2qa.pth"




def parse_args():
    """
    Parse the following arguments for a default parser
    """
    parser = argparse.ArgumentParser(
        description="Running experiments"
    )
    parser.add_argument(
        "--f",
        dest="frames",
        help="how much frames",
        default=10,
        type=int,
    )
    return parser.parse_args()


def bilm(q_uid, question, answer, wrong_answers, result):

    key = "full_bilm_pred"

    if key in result:
        return result[key] != 4, {}

    with torch.no_grad():
        try:
            video = torch.from_numpy(np.load(f"./features/{q_uid}.npy").astype("float32"))
        except:
            return {key:  -1} 
        
        if video.shape[0] != frame_count:
            return False, {key:  -1} 
        video = video.unsqueeze(0).cuda()
        video_mask = get_mask(
            torch.tensor(frame_count, dtype=torch.long).unsqueeze(0), video.size(1)
        ).cuda()
        
        if question[-1] != "?":
            question = question + "?"

        multiple_choice = [w.lower().strip() for w in wrong_answers]
        multiple_choice.append(answer.lower().strip())

        logits_list = []
        for choice in multiple_choice:
            text = f"Question: {question.capitalize()} Is it '{choice.capitalize()}'? {tokenizer.mask_token}."

            encoded = tokenizer(
                [text],
                add_special_tokens=True,
                max_length=300,
                padding="longest",
                truncation=True,
                return_tensors="pt")


            output = model(video=video,
                        video_mask=video_mask,
                        input_ids=encoded["input_ids"].to(device),
                        attention_mask=encoded["attention_mask"].to(device),
                        )

            logits = output["logits"]
            logits = logits[:, frame_count : encoded["input_ids"].size(1) + frame_count][encoded["input_ids"] == tokenizer.mask_token_id]
            logits_list.append(logits.softmax(-1)[:, 0].cpu())

        try: 
            yes_scores = torch.stack(logits_list, 1)[0]
        except Exception as e:
            print(logits_list)
            return {key: -1}
        
        prediction = int(torch.argmax(yes_scores).cpu())
            
        del video
        del video_mask
        del logits
        torch.cuda.empty_cache()
        
        if prediction != 4:
            return {key: prediction}
        return {key: prediction}

def main():
    result = []
    
    result_file_name = f"{frame_count}_bilm_accuracies"
    current_results = {}
    if os.path.isfile(f"{result_folder}/{result_file_name}.json"):
        current_results_f = open(f"{result_folder}/{result_file_name}.json") 
        current_results = json.load(current_results_f)
    print(len(current_results))
    q_uid_to_res = {res['q_uid']: res for res in current_results}
        
    for q_dict in tqdm(qa_data):
        q_uid = q_dict['q_uid']
        q = q_dict['question']
        options = [q_dict['option 0'], q_dict['option 1'], q_dict['option 2'], q_dict['option 3'], q_dict['option 4']]
        correct_answer = q_dict['corrent_answer']
        correct_option = options.pop(correct_answer)
        
        result = {}
        if q_uid in q_uid_to_res:
            result = q_uid_to_res[q_uid]
            continue
        
        result["q_uid"] = q_uid
        result["q"] = q
        result["a"] = correct_option
        result["w"] = options
               
        output = bilm(q_uid, q, correct_option, options, result)
        result.update(output)
        current_results[q_uid] = result
        with open(f"{result_folder}/{result_file_name}.json", 'w') as f:
            json.dump(current_results, f)
    
if __name__ == "__main__":
    args = parse_args()
        
    features_folder = f"./features/"
    frame_count = args.frames
        
    tokenizer = DebertaV2Tokenizer.from_pretrained("microsoft/deberta-v2-xlarge")
    model = DebertaV2ForMaskedLM.from_pretrained(
        features_dim=768,
        max_feats=frame_count,
        freeze_lm=False,
        freeze_mlm=False,
        ft_ln=False,
        ds_factor_attn=8,
        ds_factor_ff=8,
        dropout=0.1,
        n_ans=2,
        freeze_last=False,
        pretrained_model_name_or_path="microsoft/deberta-v2-xlarge",
        )

    checkpoint = torch.load("/home/raiymbek/frozenbilm_how2qa.pth", map_location="cpu")
    model.load_state_dict(checkpoint["model"], strict=False)
    
    model.cuda()
    model.eval()

    tok_yes = torch.tensor(tokenizer("Yes",
                                     add_special_tokens=False,
                                     max_length=1,
                                     truncation=True,
                                     padding="max_length",)["input_ids"],
                           dtype=torch.long,)

    tok_no = torch.tensor(tokenizer("No",
                                    add_special_tokens=False,
                                    max_length=1,
                                    truncation=True,
                                    padding="max_length",)["input_ids"],
                          dtype=torch.long,)


    a2tok = torch.stack([tok_yes, tok_no])
    model.set_answer_embeddings(
        a2tok.to(model.device), freeze_last=False
    )
        
    result_folder = f"bilm_results"
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)
        
    qa_data_f = open(f"{EGOSCHEMA_FOLDER}/questions_with_correct.json")
    qa_data = json.load(qa_data_f)
    
    main()
