import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


df = pd.read_csv('/content/fetch_california_housing.csv')


X = df[['AveRooms']].values
y = df['MedHouseVal'].values


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)


model = LinearRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)


mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Squared Error : {mse:.4f}')
print(f'R-squared : {r2:.4f}')
print(f'Coefficient (slope): {model.coef_[0]:.4f}')
print(f'Intercept : {model.intercept_:.4f}')


plt.scatter(X_test, y_test, color='steelblue', alpha=0.4, label='Actual')
plt.plot(X_test, y_pred, color='red', linewidth=2, label='Predicted')
plt.xlabel('Average Rooms (AveRooms)')
plt.ylabel('Median House Value')
plt.title('Linear Regression – California Housing')
plt.legend()
plt.tight_layout()
plt.show()