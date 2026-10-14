# ============================================================
# Experiment : Linear vs Ridge (L2) vs Lasso (L1) Regression
# Dataset    : Pima Indians Diabetes (Datasets/diabetes_dataset.csv)
# Columns    : Pregnancies, Glucose, BloodPressure, SkinThickness,
#              Insulin, BMI, DiabetesPedigreeFunction, Age
# Target     : Outcome (0 / 1, treated here as a number to regress)
# Goal       : See how regularisation shrinks the coefficients.
#              Ridge shrinks all of them; Lasso can make some exactly 0
#              (automatic feature selection).
# ============================================================

import os                                             # to build the dataset file path
import numpy as np                                    # numerical arrays
import pandas as pd                                   # reading the CSV
import matplotlib.pyplot as plt                       # plotting

from sklearn.model_selection import train_test_split  # split data into train / test
from sklearn.preprocessing import StandardScaler      # scaling: mean 0, std 1
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV  # the 3 models
from sklearn.metrics import mean_squared_error, r2_score             # evaluation metrics

# Folder that contains the CSV files (Ml lab/Datasets).
# On Colab change this to '/content'.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Datasets')

# Load the dataset (768 rows x 9 columns)
df = pd.read_csv(os.path.join(DATA_DIR, 'diabetes_dataset.csv'))

# X = 8 input features, y = Outcome
X = df.drop('Outcome', axis=1)
y = df['Outcome']

# Scale features so the penalty treats every coefficient fairly
# (otherwise big-valued features like Insulin would dominate)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 80% train / 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# 1) Plain linear regression - no penalty
linear = LinearRegression()
linear.fit(X_train, y_train)

# 50 candidate penalty strengths (alpha) from 0.001 to 1000
alphas = np.logspace(-3, 3, 50)

# 2) Ridge: adds alpha * sum(coef^2). RidgeCV picks the best alpha with 5-fold cross-validation
ridge = RidgeCV(alphas=alphas, cv=5)
ridge.fit(X_train, y_train)

# 3) Lasso: adds alpha * sum(|coef|). LassoCV picks the best alpha with 5-fold CV
lasso = LassoCV(alphas=alphas, cv=5, random_state=42, max_iter=10000)
lasso.fit(X_train, y_train)

# Predictions from each model on the test set
y_pred_linear = linear.predict(X_test)
y_pred_ridge = ridge.predict(X_test)
y_pred_lasso = lasso.predict(X_test)

# Compare errors (lower MSE / higher R2 = better)
print("Model Performance\n")

print(f"Linear Regression      MSE = {mean_squared_error(y_test, y_pred_linear):.4f}   R² = {r2_score(y_test, y_pred_linear):.4f}")
print(f"Ridge (L2)             MSE = {mean_squared_error(y_test, y_pred_ridge):.4f}   R² = {r2_score(y_test, y_pred_ridge):.4f}")
print(f"Lasso (L1)             MSE = {mean_squared_error(y_test, y_pred_lasso):.4f}   R² = {r2_score(y_test, y_pred_lasso):.4f}")

# Table of coefficients: one row per feature, one column per model
coef_df = pd.DataFrame({
    'Feature': X.columns,
    'Linear Regression': linear.coef_,
    'Ridge (L2)': ridge.coef_,
    'Lasso (L1)': lasso.coef_
})

# Grouped horizontal bar chart to compare coefficients
plt.figure(figsize=(10,7))

x = np.arange(len(coef_df))   # one position per feature
width = 0.25                  # bar thickness

# Shift each model's bars slightly so they sit side by side
plt.barh(x - width, coef_df['Linear Regression'], height=width, label='Linear Regression')
plt.barh(x, coef_df['Ridge (L2)'], height=width, label='Ridge (L2)')
plt.barh(x + width, coef_df['Lasso (L1)'], height=width, label='Lasso (L1)')

plt.yticks(x, coef_df['Feature'])
plt.xlabel("Coefficient Value")
plt.ylabel("Feature")
plt.title("Comparison of Feature Coefficients")
plt.legend()

plt.tight_layout()
plt.show()