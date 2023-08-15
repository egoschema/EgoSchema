import pandas as pd
import os
import numpy as np 
import argparse

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
    
if __name__ == "__main__":
    args = parse_args()
    frames = args.frames

    if not os.path.exists(f"features"):
        print("making folder")
        os.mkdir(f"features")
        
    total = 0
    VID_PATH = f"{EGOSCHEMA_FOLDER}/videos"
    
    to_add = []
    for q_uid in os.listdir(f"{VID_PATH}"):
        if not os.path.exists(f"{VID_PATH}/{q_uid[:q_uid.rfind('.')]}.npy"):
            to_add.append(q_uid[:q_uid.rfind('.')])
            total += 1

    import torch
    for q_uid in os.listdir(f"./features/"):
        if torch.from_numpy(np.load(f"./features/{q_uid}").astype("float32")).shape[0] != frames:
            to_add.append(q_uid[:q_uid.rfind('.')])
            print(q_uid)

    table = []
    columns = ["video_path", "feature_path"]
    
    
    for q_uid_mp4 in os.listdir(f"{VID_PATH}"):
        q_uid = q_uid_mp4[:q_uid_mp4.rfind(".")]
        if "ipynb" in q_uid_mp4:
            continue
            
        if q_uid not in to_add:
            continue
        row = [f"{VID_PATH}/"+ q_uid_mp4, f"./features/" + q_uid]
        table.append(row)

    df = pd.DataFrame(table,columns=columns)
    df.to_csv("test_additional_paths.csv", index=False)

    import torch as th
    import math
    import numpy as np
    import torch.nn.functional as F
    from tqdm import tqdm
    import argparse
    from extract.video_loader import VideoLoader
    from torch.utils.data import DataLoader
    from extract.preprocessing import Preprocessing
    from extract.random_sequence_shuffler import RandomSequenceSampler
    from args import MODEL_DIR
    import clip

    dataset = VideoLoader(
        "test_additional_paths.csv",
        framerate = frames / 180,  # one feature per second max
        size=224,
        centercrop=True,
    )

    n_dataset = len(dataset)
    sampler = RandomSequenceSampler(n_dataset, frames)
    loader = DataLoader(
        dataset,
        batch_size=1,
        shuffle=False,
        num_workers=10,
        sampler=sampler if n_dataset > 10 else None,
    )

    preprocess = Preprocessing()
    model, _ = clip.load("ViT-L/14", download_root=MODEL_DIR)
    model.eval()
    model = model.cuda()

    with th.no_grad():
        for k, data in enumerate(loader):
            input_file = data["input"][0]
            output_file = data["output"][0]
            if len(data["video"].shape) > 3:
                print(
                    "Computing features of video {}/{}: {}".format(
                        k + 1, n_dataset, input_file
                    )
                )
                video = data["video"].squeeze()
                if len(video.shape) == 4:
                    video = preprocess(video)
                    n_chunk = len(video)
                    features = th.cuda.FloatTensor(n_chunk, 768).fill_(0)
                    n_iter = int(math.ceil(n_chunk / float(128)))
                    for i in tqdm(range(n_iter)):
                        min_ind = i * 128
                        max_ind = (i + 1) * 128
                        video_batch = video[min_ind:max_ind].cuda()
                        batch_features = model.encode_image(video_batch)
                        if 0:
                            batch_features = F.normalize(batch_features, dim=1)
                        features[min_ind:max_ind] = batch_features
                    features = features.cpu().numpy()
                    if 1:
                        features = features.astype("float16")
                    np.save(output_file, features)
            else:
                print("Video {} already processed.".format(input_file))

    
