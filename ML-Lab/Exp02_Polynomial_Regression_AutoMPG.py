# ============================================================
# Experiment No: 2
# POLYNOMIAL REGRESSION ON AUTO MPG DATASET
# ------------------------------------------------------------
# Aim     : Predict MPG from engine displacement using polynomial
#           regression and compare with linear regression.
# Dataset : Datasets/AUTOMPG.csv  (loaded with read_csv)
#           Columns: (row index), displacement, cylinders, horsepower,
#                    weight, acceleration, model_year, origin, mpg
#           Target : mpg
# ============================================================

import os                                                # build file paths
import numpy as np                                       # numerical arrays
import pandas as pd                                      # read_csv
import matplotlib.pyplot as plt                          # plotting
from sklearn.linear_model import LinearRegression        # fits the coefficients
from sklearn.preprocessing import PolynomialFeatures     # makes x, x^2, x^3 ... columns
from sklearn.model_selection import train_test_split     # train / test split
from sklearn.metrics import mean_squared_error, r2_score # evaluation metrics

# Path to the Datasets folder (Ml lab/Datasets). On Colab use '/content'.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Datasets')

# ---- Step 2: Load dataset ----
# index_col=0 -> the first (unnamed) column is just a row number, use it as index
df = pd.read_csv(os.path.join(DATA_DIR, 'AUTOMPG.csv'), index_col=0)
print(df.head())

# ---- Step 3: Preprocess ----
df.dropna(inplace=True)            # drop rows with missing values (horsepower has a few)
X = df[['displacement']].values    # feature (2-D)
y = df['mpg'].values               # target

# ---- Step 4: Split (80% / 20%) ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# ---- Step 5 – 9: Fit and compare models ----
# degree 1 = straight line (baseline), degree 2/3/4 = curves
for degree in [1, 2, 3, 4]:
    poly = PolynomialFeatures(degree=degree)   # e.g. degree 2: x -> [1, x, x^2]
    X_tr_p = poly.fit_transform(X_train)
    X_te_p = poly.transform(X_test)

    # Linear regression on polynomial features = polynomial curve in x
    model = LinearRegression().fit(X_tr_p, y_train)
    y_pred = model.predict(X_te_p)

    mse = mean_squared_error(y_test, y_pred)   # lower = better
    r2 = r2_score(y_test, y_pred)              # closer to 1 = better
    label = 'Linear' if degree == 1 else f'Poly deg={degree}'
    print(f'{label:18s} MSE={mse:.3f}  R2={r2:.3f}')

    # ---- Step 10: Visualise ----
    # 200 evenly spaced x values -> smooth curve for this degree
    X_plot = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
    X_plot_p = poly.transform(X_plot)
    plt.plot(X_plot, model.predict(X_plot_p), label=label)

plt.scatter(X, y, color='grey', alpha=0.3, s=10, label='Data')   # actual points
plt.xlabel('Engine Displacement')
plt.ylabel('MPG')
plt.title('Polynomial Regression – Auto MPG')
plt.legend()
plt.tight_layout()
plt.show()
