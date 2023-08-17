import requests
import os
import json
from tqdm import tqdm
import multiprocessing
from multiprocessing import Queue as multi_queue
import time
import argparse
import os
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip, ffmpeg_resize
from multiprocessing import active_children
import signal

def parse_args():
    """
    Parse the following arguments for a default parser
    """
    parser = argparse.ArgumentParser(
        description="Getting dataset on dataset segment"
    )
    
    parser.add_argument(
        "--p",
        dest="process_num",
        help="number of processes",
        default=4,
        type=int,
    )
    return parser.parse_args()

def download_from_google_drive(file_id, destination):
    base_url = "https://drive.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(base_url, params={'id': file_id}, stream=True)
    token = None
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            token = value
            break

    if token:
        response = session.get(base_url, params={'id': file_id, 'confirm': token}, stream=True)

    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)


def progress_task(initially_done, the_queue, to_do):
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
        
        print(f"Done: {100 * (initially_done + done) / (initially_done + to_do)}%. Time left: {time_left / 60} minutes", end='\r', flush = True)

def task(the_queue):
    while True:
        if the_queue.empty():
            break

        q_one = the_queue.get()
        google_drive_id = q_one['google_drive_id']
        download_from_google_drive(google_drive_id, f"videos/{q_one['q_uid']}.mp4")

def validate_download(to_print):
    uploaded = set([vid[:vid.find(".")] for vid in os.listdir("./videos")])
    for video in tqdm(questions):
        video_name = video['q_uid']
        drive_id =  video['google_drive_id']

        if video_name not in uploaded:
            continue
            
        try:
            clip = VideoFileClip(f"videos/{video_name}.mp4")
        except Exception as e:
            print(e)
            if to_print:
                print(f"Print: removing: {video_name}")
            time.sleep(1)
            os.remove(f"videos/{video_name}.mp4")
            if to_print:
                print(f"Having problems with downloading {video_name}. Please install it manually at https://drive.google.com/file/d/{drive_id}/view?usp=drivesdk")
                print(f"---------------------------------")

def signal_handler(sig, frame):
    print("Stopping all the processes")
    active = active_children()
    for child in active:
        child.terminate()
    sys.exit(0)
    

if __name__ == "__main__":
    args = parse_args()

    questions_f = open("questions.json")
    questions = json.load(questions_f)

    q_uid_to_drive = {q['q_uid']:q['google_drive_id'] for q in questions}

    uploaded = set([vid[:vid.find(".")] for vid in os.listdir("./videos")])
    signal.signal(signal.SIGINT, signal_handler)

    print("Validating clips that are already uploaded")
    validate_download(False)

    the_queue = multi_queue()
    for q in questions:
        q_uid = q["q_uid"]

        if q_uid not in uploaded:
            the_queue.put(q)

    initially_done = len(uploaded)
    to_do = len(questions) - 1 - initially_done
    progress_process = multiprocessing.Process(target=progress_task, args=(initially_done, the_queue, to_do))

    procceses = []
    for i in range(args.process_num):
        p1 = multiprocessing.Process(target=task, args=(the_queue,))
        procceses.append(p1)
        
    progress_process.start()
    for p in procceses:
        p.start()
        
    for p in procceses:
        p.join()
    progress_process.join()

    print("Validating clips")
    validate_download(True)

        
            
