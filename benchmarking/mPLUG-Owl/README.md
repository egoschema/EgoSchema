
# Benchmarking `mPLUG-Owl` with the EgoSchema Dataset

This guide offers a step-by-step walkthrough to benchmark the `mPLUG-Owl` system with the EgoSchema dataset. For a successful setup and execution, it's essential to follow each step diligently.

## Prerequisites

**EgoSchema Dataset**:
Ensure the EgoSchema dataset is downloaded and easily accessible before proceeding.

## Installation and Configuration

### Step 1: Clone the `mPLUG-Owl` Repository

1. Clone the specific branch of the `mPLUG-Owl` repository:

```bash
git clone -b v0 https://github.com/OpenGVLab/InternVideo.git
```

2. Adhere to the onboarding instructions detailed in their official documentation.
3. Download both `mPLUG-Owl` and the tokenizer weights.
4. Update `run_mplug.py` with the following paths:
    - `CHECKPOINT_PATH`: Path to the `mPLUG-Owl` weights.
    - `TOKENIZER_PATH`: Path to the tokenizer weights.
    - `EGOSCHEMA_FOLDER`: Path to the EgoSchema dataset.

### Step 2: Integrate Code Files

Transfer the provided code files into the cloned `mPLUG-Owl` directory.

### Step 3: Frame Preparation using `framing.ipynb`

1. Open `framing.ipynb` or `framing.py`:
    - Set `EGOSCHEMA_FOLDER` to the path of the EgoSchema dataset.
    - Define the number of frames you wish to extract by adjusting the `frames` variable.
    
2. Running `framing.ipynb` or `framing.py`will create a directory named `frame_{number of frames}`. Inside, you'll find subdirectories corresponding to each video. Each subdirectory houses a certain number of frames extracted from its associated video.

### Step 4: Execute the Benchmark Script

Run the `run_mplug.py` script with the desired frame parameter:

```bash
python run_mplug.py --f 10
```

Parameters:
- `--f`: Specifies the number of frames to utilize. 

---

