
# Benchmarking `InternVideo` with EgoSchema Dataset

This README provides a comprehensive guide to benchmarking the `InternVideo` system using the EgoSchema dataset. Follow each step methodically to ensure seamless setup and execution. Note: all of the benchmarking code requires correct answer to the questions that we will release soon.

## Prerequisites

### 1. EgoSchema Dataset

Ensure you have the EgoSchema dataset downloaded and readily available.

### 2. Configuration Adjustments

Navigate to the `disguise.ipynb` file:
- Update `EGOSCHEMA_FOLDER` with the path pointing to the EgoSchema dataset.

## Installation and Configuration

### Step 1: Clone `InternVideo` Repository

Clone the `InternVideo` repository from the official GitHub repository:

```bash
git clone https://github.com/OpenGVLab/InternVideo.git
```

Subsequently:
- Closely follow the onboarding steps detailed on their official documentation.
- Ensure you install both `InternVideo's MSRVTT` and `Vit-L-14 finetuned weights`.

### Step 2: Positioning Code Files

Place the provided code files and directories into `Downstream/multi-modalities-downstream`.

### Step 3: Question Formatting

Execute the `disguise.ipynb` Jupyter notebook. This script will transform the questions into a format compatible with `msrvtt`.

### Step 4: Modify `objectives.py` File

Navigate to `Cotrain/modules/objectives.py` and find the section around line 571. Replace the existing code block:

```python
phase = "train" if pl_module.training else "val"
acc = getattr(pl_module, f"{phase}_multiple_choice_accuracy")(
    score, vtm_labels
)
# print(acc)
ret = {
    "multiple_choice_loss": loss,
}

phase = "train" if pl_module.training else "val"
loss = getattr(pl_module, f"{phase}_multiple_choice_loss")(ret["multiple_choice_loss"])

pl_module.log(f"multiple_choice/{phase}/loss", loss)
pl_module.log(f"multiple_choice/{phase}/accuracy", acc)
return ret
```

With the modified version:

```python
ret = {
       "score": score,
       "ground_truth": vtm_labels
   }
return ret
```

This modification allows the extraction of choice scores from the model.

### Step 5: Run Benchmark Script

Execute the `run_internvideo.py` script:

```bash
python run_internvideo.py --f 15
```

Parameters:
- `--f`: Determines the number of frames to be used during processing. 

---

