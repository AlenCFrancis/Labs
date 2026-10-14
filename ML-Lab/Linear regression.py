# ============================================================
# Experiment : Simple Linear Regression
# Dataset    : California Housing (Datasets/california_housing.csv)
# Columns    : MedInc, HouseAge, AveRooms, AveBedrms, Population,
#              AveOccup, Latitude, Longitude
# Target     : MedHouseVal (median house value, in $100,000s)
# Goal       : Predict house value from ONE feature (AveRooms)
#              using the straight line  y = m*x + c
# ============================================================

import os                                             # to build the dataset file path
import numpy as np                                    # numerical arrays
import pandas as pd                                   # reading the CSV
import matplotlib.pyplot as plt                       # plotting
from sklearn.model_selection import train_test_split  # split data into train / test
from sklearn.linear_model import LinearRegression     # the regression model
from sklearn.metrics import mean_squared_error, r2_score  # evaluation metrics

# Folder that contains the CSV files (Ml lab/Datasets).
# On Colab change this to '/content'.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Datasets')

# Load the 8 feature columns (20,640 rows)
df = pd.read_csv(os.path.join(DATA_DIR, 'california_housing.csv'))

# The local CSV has only the features - it does NOT include the target column.
# The rows are in the same order as sklearn's copy, so we take the target from there.
# (Needs internet the first time; sklearn caches it afterwards.)
if 'MedHouseVal' not in df.columns:
    from sklearn.datasets import fetch_california_housing
    df['MedHouseVal'] = fetch_california_housing().target

# X = input feature (average rooms per house) -> double brackets keep it 2-D for sklearn
# y = output / target (median house value)
X = df[['AveRooms']].values
y = df['MedHouseVal'].values

# 80% data for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Fit the line: finds slope (m) and intercept (c) that minimise squared error
model = LinearRegression()
model.fit(X_train, y_train)

# Predict house values for the test data
y_pred = model.predict(X_test)

# MSE = average of (actual - predicted)^2  -> lower is better
# R2  = how much of the variation in y the model explains -> 1 is perfect
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error : {mse:.4f}')
print(f'R-squared : {r2:.4f}')
print(f'Coefficient (slope): {model.coef_[0]:.4f}')   # m in y = m*x + c
print(f'Intercept : {model.intercept_:.4f}')          # c in y = m*x + c

# Plot actual points (blue) and the fitted regression line (red)
plt.scatter(X_test, y_test, color='steelblue', alpha=0.4, label='Actual')
plt.plot(X_test, y_pred, color='red', linewidth=2, label='Predicted')
plt.xlabel('Average Rooms (AveRooms)')
plt.ylabel('Median House Value')
plt.title('Linear Regression – California Housing')
plt.legend()
plt.tight_layout()
plt.show()