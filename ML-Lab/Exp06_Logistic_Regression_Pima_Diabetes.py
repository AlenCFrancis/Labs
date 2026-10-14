# ============================================================
# Experiment No: 6
# LOGISTIC REGRESSION ON PIMA INDIANS DIABETES DATASET
# ------------------------------------------------------------
# Aim     : Predict diabetes with logistic regression and compare
#           performance with and without feature scaling.
# Dataset : Datasets/diabetes_dataset.csv  (loaded with read_csv)
#           Columns: Pregnancies, Glucose, BloodPressure, SkinThickness,
#                    Insulin, BMI, DiabetesPedigreeFunction, Age
#           Target : Outcome (1 = diabetic, 0 = not diabetic)
# ============================================================

import os                                                # build file paths
import numpy as np                                       # numerical arrays / NaN
import pandas as pd                                      # read_csv
import matplotlib.pyplot as plt                          # plotting
from sklearn.model_selection import train_test_split     # train / test split
from sklearn.preprocessing import StandardScaler         # scaling
from sklearn.linear_model import LogisticRegression      # the model
from sklearn.metrics import (accuracy_score, classification_report,
                             roc_curve, roc_auc_score)

# Path to the Datasets folder (Ml lab/Datasets). On Colab use '/content'.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Datasets')

# ---- Step 2: Load ----
df = pd.read_csv(os.path.join(DATA_DIR, 'diabetes_dataset.csv'))
print(df.head())

# ---- Step 3: Handle missing values ----
# A value of 0 is impossible for these medical measurements, so 0 = missing.
med_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
print('\nZeros per column:\n', (df[med_cols] == 0).sum())
df[med_cols] = df[med_cols].replace(0, np.nan)   # mark as missing
df = df.fillna(df.median())                      # replace with column median

# ---- Step 4: Features and target ----
X = df.drop('Outcome', axis=1).values
y = df['Outcome'].values

# ---- Step 5: Split (80% / 20%) ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Fit the scaler on training data only (avoid leaking test info)
scaler = StandardScaler().fit(X_train)

# ---- Step 6 – 10: Train both versions, evaluate, plot ROC ----
for scaled, label in [(False, 'Without Scaling'), (True, 'With Scaling')]:
    Xtr = scaler.transform(X_train) if scaled else X_train
    Xte = scaler.transform(X_test) if scaled else X_test

    clf = LogisticRegression(max_iter=1000, random_state=42)
    clf.fit(Xtr, y_train)

    y_pred = clf.predict(Xte)               # class 0/1
    y_prob = clf.predict_proba(Xte)[:, 1]   # probability of diabetes (for ROC)

    print(f'\n--- {label} ---')
    print(f'Accuracy : {accuracy_score(y_test, y_pred):.4f}')
    print(classification_report(y_test, y_pred))   # precision, recall, F1

    # ROC: TPR vs FPR at all thresholds; AUC = area under it (1 = perfect)
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)
    plt.plot(fpr, tpr, label=f'{label} (AUC={auc:.3f})')

plt.plot([0, 1], [0, 1], 'k--')   # random-guess line
plt.xlabel('FPR'); plt.ylabel('TPR')
plt.title('ROC Curve – Pima Diabetes')
plt.legend(); plt.tight_layout(); plt.show()
