import warnings

from sklearn import ensemble
warnings.filterwarnings("ignore", "Detected call of", UserWarning)
import os
import copy
import pytorch_lightning as pl
from CoTrain.config import ex
from CoTrain.modules import CLIP
from CoTrain.datamodules.video.multitask_datamodule import MTDataModule
import datetime
from pytorch_lightning.utilities.cloud_io import get_filesystem
from pytorch_lightning.utilities.cloud_io import load as pl_load

import torch
import numpy as np
from pytorch_lightning.strategies import DDPStrategy
from tqdm import tqdm
import random
import argparse
import json
torch.manual_seed(0)

ViT = '/old_home_that_will_be_deleted_at_some_point/raiymbek/InternVideo/Downstream/multi-modalities-downstream/ViT-L-14.pt'
MSRVTT = '/old_home_that_will_be_deleted_at_some_point/raiymbek/InternVideo/Downstream/multi-modalities-downstream/MSRVTT.ckpt'

CONFIG = {'exp_name': 'clip_kc_nc_finetune_msrvttchoice', 
          'seed': 0, 
          'video_datasets': ['msrvtt_choice'], 
          'image_datasets': [], 
          'val_datasets': [], 
          'loss_names': {'vtm': 0, 
                         'mlm': 0, 
                         'mpp': 0, 
                         'vtc': 0, 
                         'vcop': 0, 
                         'dino': 0, 
                         'vqa': 0, 
                         'openend_vqa': 0, 
                         'mc_vqa': 0, 
                         'nlvr2': 0, 
                         'irtr': 0, 
                         'multiple_choice': 1, 
                         'vcr_q2a': 0, 
                         'zs_classify': 0, 
                         'contrastive': 0, 
                         'cap': 0, 
                         'mim': 0}, 
          'val_loss_names': {'vtm': 0, 
                             'mlm': 0, 
                             'mpp': 0, 
                             'vtc': 0, 
                             'vcop': 0, 
                             'dino': 0, 
                             'vqa': 0, 
                             'openend_vqa': 0, 
                             'mc_vqa': 1, 
                             'nlvr2': 0, 
                             'irtr': 0, 
                             'multiple_choice': 0, 
                             'vcr_q2a': 0, 
                             'zs_classify': 0, 
                             'contrastive': 0, 
                             'cap': 0, 
                             'mim': 0}, 
          'batch_size': 1, 
          'linear_evaluation': False, 
          'draw_false_image': 1, 
          'train_transform_keys': ['pixelbert'], 
          'val_transform_keys': ['pixelbert'], 
          'image_size': 224, 
          'patch_size': 16, 
          'max_image_len': -1, 
          'draw_false_video': 1, 
          'video_only': False, 
          'num_frames': None, 
          'vqav2_label_size': 3129, 
          'msrvttqa_label_size': 1501, 
          'max_text_len': 77, 
          'tokenizer': 'bert-base-uncased', 
          'vocab_size': 30522, 
          'whole_word_masking': False, 
          'mlm_prob': 0.15, 
          'draw_false_text': 5, 
          'draw_options_text': 0, 
          'vit': 'vit_base_patch16_224', 
          'hidden_size': 768, 
          'num_heads': 12, 
          'num_layers': 12, 
          'mlp_ratio': 4, 
          'drop_rate': 0.1, 
          'shared_embedding_dim': 512, 
          'save_checkpoints_interval': 1, 
          'optim_type': 'adamw', 
          'learning_rate': 0.0001, 
          'weight_decay': 0.01, 
          'decay_power': 1, 
          'max_epoch': 10, 
          'max_steps': 25000, 
          'warmup_steps': 0.1, 
          'end_lr': 0, 
          'lr_mult': 1, 
          'backend': 'a100', 
          'get_recall_metric': False, 
          'get_ind_recall_metric': False, 
          'retrieval_views': 3, 
          'resume_from': None, 
          'fast_dev_run': False, 
          'val_check_interval': 0.5, 
          'test_only': True, 
          'data_root': './meta_data/',
          'log_dir': '/result/', 
          'per_gpu_batchsize': 1, 
          'num_gpus': 1, 
          'num_nodes': '', 
          'load_path': MSRVTT, 
          'num_workers': 1, 
          'precision': 16, 
          'model_dir': '//models/', 
          'clip': ViT, 
          'clip_type': 'kc_new', 
          'clip_freeze': False, 
          'clip_freeze_text': False, 
          'clip_dpr': 0.0, 
          'prompt_type': 'all', 
          'clip_lr_mult': 1, 
          'clip_no_pretrain': False, 
          'clip_grad_unfreeze_int': 0, 
          'clip_evl_dropout': 0.5, 
          'mim_prob': 0.9, 
          'clip_mlm_decoder_n_layers': 4, 
          'clip_mim_decoder_n_layers': 4, 
          'clip_mim_decoder_width': 512, 
          'clip_cap_decoder_n_layers': 4, 
          'clip_init_zero': True, 
          'clip_qa_type': 'vtc', 
          'clip_mc_type': 'vtc', 
          'clip_wiseft_coef': 0.5,
          'clip_mmt': False, 
          'clip_alt_data': False, 
          'image_data_mult': 1,
          'clip_cls_dropout': 0.5,
          'save_last': True, 
          'save_top_k': 1, 
          'clip_use_checkpoint': False,
          'clip_checkpoint_num': [0, 0, 0], 
          'clip_momentum_ckpt': 1, 
          'clip_momentum_interval': 1}

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


if __name__ == '__main__':
    args = parse_args()
    CONFIG['num_frames'] = args.frames
    frames = args.frames
    os.environ["CUDA_VISIBLE_DEVICES"]=args.gpu
    torch.cuda.empty_cache()
    dm = MTDataModule(CONFIG, dist=False)
    model = CLIP(CONFIG)
    model.current_tasks = ['multiple_choice']
    model = model.eval()
    dm.prepare_data()
    dm.setup("test")
    loader = dm.test_dataloader()
    batch_gen = iter(loader)
        
    try:
        results_path = f"InternVid_save_result_{frames}.json"
        dataset_file = open(results_path)
        results = json.load(dataset_file)
    except:
        results = {}
        
    random.seed(1998)
    i = 0
    for batch in tqdm(batch_gen):
        if batch['q_uid'][0] in results:
            seed_continuity = random.choice([0])
            continue
        res = model(batch)
        best_score = torch.max(res['score'][0])
        the_best = [i for i in range(5) if res['score'][0][i] == best_score]
        if len(the_best) == 1:
            seed_continuity = random.choice([0])
            best = the_best[0]
        else:
            best = random.choice(the_best)
        results[batch['q_uid'][0]] = best
        i+=1

        with open(f"InternVid_save_result_{frames}.json", 'w') as f:
            json.dump(results, f)