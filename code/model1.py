# Packages for model training
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import StandardScaler
from imblearn.under_sampling import RandomUnderSampler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
from sklearn.metrics import classification_report
# import joblib
# import yaml

path_X_train = "../data/X_train.csv"
path_y_train = "../data/y_train.csv"
random_state = 20230703

# scaler function
def scaler_transform(data, scaler):
    data_scaled = scaler.transform(data)
    data_scaled = pd.DataFrame(data_scaled)
    data_scaled.columns = data.columns
    data_scaled.index = data.index

    return data_scaled

# Model training
def train_model(path_X_train, path_y_train):
    X_train = pd.read_csv(path_X_train, index_col=0)
    y_train = pd.read_csv(path_y_train, index_col=0).squeeze()
    X_train["LogMonthlyIncome"] = np.log(X_train["MonthlyIncome"]+1)
    X_train["LogLogRevolvingUtilizationOfUnsecuredLines"] = np.log(np.log(X_train["RevolvingUtilizationOfUnsecuredLines"]+1)+1)
    X_train["LogDebtRatio"] = np.log(X_train["DebtRatio"]+1e-05)

    # Standardizing data & undersampling
    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train_scaled = scaler_transform(data = X_train,
                                      scaler = scaler)
    rus = RandomUnderSampler(sampling_strategy = 0.3,
                            random_state = 20230703)
    X_res, y_res = rus.fit_resample(X_train_scaled, y_train)

    # Assigning weight to Approved & Rejected credit
    n_samples = len(y_res)
    n_classes = len(y_res.value_counts())
    n_samples_j = y_res.value_counts()

    class_weight = n_samples / (n_classes * n_samples_j)
    class_weight

    # hyperparameter search
    logreg = LogisticRegression(class_weight = dict(class_weight),
                                solver = "liblinear",
                                random_state = 20230703)
    search_params = {"penalty": ["l1", "l2"],
                    "C": np.logspace(-5, 5, 20)}
    logreg_cv = GridSearchCV(estimator = logreg,
                            param_grid = search_params,
                            cv = 5)
    logreg_cv.fit(X = X_res,
                y = y_res)
    
    # fitting best model
    logreg_best = LogisticRegression(penalty = logreg_cv.best_params_["penalty"],
                                    C = logreg_cv.best_params_["C"],
                                    class_weight = dict(class_weight),
                                    solver = "liblinear",
                                    random_state = random_state)
    logreg_best.fit(X_res, y_res)

    return logreg_best
    





# PATH_CONFIG = "../config/config.yaml"
# config = yaml.safe_load(open(PATH_CONFIG))


