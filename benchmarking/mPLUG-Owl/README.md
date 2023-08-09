# Benchmarking mPlug-Owl

## Files you will need
- questions.csv - a csv file that will be provided on our project Github page. Here we provided a sample questions.csv with redacted unnessasry columns
- folder with clips. file name of the clips should be the same as the relevant column name in questions.csv

### Step 1:  Clone mPlug-Owl at https://github.com/X-PLUG/mPLUG-Owl
Please follow all the step for their onboarding listed on their website.
### Step 2: Put the code files and folders inroot folder of mPLUG-Owl
### Step 3: You will need to prepare the frames with framing.ipynb
- You will need questions.csv file where first column is the video name and second is the questins and answer options. A sample file is provided.
- Please specify the vid_location to be the folder in with clips and frames
- put the clip video files in clips folder in vid_location
- create the folder in vid_location called frames_{amount of frames you want to run}

### Step 3: Run run_mplug.py file
- Put the frame folder in FRAME_FOLDER variable
```
python run_mplug.py --f 15
```
- --f how much frames to use 