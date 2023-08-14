# Reproducing VIOLETv2 Results on EgoSchema

This readme provides a step by step procedure for evaluating VIOLETv2 on EgoSchema

**Step 1:** Clone VIOLETv2 repo & setup environment
```shell
git clone https://github.com/tsujuifu/pytorch_empirical-mvm
cd pytorch_empirical-mvm
mkdir egoSchema
```
Next:
1. Download the clips and save them to a directory `<clips_dir>`
2. Download the EgoSchema csv and save it to the folder your created above: `pytorch_empirical-mvm/egoSchema`
3. Download provided pre-processing scripts and put them in `pytorch_empirical-mvm/egoSchema`
4. Download the `args_egoSchema.json` and place it in `pytorch_empirical-mvm/_args`
4. Install the necessary packages as listed on pytorch_empirical-mvm README.md

**Step 2:** Preprocess EgoSchema data 
```shell
python preprocess_vids.py --videos_dir <clips_dir> --n_frames <However many frames you want to extract (should be more than 75)>
python preprocess_text.py
```
**Step 3:** Run VIOLETv2 on EgoSchema
The following uses 4 GPUs for inference. Modify the script to accomodate the number you have access to.
```shell
CUDA_VISIBLE_DEVICES='0,1,2,3' python -m torch.distributed.launch --nproc_per_node=4 --master_port=5566 main_qamc_tsv.py --config _args/args_egoSchema.json
```