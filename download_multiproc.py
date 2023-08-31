import requests
import os
import json
import time
import argparse
import multiprocessing
from moviepy.editor import VideoFileClip
import signal
import sys
from tqdm import tqdm

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Download dataset segments.")
    parser.add_argument("--p", dest="process_num", default=4, type=int, help="Number of processes")
    return parser.parse_args()

def download_from_wasabi(url, destination, retries=3):
    """Download a file from the given URL and save it to the destination path."""
    for _ in range(retries):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(destination, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=1024*1024):
                    fd.write(chunk)
            return True
        except requests.RequestException as e:
            print(f"[ERROR] Issue downloading video: {e}. Retrying...")
    print("[WARNING] Please update uid_to_url.json. The URLs seem outdated.")
    return False

def progress_task(initially_done, the_queue, to_do):
    """Print the progress of tasks being done."""
    start = time.time()
    while not the_queue.empty():
        time.sleep(1)
        done = to_do - the_queue.qsize()
        speed = done / (time.time() - start)
        rest = to_do - done
        time_left = rest / speed if speed else -1
        print(f"Done: {100 * (initially_done + done) / (initially_done + to_do)}%. Time left: {time_left / 60:.2f} minutes", end='\r', flush=True)

def task(the_queue, uid_to_url):
    """Download task using multiprocessing."""
    while not the_queue.empty():
        q_one = the_queue.get()
        download_from_wasabi(uid_to_url[q_one], os.path.join("videos", f"{q_one}.mp4"))

def validate_download():
    """Validate the integrity of downloaded videos."""
    uploaded = set([vid.split(".")[0] for vid in os.listdir("./videos")])
    for video in tqdm(questions):
        video_name = video['q_uid']
        drive_id = video['google_drive_id']
        if video_name not in uploaded:
            continue
        try:
            _ = VideoFileClip(os.path.join("videos", f"{video_name}.mp4"))
        except Exception as e:
            print(f"[ERROR] {e}\nRemoving: {video_name}")
            os.remove(os.path.join("videos", f"{video_name}.mp4"))
            time.sleep(1)
            print(f"[INFO] Problems with {video_name}. Download manually at: https://drive.google.com/file/d/{drive_id}/view?usp=drivesdk")
            print("----------")

def signal_handler(sig, frame):
    """Handle termination signals."""
    print("[INFO] Stopping all processes.")
    for child in multiprocessing.active_children():
        child.terminate()
    sys.exit(0)

if __name__ == "__main__":
    args = parse_args()

    # Load necessary JSON files
    with open("questions.json") as questions_f:
        questions = json.load(questions_f)

    with open("uid_to_url.json") as uid_to_url_f:
        uid_to_url = json.load(uid_to_url_f)

    uploaded = set([vid.split(".")[0] for vid in os.listdir("videos")])
    signal.signal(signal.SIGINT, signal_handler)

    the_queue = multiprocessing.Queue()
    for q in questions:
        q_uid = q["q_uid"]
        if q_uid not in uploaded:
            the_queue.put(q_uid)

    initially_done = len(uploaded)
    to_do = len(questions) - initially_done

    # Start multiprocessing processes
    progress_process = multiprocessing.Process(target=progress_task, args=(initially_done, the_queue, to_do))
    processes = [multiprocessing.Process(target=task, args=(the_queue, uid_to_url)) for _ in range(args.process_num)]
    
    progress_process.start()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    progress_process.join()

    print("\n[INFO] Validating clips.")
    validate_download()