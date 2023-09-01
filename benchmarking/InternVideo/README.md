
# Benchmarking `InternVideo` with EgoSchema Dataset

This README provides a comprehensive guide to benchmarking the `InternVideo` system using the EgoSchema dataset. Follow each step methodically to ensure seamless setup and execution.

## Prerequisites

### 1. EgoSchema Dataset

Ensure you have the EgoSchema dataset downloaded and readily available.

### 2. Configuration Adjustments

Navigate to the `disguise.ipynb` file:
- Update `EGOSCHEMA_FOLDER` with the path pointing to the EgoSchema folder.

## Installation and Configuration

### Step 1: Clone `InternVideo` Repository

Clone the `InternVideo` repository from the official GitHub repository:

```bash
git clone https://github.com/OpenGVLab/InternVideo.git
```

Subsequently:
- Closely follow the onboarding steps detailed on their official documentation.
- Install CLIP Vit-L-14 weights file `ViT-L-14.pt` at https://openaipublic.azureedge.net/clip/models/b8cca3fd41ae0c99ba7e8951adf17d267cdb84cd88be6f7c2e0eca1737a03836/ViT-L-14.pt
- Install InternVideo's MSRVTT weight file `MSRVTT.ckpt` by submitting InternVideo form avaliable on their github page.

### Step 2: Positioning Code Files

Place the `run_internvideo.py` and `disguise.ipynb` files as well as `meta_data` folder into `Downstream/multi-modalities-downstream`. Additionally place the weights files `MSRVTT.ckpt` and `ViT-L-14.pt` in the `Downstream/multi-modalities-downstream`.

### Step 3: Question Formatting

Execute the `disguise.ipynb` Jupyter notebook. This script will transform the questions into a format compatible with `msrvtt` and fill the meta_data folder appropriatelly.

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

