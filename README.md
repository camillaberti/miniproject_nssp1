# NSSP Mini Project 1

## Folder setup

To run the subsequent analysis, the project reporitory must be organized as follow:

```text
E_code/
├── 01_struct_preprocessing.ipynb
├── 02_func_preprocessing.ipynb
├── 03_glm.ipynb
├── 04_ica.ipynb
├── utils.py
└── dataset/
    ├── dataset_description.md
    ├── T1/
    │   └── T1w.nii.gz
    └── fMRI/
        └── tfMRI_LANGUAGE_LR/
            ├── tfMRI_LANGUAGE_LR.nii.gz
            └── tfMRI_LANGUAGE_LR_task_onsets.csv
```

## Execution order

Open Jupyter in Neurodesk with `E_code/` as the working directory and run all cells in each notebook from top to bottom before starting the next one.

1. `01_struct_preprocessing.ipynb` — anatomical preprocessing
2. `02_func_preprocessing.ipynb` — functional preprocessing
3. `03_glm.ipynb` — general linear model (GLM) analysis
4. `04_ica.ipynb` — independent component analysis (ICA)
