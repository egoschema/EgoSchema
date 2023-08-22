# EgoSchema Dataset

## A Diagnostic Benchmark for Very Long-form Video Language Understanding
**Authors**: Karttikeya Mangalam, Raiymbek Akshulakov, Jitendra Malik

[Webpage](https://egoschema.github.io/) :globe_with_meridians: | [Paper](https://arxiv.org/abs/2308.09126) :newspaper: | [Video](https://youtu.be/_VVoiSzb5E4) :movie_camera:

<br/>

<p align="center">
<a href="http://www.youtube.com/watch?feature=player_embedded&v=_VVoiSzb5E4" target="_blank"><img src="http://img.youtube.com/vi/_VVoiSzb5E4/0.jpg" alt="EgoSchema Video" width="80%" height="80%" border="10" /></a>
</p>

EgoSchema is an avant-garde dataset designed to assess the capabilities of contemporary vision and language systems in understanding long videos. Originating from Ego4D, the EgoSchema dataset encompasses over 5,000 human-curated multiple-choice question-answer pairs, which span more than 250 hours of authentic video data, capturing a vast spectrum of human activity and behavior. Our dataset introduces "temporal certificate sets," a novel concept intended to capture the intrinsic temporal understanding length inherent to a diverse range of video understanding tasks and datasets.

:exclamation: The intrinsic temporal lengths in EgoSchema exceed those of the second closest dataset by over 5.7 times and are between 10 to 100 times longer than several other datasets.<br/><br/>
:exclamation: Even the most recent, high-caliber video and language models, boasting billions of parameters, falter on this dataset, achieving a mere QA accuracy of less than 33% (in comparison to the 20% expected from random choice). In contrast, human performance sits at around 76% accuracy.<br/><br/>
:exclamation: EgoSchema has been crafted to serve as a foundational dataset for the next wave of advanced long-term video understanding systems.<br/><br/>

## Downloading the Dataset

Follow these instructions to download the dataset :point_down::

- ### Download the `uid_to_url.json` file from [EgoSchema Google Drive](https://drive.google.com/drive/folders/1SS0VVz8rML1e5gWq7D7VtP1oxE2UtmhQ?usp=sharing)

This file will be updated weekly as the links expire every 7 days. You will receive a warning if your file becomes outdated.

- ### Execute the following commands:

```bash
conda create -n egoschema_download python=3.8 
conda activate egoschema_download
conda install tqdm simplejson requests
pip install moviepy
mkdir videos
python download.py
```
This will retrieve the dataset and store it in the `videos` directory. Video names correspond to the `q_uid` key in the `questions.json` file. If any files encounter issues during installation, rerun the `download.py` script. If problems persist, links to the necessary files will be provided via Google Drive.

- ### Direct Download (Alternative):

Directly download the zipped file from the [EgoSchema Google Drive](https://drive.google.com/drive/folders/1SS0VVz8rML1e5gWq7D7VtP1oxE2UtmhQ?usp=sharing).

- ### Multiprocessing Script (Alternative):

```bash
conda create -n egoschema_download python=3.8 
conda activate egoschema_download
conda install tqdm simplejson requests
pip install moviepy
mkdir videos
python download_multiproc.py --p <number of processes>
```

This script accelerates the download process by running multiple processes concurrently. Please be aware that this method might hit the rate limit. If the script fails after running for a while, revert to the `download.py` script.

## Benchmarking EgoSchema

For those keen on benchmarking using the EgoSchema dataset, detailed instructions for various models have been compiled. Navigate to the `benchmarking` directory for comprehensive guides and setup processes for each model. Please note that all benchmarking codes will require the correct answers to the questions, which will be made available soon.
