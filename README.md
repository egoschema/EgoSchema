
# EgoSchema Dataset

## Introduction

[Webpage](https://https://egoschema.github.io/) • [Paper](https://https://egoschema.github.io/) 

![Teaser](paper/teaser_final.pdf)
<object data="http://yoursite.com/the.pdf" type="application/pdf" width="700px" height="700px">
    <embed src="http://yoursite.com/the.pdf">
        <p>This browser does not support PDFs. Please download the PDF to view it: <a href="http://yoursite.com/the.pdf">Download PDF</a>.</p>
    </embed>
</object>
EgoSchema is a pioneering dataset aimed to evaluate the long video understanding capabilities of the contemporary vision and language systems. Derived from Ego4D, EgoSchema encompasses over 5000 human-curated multiple-choice question-answer pairs, spread across more than 250 hours of genuine video data. This dataset captures a vast spectrum of natural human activity and behavior.

For each question,  EgoSchema  requires the correct answer to be selected between  five given options based on a three-minute-long video clips. While some prior works have proposed video datasets with long clip lengths, we posit that merely the length of the video clip does not truly capture the temporal difficulty of the video task that is being considered. To remedy this, we introduce temporal certificate sets, a general notion for capturing the intrinsic temporal understanding length associated with a broad range of video understanding tasks & datasets. EgoSchema, alongside its profound temporal structures and varying complexity, is projected to be a pivotal evaluation tool for the subsequent advancements in the realm of video understanding.

## Highlights

- Over 5000 curated multiple choice question-answer pairs.
- More than 250 hours of real video data.
- EgoSchema possesses intrinsic temporal lengths surpassing 5.7 times that of the second closest dataset and between 10 to 100 times longer than other datasets.
- The latest high-end video and language models with billions of parameters have struggled to perform well on this dataset. A mere QA accuracy less than 33% (compared to a random choice's 20%) was noted, whereas human performance rests at approximately 76% accuracy.
- Designed to act as a cornerstone for the future development of highly effective long-term video understanding systems.

## Downloading the Dataset

To download the dataset, simply run the following command:

```bash
conda create -n egoschema_download python=3.8 
conda activate egoschema_download
conda install tqdm simplejson requests
mkdir videos
python download.py
```

This will fetch the dataset and save it in the `videos` folder. The naming convention for the videos corresponds to the `q_uid` key in the `questions.json` file.