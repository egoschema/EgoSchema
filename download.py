import requests
import os
import json
from tqdm import tqdm

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

    content_length_drive = int(dict(response.headers).get("Content-Length", 0))
    
    with open(destination, "wb") as f:
        for chunk in response.iter_content(32768):
            if chunk:
                f.write(chunk)

    downloaded_file_size = len(open(destination, 'rb').read())
    
    if content_length_drive == downloaded_file_size:
        #print("Download validation successful!")
        return True
    else:
        #print("Download validation failed. Sizes don't match.")
        return False


def validate_download(file_id, destination):
    drive_file_size_url = f"https://drive.google.com/get_video_info?docid={file_id}"
    response = requests.get(drive_file_size_url)
    content_length_drive = int(dict(response.headers).get("Content-Length", 0))
    downloaded_file_size = len(open(destination, 'rb').read())
    
    if content_length_drive == downloaded_file_size:
        #print("Download validation successful!")
        return True
    else:
        #print("Download validation failed. Sizes don't match.")
        return False


if __name__ == "__main__":

    questions_f = open("questions.json")
    questions = json.load(questions_f)

    for q in tqdm(questions):
        q_uid = q["q_uid"]
        google_drive_id = q['google_drive_id']

        if os.path.exists(f"videos/{q_uid}.mp4"):
            continue

        downloaded = False
        for trial in range(5):
            downloaded = download_from_google_drive(google_drive_id, f"videos/{q_uid}.mp4")
            if downloaded:
                break

        if not downloaded:
            print(f"Having problems with downloading {q_uid}. Please install it manually at https://drive.google.com/file/d/{google_drive_id}/view?usp=drivesdk")
            if os.path.exists(f"videos/{q_uid}.mp4"):
                os.remove(f"videos/{q_uid}.mp4")

        
            
