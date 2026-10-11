import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv('/content/Testing.csv')


X = df.drop('Outcome', axis=1)
y = df['Outcome']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

linear = LinearRegression()
linear.fit(X_train, y_train)

alphas = np.logspace(-3, 3, 50)
ridge = RidgeCV(alphas=alphas, cv=5)
ridge.fit(X_train, y_train)

lasso = LassoCV(alphas=alphas, cv=5, random_state=42, max_iter=10000)
lasso.fit(X_train, y_train)


y_pred_linear = linear.predict(X_test)
y_pred_ridge = ridge.predict(X_test)
y_pred_lasso = lasso.predict(X_test)


print("Model Performance\n")

print(f"Linear Regression      MSE = {mean_squared_error(y_test, y_pred_linear):.4f}   R² = {r2_score(y_test, y_pred_linear):.4f}")
print(f"Ridge (L2)             MSE = {mean_squared_error(y_test, y_pred_ridge):.4f}   R² = {r2_score(y_test, y_pred_ridge):.4f}")
print(f"Lasso (L1)             MSE = {mean_squared_error(y_test, y_pred_lasso):.4f}   R² = {r2_score(y_test, y_pred_lasso):.4f}")


coef_df = pd.DataFrame({
    'Feature': X.columns,
    'Linear Regression': linear.coef_,
    'Ridge (L2)': ridge.coef_,
    'Lasso (L1)': lasso.coef_
})

plt.figure(figsize=(10,7))

x = np.arange(len(coef_df))
width = 0.25

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