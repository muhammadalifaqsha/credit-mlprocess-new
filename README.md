# Data Preparation

<img src="https://i.ibb.co/rw0z7bT/Blank-diagram-1.png" width="400">

# Data Preprocessing

<img src="https://i.ibb.co/T1g8sfW/Data-Preprocessing.png" width="800">

# Features Engineering

<img src="https://i.ibb.co/mcmRk0z/Features-Engineering-1.png" width="800">

# Modelling & Evaluation

<img src="https://i.ibb.co/CQ4YSXS/Modelling-Evaluation-1.png" width="800">

# How to Retrain Model

1. If you just want to retrain model, just run the notebook "02 modelling-training.ipynb".
2. If you also want to change the train-test split (or use another data), run the "01 preprocessing-eda.ipynb" first (with appropriate modification to random state or data input), then run "02 modelling-training.ipynb".

# Note on Local Deployment

If you want to clone & deploy this repository in your local environment, you might want to modify the "credit-api.py" file (in the api folder) with this: [modified credit-api.py](https://github.com/muhammadalifaqsha/credit-mlprocess/blob/main/api/credit-api.py)
