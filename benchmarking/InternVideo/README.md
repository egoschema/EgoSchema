

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
- Install CLIP Vit-L-14 weights file `ViT-L-14.pt` at [following link](https://openaipublic.azureedge.net/clip/models/b8cca3fd41ae0c99ba7e8951adf17d267cdb84cd88be6f7c2e0eca1737a03836/ViT-L-14.pt)
- Install InternVideo's MSRVTT weight file `MSRVTT.ckpt` by submitting InternVideo form avaliable on their github page. Here is their [link](https://wenjuan.feishu.cn/m/res?t=syQjww7QWNJi-jk5u)

### Step 2: Positioning Code Files

Place the `run_internvideo.py` and `disguise.ipynb` files as well as place the weights files `MSRVTT.ckpt` and `ViT-L-14.pt` in the `Downstream/multi-modalities-downstream`.

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

### Step 5: Modify `msrvtt_choice.py` File

Navigate to `Cotrain/datasets/video/msrvtt_choice.py` and find the section around line 72. Replace the existing code block:

```python
ret = {
            "video": video_tensor,
            "vid_index": index,
            "cap_index": index,
            "raw_index": index,
            'answer': answer
        }
```

With the modified version:

```python
ret = {
            "video": video_tensor,
            "vid_index": index,
            "cap_index": index,
            "raw_index": index,
            'answer': answer,
            'q_uid': sample['clip_name'],
        }
```


This modification allows us to keep track of the q_uid of question when recording the results

### Step 6: Modify `text_prompt.py` File

Navigate to `Cotrain/datasets/modules/text_prompt.py` and find the section around line 10. Replace the existing code block:

```python
def text_prompt(data = K400VideoDataset.classes(), prompt_type='all'):
```

With the modified version:

```python
def text_prompt(data, prompt_type='all'):
```

This modification just fixes some issues the codebase.

### Step 7: Modify `cotrain_utils.py` File

Navigate to `Cotrain/datasets/modules/cotrain_utils.py` and find the section around line 46. Comment out the existing code block:

```python
setattr(pl_module, f"{split}_{k}_accuracy", Accuracy())
```

This modification just fixes some issues the codebase. There might be other small bugs.

### Step 8: Run Benchmark Script

- Update `ViT` with the path pointing to the previously downloaded ViT weights file
- Update `MSRVTT` with the path pointing to the previously downloaded `MSRVTT` weights file

Execute the `run_internvideo.py` script:

```bash
python run_internvideo.py --f 15
```

Parameters:
- `--f`: Determines the number of frames to be used during processing. 

---

