
# Benchmarking `FrozenBiLM` with EgoSchema Dataset

This guide provides the code for benchmarking the `FrozenBiLM` model using the EgoSchema dataset. Follow the instructions carefully to ensure smooth execution.

## Prerequisites

1. **Download the EgoSchema Dataset**: Before proceeding, make sure you have the EgoSchema dataset downloaded and ready.

2. **Configuration Updates**: Open `run_frozenbilm.py`:
    - Set `EGOSCHEMA_FOLDER` to the path where the EgoSchema dataset resides.
    - Update `WEIGHTS_PATH` with the path leading to the `FrozenBiLM how2qa finetuned weights`.

## Setup and Execution Steps

### Step 1: Clone the `FrozenBiLM` Repository

Begin by cloning the `FrozenBiLM` repository from the official GitHub page:

```bash
git clone https://github.com/antoyang/FrozenBiLM.git
```

Ensure that you follow all onboarding steps and setup instructions provided on their official documentation.

### Step 2: Integrate Code Files

Place the provided code files into the root directory of the cloned `FrozenBiLM` repository.

### Step 3: Generate Video Clip Features

- Launch the `feature_gen.ipynb` or run `python feature_gen.py --f <frames number>`. This script facilitates the generation of features for video clips in the EgoSchema dataset. Some videos might not get proccessed properly so you might need to run it several times.
  
- You have the flexibility to adjust the `frame` parameter as per requirements.
  
- Upon execution, a new directory named `features` will be created. This will contain processed features for each video, maintaining a consistent naming convention.

### Step 4: Run the Benchmark Script

Execute the `run_frozenbilm.py` script using the following command:

```bash
python run_frozenbilm.py --f 90
```

Parameters:
- `--f`: Specifies the number of frames utilized during feature generation. The default value is `10`.

On successful execution, a JSON file will be generated, encapsulating the model's predictions for each question in the dataset.

**Note**: The correct answer corresponds to the output labeled `4`.
