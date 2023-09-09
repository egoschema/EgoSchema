# EgoSchema Dataset Download Repository 
 
<h2 align="center">  EgoSchema: A Diagnostic Benchmark for Very Long-form Video 
Language Understanding </h2>

<p align="center">
    <a href="https://karttikeya.github.io/)">Karttikeya Mangalam</a>,  <a href="https://www.linkedin.com/in/raiymbek-akshulakov)">Raiymbek Akshulakov</a>,  <a href="https://people.eecs.berkeley.edu/~malik/)">Jitendra Malik</a> 
</p>
<p align="center"> Berkeley AI Research, UC Berkeley </p>

:globe_with_meridians: [Webpage](https://egoschema.github.io/)  | :book: [Paper](https://arxiv.org/abs/2308.09126)  | :movie_camera: [Teaser Video](https://youtu.be/_VVoiSzb5E4)  | :microphone: [4-min Podcast](https://www.podbean.com/media/share/pb-sj7gk-148d8bc?)  |  :speaking_head: [Overview Talk Video]() | :bar_chart: [Statistics Dashboard](https://public.tableau.com/views/EgoSchema/EGOSchema?:showVizHome=no)| :crossed_swords: [Kaggle](https://www.kaggle.com/competitions/egoschema-public/overview)

<br/>

<p align="center">
<a href="http://www.youtube.com/watch?feature=player_embedded&v=_VVoiSzb5E4" target="_blank"><img src="http://img.youtube.com/vi/_VVoiSzb5E4/0.jpg" alt="EgoSchema Video" width="80%" height="80%" border="10" /></a>
</p>
<p align="center" style="color: #87CEEB"> Click for the youtube teaser video </p>

## :dizzy: Dataset Highlights 

:exclamation: EgoSchema is 10x to 100x more difficult longer temporal reasoning than almost all other video datasets**.<br/><br/>
:exclamation: Largest OSS Video-Language models with 7B+ parameters achieve QA accuracy of <33% (Random choice is 20%). Humans achieve ~76%. <br/><br/>
:exclamation: Even web-scaled trained closed source models with 100B+ parameters achieve <40% accuracy, highlighting the massive latent gap in model capabilities for long-term video understanding.  <br/><br/>

<i> **please see [paper](https://arxiv.org/abs/2308.09126) for precise operationalizations. </i>

## :star: Downloading the Dataset

### Option A (Download via Kaggle): 
The most optimal way to download the dataset at the current moment.

1. Visit Kaggle [Public API guide](https://www.kaggle.com/docs/api) and install and authenticate Kaggle CLI
2. Visit the [Egoschema competition page](https://www.kaggle.com/competitions/egoschema-public/overview), read and accept the rules in order to download data or make submissions.
3. After that you can download the videos folder by running the following command:
`kaggle competitions download -c egoschema-public`


### Option B (Download via Wasabi): 
Fast. Supports Resuming over spotty internet.
  
1. Download `uid_to_url.json` file from [EgoSchema Google Drive](https://drive.google.com/drive/folders/1SS0VVz8rML1e5gWq7D7VtP1oxE2UtmhQ?usp=sharing)

This file will be updated weekly as the links expire every 7 days. You will receive a warning if your file becomes outdated.

2. Run the following:

```bash
conda create -n egoschema_download python=3.8 
conda activate egoschema_download
conda install tqdm simplejson requests
pip install moviepy
mkdir videos
python download.py
```

**Note 1**: This will retrieve the dataset and store it in the `videos` directory. Video names correspond to the `q_uid` key in the `questions.json` file. If any files encounter issues during installation, rerun the `download.py` script. If problems persist, links to the necessary files will be provided via Google Drive.

**Note 2**: If above is too slow, run `python download_multiproc.py --p <number of processes>` instead for multi-processed downloading. Please be aware that this method might hit the rate limit under heavy load on wasabi servers. In that case please revert to `download.py`  

### Option C: Direct Download (Download zip from Google Drive):
Simpler. Requires stable internet connection. 

1. Directly download the zipped file from the [EgoSchema Google Drive](https://drive.google.com/drive/folders/1SS0VVz8rML1e5gWq7D7VtP1oxE2UtmhQ?usp=sharing).

## Benchmarking on EgoSchema 

### 1. Benchmarking New models: 
While we release all the video and questions from EgoSchema, we release the correct answers to only 500 of the EgoSchema questions provided in the `subset_answers.json` file intended for offline experimentation and performance tracking. 

:loudspeaker: EgoSchema is intended for a 0-shot evaluation benchmark, hence the **entire correct answer file will not be make public**. To evaluate on the entire benchmark please submit the correct answer estimate as follows: 
  
  **Option A:** 
Public Kaggle leaderboard. The primary means of submitting the results.
  
- **Step 1**:  Visit Kaggle [Public API guide](https://www.kaggle.com/docs/api) and install and authenticate Kaggle CLI.
- **Step 2**: Visit the [Egoschema competition page](https://www.kaggle.com/competitions/egoschema-public/overview), read and accept the rules in order to make submissions. Additionally read the submission procedure overview in the competition landing page.
- **Step 3**:  You can use Kaggle CLI to submit your results. **Use `egoschema-public` as competition name.**
```
usage: kaggle competitions submit [-h] -f FILE_NAME -m MESSAGE [-q]
                                  [competition]

required arguments:
  -f FILE_NAME, --file FILE_NAME
                        File for upload (full path)
  -m MESSAGE, --message MESSAGE
                        Message describing this submission

optional arguments:
  -h, --help            show this help message and exit
  competition           Competition URL suffix (use "kaggle competitions list" to show options)
                        If empty, the default competition will be used (use "kaggle config set competition")"
  -q, --quiet           Suppress printing information about the upload/download progress
```

 **Option B (using our provided wrapper):** 
No leaderboard, just a submission validation.

- **Step 1**: Prepare a JSON file that contains a dictionary structured as `{ <question uid> :<correct answer>` where `correct_answer : int[0 - 4]`.  
- **Step 2**:  Run `python validate.py --f <path_to_json_file>` to send the request to EgoSchema server,

**Option C (directly using CURL):** 
No leaderboard, just a submission validation.

- `curl -X POST -H "Content-Type: application/json" -d @<path_to_json_file> https://validation-server.onrender.com/api/upload/`

**Returned Payload** will contain the Multiple-Choice Question-Answer accuracy in the following text format: 
```
MCQ Accuracy for All of 5031 EgoSchema Questions
MCQ Accuracy for Publicly eleased 500 EgoSchema Answers 
```

:fireworks: *Coming Soon* : A public leaderboard of submitted model rankings on EgoSchema.  
### 2. Reproducing model results from paper : 
Please see `benchmarking/` for detailed description of each model separately.