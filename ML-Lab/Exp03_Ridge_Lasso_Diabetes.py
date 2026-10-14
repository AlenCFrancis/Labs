# ============================================================
# Experiment No: 3
# RIDGE AND LASSO REGRESSION ON DIABETES DATASET
# ------------------------------------------------------------
# Aim     : Compare Ridge (L2) and Lasso (L1) regularised regression
#           with plain Linear Regression.
# Dataset : sklearn.datasets.load_diabetes()  (loaded from package)
#           442 patients, 10 features: age, sex, bmi, bp, s1 ... s6
#           Target : disease progression one year after baseline
#           (This is NOT the Pima diabetes CSV - that is used in Exp 6.)
# ============================================================

import numpy as np                                       # numerical arrays
import pandas as pd                                      # DataFrames
import matplotlib.pyplot as plt                          # plotting
from sklearn.datasets import load_diabetes               # dataset from package
from sklearn.model_selection import train_test_split     # train / test split
from sklearn.preprocessing import StandardScaler         # mean 0, std 1 scaling
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV  # the 3 models
from sklearn.metrics import mean_squared_error, r2_score # evaluation metrics

# ---- Step 2: Load dataset ----
data = load_diabetes()
X, y = data.data, data.target
print(pd.DataFrame(X, columns=data.feature_names).head())

# ---- Step 3: Standardise ----
# Penalties act on coefficient size, so all features must be on the same scale
scaler = StandardScaler()
X = scaler.fit_transform(X)

# ---- Step 4: Split (80% / 20%) ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# 100 candidate penalty strengths from 0.0001 to 100
alphas = np.logspace(-4, 2, 100)

models = {
    # no penalty
    'Linear Regression': LinearRegression(),
    # Ridge: loss + alpha*sum(w^2); best alpha chosen by 5-fold cross-validation
    'Ridge (L2)'       : RidgeCV(alphas=alphas, cv=5),
    # Lasso: loss + alpha*sum(|w|); can push some weights exactly to 0
    'Lasso (L1)'       : LassoCV(alphas=alphas, cv=5, max_iter=10000),
}

# ---- Step 5 – 9: Train, predict and evaluate each model ----
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f'{name:22s} MSE={mse:.2f}  R2={r2:.4f}')

# Best alpha selected by cross-validation
print(f"\nRidge best alpha : {models['Ridge (L2)'].alpha_:.4f}")
print(f"Lasso best alpha : {models['Lasso (L1)'].alpha_:.4f}")

# ---- Step 10 & 11: Visualise coefficients ----
# Ridge shrinks all coefficients; Lasso sets some to zero (feature selection)
feat_names = data.feature_names
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
for ax, (name, model) in zip(axes, models.items()):
    ax.bar(feat_names, model.coef_)
    ax.set_title(name)
    ax.tick_params(axis='x', rotation=45)
plt.tight_layout()
plt.show()
