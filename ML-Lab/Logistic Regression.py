import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_curve,
    roc_auc_score
)

df = pd.read_csv('/content/diabetes.csv')

cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']

for col in cols:
    df[col] = df[col].replace(0, np.nan)
    df[col].fillna(df[col].median(), inplace=True)

X = df.drop('Outcome', axis=1)
y = df['Outcome']

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model_no_scale = LogisticRegression(max_iter=1000)
model_no_scale.fit(X_train, y_train)

y_pred_no = model_no_scale.predict(X_test)
y_prob_no = model_no_scale.predict_proba(X_test)[:, 1]

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model_scaled = LogisticRegression(max_iter=1000)
model_scaled.fit(X_train_scaled, y_train)

y_pred_scaled = model_scaled.predict(X_test_scaled)
y_prob_scaled = model_scaled.predict_proba(X_test_scaled)[:, 1]

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

plt.plot([0,1], [0,1], 'k--')

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve Comparison")

plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()