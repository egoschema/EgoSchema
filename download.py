import requests
import os
import json
from tqdm import tqdm
import time
import gdown
#os.environ["IMAGEIO_FFMPEG_EXE"] = "../../../ffmpeg-git-20220910-amd64-static/ffmpeg"
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip, ffmpeg_resize

def download_from_google_drive(file_id, destination):
    url = f'https://drive.google.com/uc?id={file_id}'
    gdown.download(url,  destination, quiet=True)
    time.sleep(2)

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


if __name__ == "__main__":

    questions_f = open("questions.json")
    questions = json.load(questions_f)

    print("Validating clips that are already uploaded")
    validate_download(False)

    for q in tqdm(questions):
        q_uid = q["q_uid"]
        google_drive_id = q['google_drive_id']

        if os.path.exists(f"videos/{q_uid}.mp4"):
            continue
            
        download_from_google_drive(google_drive_id, f"videos/{q_uid}.mp4")
        time.sleep(1)

    print("Validating clips")
    validate_download(True)

        
            
