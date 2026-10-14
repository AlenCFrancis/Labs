# ============================================================
# Experiment No: 10
# LOGISTIC REGRESSION VS DECISION TREE ON ADULT INCOME DATASET
# ------------------------------------------------------------
# Aim     : Predict whether income is >50K and compare Logistic
#           Regression with a Decision Tree.
# Dataset : Datasets/adult.csv  (loaded with read_csv)
#           Columns: age, workclass, fnlwgt, education, educational-num,
#                    marital-status, occupation, relationship, race, gender,
#                    capital-gain, capital-loss, hours-per-week, native-country
#           Target : income ('<=50K' -> 0, '>50K' -> 1)
#           Missing values are written as '?'.
# ============================================================

import os                                                # build file paths
import numpy as np                                       # numerical arrays
import pandas as pd                                      # read_csv
import matplotlib.pyplot as plt                          # plotting
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# Path to the Datasets folder (Ml lab/Datasets). On Colab use '/content'.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Datasets')

# ---- Step 2: Load ----
# na_values='?' -> treat '?' as missing; skipinitialspace removes spaces after commas
df = pd.read_csv(os.path.join(DATA_DIR, 'adult.csv'),
                 na_values='?', skipinitialspace=True)
print(df.head())
print('Missing values per column:\n', df.isna().sum())
df = df.dropna()                                  # drop rows with missing values

# ---- Step 3 & 4: Encode target and categorical features ----
# Target: 1 if income > 50K else 0  (rstrip('.') handles '>50K.' variants)
df['income'] = (df['income'].str.strip().str.rstrip('.') == '>50K').astype(int)

# Convert each text column (workclass, education, ...) to integer codes
cat_cols = df.select_dtypes('object').columns
for c in cat_cols:
    df[c] = LabelEncoder().fit_transform(df[c])

X = df.drop('income', axis=1).values
y = df['income'].values
feat_names = df.drop('income', axis=1).columns.tolist()

# ---- Step 5 & 6: Split and scale ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
scaler = StandardScaler().fit(X_train)   # learn mean/std from training data
Xs_train = scaler.transform(X_train)
Xs_test = scaler.transform(X_test)

# ---- Step 7: Logistic Regression (needs scaled features) ----
lr = LogisticRegression(max_iter=1000, random_state=42)
lr.fit(Xs_train, y_train)

# ---- Step 8: Decision Tree (Gini by default; scaling not needed for trees) ----
dt = DecisionTreeClassifier(max_depth=7, random_state=42)
dt.fit(X_train, y_train)

# ---- Step 9 & 10: Predict and evaluate both ----
for name, clf, Xte in [('Logistic Regression', lr, Xs_test),
                       ('Decision Tree', dt, X_test)]:
    y_pred = clf.predict(Xte)
    print(f'\n=== {name} ===')
    print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
    print(classification_report(y_test, y_pred,
                                target_names=['<=50K', '>50K']))

# ---- Step 11: Feature importances from the Decision Tree ----
plt.barh(feat_names, dt.feature_importances_)
plt.xlabel('Importance'); plt.title('DT Feature Importances')
plt.tight_layout(); plt.show()
