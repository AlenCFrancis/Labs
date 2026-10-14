# ============================================================
# Experiment No: 1
# LINEAR REGRESSION ON CALIFORNIA HOUSING DATASET
# ------------------------------------------------------------
# Aim     : Predict house price from ONE feature (AveRooms) using
#           simple linear regression  y = m*x + c
# Dataset : Datasets/california_housing.csv  (loaded with read_csv)
#           Columns: MedInc, HouseAge, AveRooms, AveBedrms, Population,
#                    AveOccup, Latitude, Longitude
#           Target : MedHouseVal (median house value in $100,000s)
#           NOTE: the CSV has no target column, so the target is taken
#           from sklearn's fetch_california_housing() (same row order).
# ============================================================

import os                                                # build file paths
import numpy as np                                       # numerical arrays
import pandas as pd                                      # read_csv / DataFrames
import matplotlib.pyplot as plt                          # plotting
from sklearn.datasets import fetch_california_housing    # package copy of the dataset
from sklearn.model_selection import train_test_split     # train / test split
from sklearn.linear_model import LinearRegression        # the model
from sklearn.metrics import mean_squared_error, r2_score # evaluation metrics

# Path to the Datasets folder (Ml lab/Datasets). On Colab use '/content'.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Datasets')

# ---- Step 2: Load dataset ----
# Features from the local CSV file
df = pd.read_csv(os.path.join(DATA_DIR, 'california_housing.csv'))

# Target column from the sklearn package (CSV does not contain it)
data = fetch_california_housing()
df['MedHouseVal'] = data.target
print(df.head())

# ---- Step 3: Select single feature ----
X = df[['AveRooms']].values      # input  -> 2-D array (n_samples, 1) as sklearn needs
y = df['MedHouseVal'].values     # output -> 1-D array

# ---- Step 4: Train-test split (80% / 20%) ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)   # random_state -> same split every run

# ---- Step 5 & 6: Train Linear Regression model ----
# sklearn solves the least-squares problem (same result as Normal Equation
# theta = (X^T X)^-1 X^T y) to find slope and intercept.
model = LinearRegression()
model.fit(X_train, y_train)

# ---- Step 8: Predict on test data ----
y_pred = model.predict(X_test)

# ---- Step 9: Evaluate ----
mse = mean_squared_error(y_test, y_pred)   # avg of (actual - predicted)^2, lower = better
r2 = r2_score(y_test, y_pred)              # fraction of variance explained, 1 = perfect
print(f'Mean Squared Error : {mse:.4f}')
print(f'R-squared          : {r2:.4f}')
print(f'Coefficient (slope): {model.coef_[0]:.4f}')   # m
print(f'Intercept          : {model.intercept_:.4f}') # c

# ---- Step 10: Visualise actual points and fitted line ----
plt.scatter(X_test, y_test, color='steelblue', alpha=0.4, label='Actual')
plt.plot(X_test, y_pred, color='red', linewidth=2, label='Predicted')
plt.xlabel('Average Rooms (AveRooms)')
plt.ylabel('Median House Value')
plt.title('Linear Regression – California Housing')
plt.legend()
plt.tight_layout()
plt.show()
