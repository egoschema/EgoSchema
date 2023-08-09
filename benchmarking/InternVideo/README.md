# Benchmarking InternVideo

## Files you will need
- questions.csv - a csv file that will be provided on our project Github page. Here we provided a sample questions.csv with redacted unnessasry columns
- folder with clips. file name of the clips should be the same as the relevant column name in questions.csv

### Step 1:  Clone FrozenBilm at https://github.com/OpenGVLab/InternVideo
Please follow all the step for their onboarding listed on their website.
### Step 2: Put the code files and folders in Downstream/multi-modalities-downstream
### Step 3: Use disguise.ipynb in order to put question in the same format as msrvtt.
You will need question.csv file that consist of question and corresposnding video file names. Please put location of clips in CLIP_LOCATION. An example of question.csv is provided.
### Step 3: Run run_internvideo.py file
```
python run_internvideo.py --f 15
```
- --f how much frames to use 