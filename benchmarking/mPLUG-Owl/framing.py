import pandas as pd
import json
import time
import numpy as np
import random
import os
from tqdm import tqdm
import cv2 

import matplotlib.pyplot as plt

from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip, ffmpeg_resize
import argparse

import multiprocessing
from multiprocessing import Queue as multi_queue
import time

EGOSCHEMA_FOLDER = "../../EgoSchema"

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

def task(the_queue):
    while True:
        if the_queue.empty():
            break
            
        vid_name = the_queue.get()
        vid_path = f"{vid_dir}/{vid_name}.mp4"
        is_it_done = True
        if vid_name in extracted_vids:
            continue
        vid_folder = f"{frames_dir}/{vid_name}"        
        if not os.path.exists(vid_folder):
            os.mkdir(vid_folder)
        uploaded_frames = os.listdir(vid_folder)
        for i in range(frames):
            if f"{i}.jpg" not in uploaded_frames:
                is_it_done = False
        
        if is_it_done:
            continue

        try:
            video = VideoFileClip(vid_path)
        except:
            continue
        vid_frames = [f for f in video.iter_frames()]
        frames_sec = np.linspace(0, len(vid_frames)-1, num=frames)
        
        for f_i in range(len(frames_sec)):
            f = frames_sec[f_i]
            frame = vid_frames[int(f)]
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cv2.imwrite(f"{vid_folder}/image_{f_i+1}.jpg", frame)

def progress_task(initially_done, the_queue, to_do):
    global done_trigger
    print("Done: -1%. Time left: -1 seconds", flush=True, end='\r')
            
    start = time.time()
    while not the_queue.empty():
        time.sleep(1)
        done = to_do - the_queue.qsize()
            
        speed = done / (time.time() - start)
        rest = to_do - done
            
        if speed == 0:
            time_left = -1
        else:
            time_left = rest / speed
        
        print(f"Done: {100 * (initially_done + done) / (initially_done+to_do)}% Time left: {time_left / 3600} seconds", end='\r', flush = True)
    
if __name__ == "__main__":
    args = parse_args()
    frames = args.frames

    questions_f = open(f"{EGOSCHEMA_FOLDER}/questions_with_correct.json")
    questions = json.load(questions_f)

    vid_dir = f"{EGOSCHEMA_FOLDER}/videos"
    frames_dir = f"frames_{frames}"
    if not os.path.exists(frames_dir):
        os.mkdir(frames_dir)
    extracted_vids = [vid for vid in os.listdir(frames_dir) if "ipynb" not in vid and len([frame for frame in os.listdir(f"{frames_dir}/{vid}") if "ipynb" not in frame]) == 10]
    all_vids = [vid[:vid.find(".")] for vid in os.listdir(vid_dir) if "ipynb" not in vid]

    the_queue = multi_queue()
    for video_name in all_vids:
        if video_name not in extracted_vids:
            the_queue.put(video_name)
            
    initially_done = len(extracted_vids)
    to_do = len(all_vids) - initially_done
    progress_process = multiprocessing.Process(target=progress_task, args=(initially_done, the_queue, to_do))
    
    procceses = []
    for i in range(10):
        p1 = multiprocessing.Process(target=task, args=(the_queue,))
        procceses.append(p1)
        
    progress_process.start()
    for p in procceses:
        p.start()
        
    for p in procceses:
        p.join()
    done_trigger = True
    progress_process.join()

