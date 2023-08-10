import os
import torch
from peft import LoraConfig, TaskType, get_peft_config, get_peft_model
from transformers.models.llama.configuration_llama import LlamaConfig
from transformers.models.llama.tokenization_llama import LlamaTokenizer

from mplug_owl.configuration_mplug_owl import mPLUG_OwlConfig
from mplug_owl.modeling_mplug_owl import (ImageProcessor,
                                          mPLUG_OwlForConditionalGeneration)
from mplug_owl.tokenize_utils import tokenize_prompts
import numpy as np
import pandas as pd
from tqdm import tqdm
import json
import random
import argparse

EGOSCHEMA_FOLDER = "../../../"
CHECKPOINT_PATH = "instruction_tuned.pht"
TOKENIZER_PATH = "tokenizer.pht"

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
        help="frame_num",
        default="",
        type=int,
    )
    parser.add_argument(
        "--g",
        dest="gpu",
        help="gpu to use",
        default="0",
        type=str,
    )

    return parser.parse_args()

def get_model(checkpoint_path=None, tokenizer_path=None, peft_config=None, device='cuda', dtype=torch.bfloat16):

    config = mPLUG_OwlConfig()
    model = mPLUG_OwlForConditionalGeneration(config=config)
    model.eval()

    if checkpoint_path is not None:
        tmp_ckpt = torch.load(
            checkpoint_path, map_location='cpu')
        if peft_config is not None:
            print('convert to LoRA model')
            model = get_peft_model(model, peft_config=peft_config)
        msg = model.load_state_dict(tmp_ckpt, strict=False)
        print(msg)

    assert tokenizer_path is not None
    tokenizer = LlamaTokenizer(
        tokenizer_path, pad_token='<unk>', add_bos_token=False)
    tokenizer.eod_id = tokenizer.eos_token_id
    img_processor = ImageProcessor()

    model = model.to(dtype)
    model = model.to(device)
    return model, tokenizer, img_processor


if __name__ == '__main__':
    args = parse_args()
    os.environ["CUDA_VISIBLE_DEVICES"]=args.gpu
    torch.cuda.empty_cache()
    with torch.no_grad():
        model, tokenizer, img_processor = get_model(checkpoint_path=CHECKPOINT_PATH, 
                                                    tokenizer_path=TOKENIZER_PATH)
    model = model.eval()
    f = open('q_prompt.txt','r')
    qa_prompt = f.read()
    questions_f = open(f"{EGOSCHEMA_FOLDER}/questions_with_correct.json")
    questions = json.load(questions_f)
    frames = args.frames
    folder = f"frames_{frames}"

    correct = 0
    total = 0
    try:
        results_path = f"save_result_{frames}.json"
        dataset_file = open(results_path)
        results = json.load(dataset_file)
    except:
        results = {}

    YES_EMBED = [3869, 22483]
    for q_dict in tqdm(questions):
        q_uid = q_dict['q_uid']
        q = q_dict['question']
        options = [q_dict['option 0'], q_dict['option 1'], q_dict['option 2'], q_dict['option 3'], q_dict['option 4']]
        correct_answer = q_dict['correct_answer']
        correct_option = options.pop(correct_answer)
    
        if q_uid in results:
            continue
    
        aw_options = [correct_option] + options
        confidence = []
            
        for option in aw_options:
            qa_string = f"Given question '{q}, is answer '{option}' correct?"
            images_folder = f"{folder}/{q_uid}"
            images_paths = [f"{images_folder}/{im}" for im in os.listdir(images_folder) if "ipynb" not in im]
        
            image_string = ""
            for f_i in range(frames):
               image_string += "Human: <image>\n"
                
            prompts = [
            f'''The following is a conversation between a curious human and AI assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.
            {image_string}
            Human: {qa_string}
            Human: {qa_prompt}
            AI:''']
            image_list = images_paths
        
            dtype = torch.bfloat16
            device='cuda'
            tokens_to_generate = 0
            add_BOS = True
            context_tokens_tensor, context_length_tensorm, attention_mask = tokenize_prompts(
                prompts=prompts, tokens_to_generate=tokens_to_generate, add_BOS=add_BOS, tokenizer=tokenizer, ignore_dist=True)
            images = img_processor(image_list).to(dtype)
            model.eval()
            images = images.to(device)
            context_tokens_tensor = context_tokens_tensor.to(device)
            attention_mask = attention_mask.to(device)
            with torch.no_grad():
                res = model.generate(input_ids=context_tokens_tensor, pixel_values=images,
                                     attention_mask=attention_mask, max_length=512, top_k=5, do_sample=True, output_scores=True, return_dict_in_generate=True)
            sentence_embeddings = res.sequences
            sentence = tokenizer.decode(sentence_embeddings.tolist()[0], skip_special_tokens=True)
            scores = res.scores
    
            if " no " in " " + sentence.lower():
                print(sentence)

            is_there_yes = False
            for yes_embeddings in YES_EMBED:
                if yes_embeddings in sentence_embeddings:
                    is_there_yes = True
                    yes_index = sentence_embeddings.tolist()[0].index(yes_embeddings)
                    conf = scores[yes_index - 1][0][yes_embeddings].type(torch.cuda.FloatTensor)
                    #print(conf.cpu())
                    confidence.append(conf.cpu().numpy())
                    break
    
            if not is_there_yes:
                confidence.append(0)
    
        best_score = np.max(confidence)
        the_best = [i for i in range(5) if confidence[i] == best_score]
        if len(the_best) == 1:
            best = the_best[0]
        else:
            best = random.choice(the_best)
        results[q_uid] = str(best)

        with open(f"save_result_{frames}.json", 'w') as f:
            json.dump(results, f)