# ============================================================
# Experiment No: 4
# LOGISTIC REGRESSION – MLE AND MAP ON BREAST CANCER DATASET
# ------------------------------------------------------------
# Aim     : Estimate logistic regression parameters using
#           MLE (no regularisation) and MAP (L2 / L1 regularisation).
# Dataset : Datasets/breast-cancer-wisconsin-data_data.csv (read_csv)
#           Columns: id, diagnosis (M/B), 30 numeric features such as
#                    radius_mean, texture_mean, ..., fractal_dimension_worst
#           Target : diagnosis -> 0 = malignant (M), 1 = benign (B)
#           (same encoding as sklearn's load_breast_cancer)
# ============================================================

import os                                                # build file paths
import numpy as np                                       # numerical arrays
import pandas as pd                                      # read_csv
import matplotlib.pyplot as plt                          # plotting
from sklearn.model_selection import train_test_split     # train / test split
from sklearn.preprocessing import StandardScaler         # scaling
from sklearn.linear_model import LogisticRegression      # the model
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, ConfusionMatrixDisplay)

# Path to the Datasets folder (Ml lab/Datasets). On Colab use '/content'.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Datasets')

# ---- Step 2: Load ----
df = pd.read_csv(os.path.join(DATA_DIR, 'breast-cancer-wisconsin-data_data.csv'))

# The header ends with a trailing comma -> pandas creates an empty 'Unnamed: 32' column.
# Drop it, and drop 'id' (just a patient number, not a useful feature).
df = df.drop(columns=['id'] + [c for c in df.columns if c.startswith('Unnamed')])

# Encode the target: M (malignant) -> 0, B (benign) -> 1
df['diagnosis'] = df['diagnosis'].map({'M': 0, 'B': 1})
target_names = ['malignant', 'benign']

X = df.drop('diagnosis', axis=1).values   # 30 features
y = df['diagnosis'].values                # target
print(df.head())

# ---- Step 3 & 4: Scale and split ----
X = StandardScaler().fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# (label, penalty, solver, C)
# MLE  : penalty=None -> maximise likelihood only
# MAP-L2 : Gaussian prior on weights  -> L2 penalty
# MAP-L1 : Laplace prior on weights   -> L1 penalty (needs 'saga' or 'liblinear' solver)
# C = 1/lambda -> smaller C = stronger prior / regularisation
configs = [
    ('MLE (no reg)', None,  'lbfgs', 1.0),
    ('MAP – L2',     'l2',  'lbfgs', 1.0),
    ('MAP – L1',     'l1',  'saga',  1.0),
]

# ---- Step 5 – 11: Train, evaluate and plot confusion matrices ----
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, (label, penalty, solver, C) in zip(axes, configs):
    clf = LogisticRegression(penalty=penalty, solver=solver,
                             C=C, max_iter=5000, random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f'\n{label}')
    print(f'  Accuracy: {acc:.4f}')
    # Step 10: compare parameter estimates (size of weights / how many are zero)
    print(f'  Sum |coef| = {np.abs(clf.coef_).sum():.2f}   '
          f'Zero coefs = {np.sum(clf.coef_ == 0)}')
    print(classification_report(y_test, y_pred, target_names=target_names))

    # Confusion matrix: rows = actual class, columns = predicted class
    cm = confusion_matrix(y_test, y_pred)
    ConfusionMatrixDisplay(cm, display_labels=target_names).plot(ax=ax, colorbar=False)
    ax.set_title(label)
plt.tight_layout()
plt.show()
