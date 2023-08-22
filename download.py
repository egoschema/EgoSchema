import requests
import os
import json
from tqdm import tqdm
import time
from moviepy.editor import VideoFileClip

def download_from_wasabi(url, destination, retries=3):
    """Download a file from the given URL and save it to the destination path."""
    for _ in range(retries):
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Raise an exception for HTTP errors

            # Save the video in chunks
            with open(destination, 'wb') as fd:
                for chunk in response.iter_content(chunk_size=1024*1024):  # 1MB chunks
                    fd.write(chunk)
            return True
        except requests.RequestException as e:
            print(f"[ERROR] Issue downloading video: {e}. Retrying...")
    print("[WARNING] Please update uid_to_url.json. The URLs seem outdated.")
    return False


def validate_download(questions):
    """Check the integrity of downloaded videos and remove corrupted files."""
    uploaded = set([vid.split(".")[0] for vid in os.listdir("videos")])
    
    for video in tqdm(questions):
        video_name = video['q_uid']
        drive_id =  video['google_drive_id']

        if video_name not in uploaded:
            continue
            
        try:
            _ = VideoFileClip(os.path.join("videos", f"{video_name}.mp4"))
        except Exception:
            print(f"[ERROR] Issue with {video_name}.mp4. Removing...")
            os.remove(os.path.join("videos", f"{video_name}.mp4"))
            time.sleep(1)
            print(f"[INFO] Having issues with {video_name}. Please rerun the download script or manually download from: https://drive.google.com/file/d/{drive_id}/view?usp=drivesdk")


if __name__ == "__main__":
    # Load necessary JSON files
    with open("questions.json") as questions_f:
        questions = json.load(questions_f)

    with open("uid_to_url.json") as uid_to_url_f:
        uid_to_url = json.load(uid_to_url_f)

    # Download videos
    for q in tqdm(questions):
        q_uid = q["q_uid"]

        if not os.path.exists(os.path.join("videos", f"{q_uid }.mp4")):
            download_from_wasabi(uid_to_url[q_uid], os.path.join("videos", f"{q_uid}.mp4"))
            time.sleep(1)

    # Validate the integrity of downloaded videos
    print("[INFO] Validating clips...")
    validate_download(questions)
