# ============================================================
# Experiment : Polynomial Regression
# Dataset    : Auto MPG (Datasets/AUTOMPG.csv)
# Columns    : (index), displacement, cylinders, horsepower, weight,
#              acceleration, model_year, origin, mpg
# Target     : mpg (miles per gallon)
# Goal       : Predict mpg from engine displacement and compare a
#              straight line (degree 1) with curves of degree 2, 3, 4.
# ============================================================

import os                                             # to build the dataset file path
import numpy as np                                    # numerical arrays
import pandas as pd                                   # reading the CSV
import matplotlib.pyplot as plt                       # plotting
from sklearn.linear_model import LinearRegression     # fits the coefficients
from sklearn.preprocessing import PolynomialFeatures  # creates x, x^2, x^3 ... columns
from sklearn.model_selection import train_test_split  # split data into train / test
from sklearn.metrics import mean_squared_error, r2_score  # evaluation metrics

# Folder that contains the CSV files (Ml lab/Datasets).
# On Colab change this to '/content'.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Datasets')

# Load the dataset (398 cars)
df = pd.read_csv(os.path.join(DATA_DIR, 'AUTOMPG.csv'))

# The first CSV column is an unnamed row index - pandas calls it 'Unnamed: 0'. Drop it.
if 'Unnamed: 0' in df.columns:
    df.drop(columns=['Unnamed: 0'], inplace=True)

# Remove rows with missing values (horsepower has a few blanks)
df.dropna(inplace=True)

# X = engine displacement (2-D for sklearn), y = mpg
X = df[['displacement']].values
y = df['mpg'].values

# 80% train / 20% test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Try polynomial degrees 1 to 4
for degree in [1, 2, 3, 4]:
    # e.g. degree=2 turns x into [1, x, x^2]
    poly = PolynomialFeatures(degree=degree)

    X_tr_p = poly.fit_transform(X_train)
    X_te_p = poly.transform(X_test)

    # Linear regression on the expanded features = polynomial curve in x
    model = LinearRegression().fit(X_tr_p, y_train)
    y_pred = model.predict(X_te_p)

    # Lower MSE / higher R2 = better fit on the test data
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    label = 'Linear' if degree == 1 else f'Poly deg={degree}'
    print(f'{label:18s} MSE={mse:.3f} R2={r2:.3f}')

    # 200 evenly spaced displacement values -> draws a smooth curve
    X_plot = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
    X_plot_p = poly.transform(X_plot)

    plt.plot(X_plot, model.predict(X_plot_p), label=label)

# Actual data points in grey behind the curves
plt.scatter(X, y, color='grey', alpha=0.3, s=10, label='Data')
plt.xlabel('Engine Displacement')
plt.ylabel('MPG')
plt.title('Polynomial Regression – Auto MPG')
plt.legend()
plt.tight_layout()
plt.show()