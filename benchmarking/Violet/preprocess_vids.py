import os
import pickle
import pandas as pd
import json
import multiprocessing as mp
import cv2
import base64
import argparse
from tqdm import tqdm
import random

def process_video(input_vals):
    """Given a clip_id, extract n_frames frames from the video
    and return them as a list of strings"""
    clip_id, n_frames, videos_dir = input_vals

    clip_path = os.path.join(videos_dir, f"{clip_id}.mp4")
    cap = cv2.VideoCapture(clip_path)
    frames = []
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    indices = sorted(random.sample(range(frame_count), n_frames))
    for i in indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_string = base64.b64encode(img_encoded).decode('utf-8')
            frames.append(img_string)
    cap.release()

    return clip_id, width, height, frames

def process_csv(n_frames, videos_dir):
    questions_f = open(f"../../../../questions_with_correct.json")
    questions = json.load(questions_f)
    
    tsv_file_path = "./img_egoSchema.tsv"
    pickle_file_path = "./img_egoSchema.id2lineidx.pkl"

    num_processes = mp.cpu_count()
    print("Using {} Processes".format(num_processes))
    pool = mp.Pool(processes=num_processes)
    rows = []

    # extract Clip IDs
    data_points = []
    for row in questions:
        clip_id = row['q_uid']
        data_points.append((clip_id, n_frames, videos_dir))

    with tqdm(total=len(questions)) as pbar:
        for i, processed_video in enumerate(pool.imap(process_video, [data_point for data_point in data_points])):
            rows.append(processed_video)
            pbar.update()
    pool.close()
    pool.join()

    rows = [[row[0], str({"class": -1, "width": row[1], "height": row[2]})] + row[3] for row in rows if len(row[3]) > 0]

    pickle_res = {}
    with open(tsv_file_path, 'w') as tsv_file:
        for i, row in enumerate(rows):
            tsv_file.write('\t'.join(row) + '\n')
            pickle_res[row[0]] = i
    with open(pickle_file_path, 'wb') as f:
        pickle.dump(pickle_res, f)
            

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Preprocess the clips by converting them to strings and storing in a TSV file')
    parser.add_argument('--videos_dir', type=str, help='Path to directory where videos are located')
    parser.add_argument('--n_frames', type=int, default=250, help='Number of frames to extract from video')
    parser.add_argument('--num_proc', type=int, default=8, help='Number of process to run')
    args = parser.parse_args()

    # Process input file and save output files
    process_csv(args.n_frames, args.videos_dir)
    