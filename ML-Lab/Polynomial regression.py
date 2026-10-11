import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score


df = pd.read_csv('/content/AUTOMPG.csv')

if 'Unnamed: 0' in df.columns:
    df.drop(columns=['Unnamed: 0'], inplace=True)

df.dropna(inplace=True)

X = df[['displacement']].values
y = df['mpg'].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

for degree in [1, 2, 3, 4]:
    poly = PolynomialFeatures(degree=degree)

    X_tr_p = poly.fit_transform(X_train)
    X_te_p = poly.transform(X_test)

    model = LinearRegression().fit(X_tr_p, y_train)
    y_pred = model.predict(X_te_p)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    label = 'Linear' if degree == 1 else f'Poly deg={degree}'
    print(f'{label:18s} MSE={mse:.3f} R2={r2:.3f}')

    X_plot = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
    X_plot_p = poly.transform(X_plot)

    plt.plot(X_plot, model.predict(X_plot_p), label=label)

plt.scatter(X, y, color='grey', alpha=0.3, s=10, label='Data')
plt.xlabel('Engine Displacement')
plt.ylabel('MPG')
plt.title('Polynomial Regression – Auto MPG')
plt.legend()
plt.tight_layout()
plt.show()