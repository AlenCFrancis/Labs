# ============================================================
# Experiment : Logistic Regression (with and without feature scaling)
# Dataset    : Pima Indians Diabetes (Datasets/diabetes_dataset.csv)
# Columns    : Pregnancies, Glucose, BloodPressure, SkinThickness,
#              Insulin, BMI, DiabetesPedigreeFunction, Age
# Target     : Outcome (1 = diabetic, 0 = not diabetic)
# Goal       : Classify patients and compare performance when the
#              features are scaled vs. not scaled.
# ============================================================

import os                                             # to build the dataset file path
import numpy as np                                    # numerical arrays / NaN
import pandas as pd                                   # reading the CSV
import matplotlib.pyplot as plt                       # plotting

from sklearn.model_selection import train_test_split  # split data into train / test
from sklearn.preprocessing import StandardScaler      # scaling: mean 0, std 1
from sklearn.linear_model import LogisticRegression   # the classification model
from sklearn.metrics import (
    accuracy_score,    # overall % correct
    precision_score,   # of predicted diabetics, how many really are
    recall_score,      # of real diabetics, how many we caught
    f1_score,          # balance of precision and recall
    roc_curve,         # points for the ROC curve
    roc_auc_score      # area under ROC curve (1 = perfect, 0.5 = random)
)

# Folder that contains the CSV files (Ml lab/Datasets).
# On Colab change this to '/content'.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Datasets')

# Load the dataset (768 rows x 9 columns)
df = pd.read_csv(os.path.join(DATA_DIR, 'diabetes_dataset.csv'))

# In these columns a value of 0 is impossible (e.g. BMI = 0), so 0 means "missing".
cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

for col in cols:
    df[col] = df[col].replace(0, np.nan)            # mark 0 as missing
    df[col] = df[col].fillna(df[col].median())      # fill missing with the column median

# X = 8 input features, y = target (Outcome)
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# 80% train / 20% test; stratify keeps the same diabetic/non-diabetic ratio in both
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ---------- Model 1: WITHOUT feature scaling ----------
model_no_scale = LogisticRegression(max_iter=1000)   # more iterations so it converges
model_no_scale.fit(X_train, y_train)

y_pred_no = model_no_scale.predict(X_test)               # predicted class (0/1)
y_prob_no = model_no_scale.predict_proba(X_test)[:, 1]   # probability of class 1 (for ROC)

# ---------- Model 2: WITH feature scaling ----------
scaler = StandardScaler()

# fit only on training data (learn mean/std), then apply the same to test data
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model_scaled = LogisticRegression(max_iter=1000)
model_scaled.fit(X_train_scaled, y_train)

y_pred_scaled = model_scaled.predict(X_test_scaled)
y_prob_scaled = model_scaled.predict_proba(X_test_scaled)[:, 1]

# ---------- Compare the metrics ----------
print("Model Performance\n")

print("Without Feature Scaling")
print(f"Accuracy  : {accuracy_score(y_test, y_pred_no):.4f}")
print(f"Precision : {precision_score(y_test, y_pred_no):.4f}")
print(f"Recall    : {recall_score(y_test, y_pred_no):.4f}")
print(f"F1-score  : {f1_score(y_test, y_pred_no):.4f}")

print("\nWith Feature Scaling")
print(f"Accuracy  : {accuracy_score(y_test, y_pred_scaled):.4f}")
print(f"Precision : {precision_score(y_test, y_pred_scaled):.4f}")
print(f"Recall    : {recall_score(y_test, y_pred_scaled):.4f}")
print(f"F1-score  : {f1_score(y_test, y_pred_scaled):.4f}")

# ---------- ROC curves ----------
# ROC = True Positive Rate vs False Positive Rate at every probability threshold
fpr1, tpr1, _ = roc_curve(y_test, y_prob_no)
auc1 = roc_auc_score(y_test, y_prob_no)

fpr2, tpr2, _ = roc_curve(y_test, y_prob_scaled)
auc2 = roc_auc_score(y_test, y_prob_scaled)

plt.figure(figsize=(8,6))

plt.plot(fpr1, tpr1,
         label=f'Without Scaling (AUC = {auc1:.3f})',
         linewidth=2)

plt.plot(fpr2, tpr2,
         label=f'With Scaling (AUC = {auc2:.3f})',
         linewidth=2)

plt.plot([0,1], [0,1], 'k--')   # diagonal = random guessing

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()