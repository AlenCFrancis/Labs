# ============================================================
# Experiment No: 11
# LINEAR SVM ON IRIS DATASET
# ------------------------------------------------------------
# Aim     : Classify Iris (Setosa vs Rest) with a linear SVM,
#           visualise the decision boundary, margin and support vectors.
# Dataset : sklearn.datasets.load_iris()  (loaded from package)
#           150 flowers, features: sepal length, sepal width,
#           petal length, petal width. Classes: setosa, versicolor, virginica
# ============================================================

import numpy as np                                       # numerical arrays
import matplotlib.pyplot as plt                          # plotting
from sklearn.datasets import load_iris                   # dataset from package
from sklearn.preprocessing import StandardScaler         # scaling
from sklearn.svm import SVC                              # SVM classifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# ---- Step 2 & 3: Load and select 2 features ----
iris = load_iris()
X = iris.data[:, 2:4]                  # columns 2,3 = petal length & petal width
y = (iris.target == 0).astype(int)     # Step 4: 1 = Setosa, 0 = not Setosa

# ---- Step 5: Scale and split ----
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42)

# ---- Step 6: Train ----
# kernel='linear' -> straight-line boundary w.x + b = 0
# C = penalty for misclassified points (large C = narrow margin, small C = wide margin)
svm = SVC(kernel='linear', C=1.0)
svm.fit(X_train, y_train)

# ---- Step 7: Evaluate ----
y_pred = svm.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
print(classification_report(y_test, y_pred,
                            target_names=['Non-Setosa', 'Setosa']))

# Margin width = 2 / ||w||  (SVM chooses w to make this as large as possible)
w = svm.coef_[0]; b = svm.intercept_[0]
print(f'w = {w},  b = {b:.4f},  margin width = {2 / np.linalg.norm(w):.4f}')
print(f'Number of support vectors: {len(svm.support_vectors_)}')

# ---- Step 8: Decision boundary ----
# Build a fine grid over the plot area and predict the class of every grid point
h = 0.02
x0_min, x0_max = X_scaled[:, 0].min() - 0.5, X_scaled[:, 0].max() + 0.5
x1_min, x1_max = X_scaled[:, 1].min() - 0.5, X_scaled[:, 1].max() + 0.5
xx, yy = np.meshgrid(np.arange(x0_min, x0_max, h),
                     np.arange(x1_min, x1_max, h))
grid = np.c_[xx.ravel(), yy.ravel()]
Z = svm.predict(grid).reshape(xx.shape)

plt.contourf(xx, yy, Z, alpha=0.3, cmap='coolwarm')        # coloured regions
# Boundary (0) and margins (-1, +1) from the decision function w.x + b
D = svm.decision_function(grid).reshape(xx.shape)
plt.contour(xx, yy, D, levels=[-1, 0, 1], colors='k',
            linestyles=['--', '-', '--'])
plt.scatter(X_scaled[:, 0], X_scaled[:, 1], c=y,
            cmap='coolwarm', edgecolors='k', s=40)
# Support vectors = points on/inside the margin that define the boundary
plt.scatter(svm.support_vectors_[:, 0],
            svm.support_vectors_[:, 1],
            s=100, facecolors='none', edgecolors='k',
            linewidths=1.5, label='Support Vectors')
plt.xlabel('Petal Length (scaled)')
plt.ylabel('Petal Width (scaled)')
plt.title('Linear SVM – Iris (Setosa vs Rest)')
plt.legend(); plt.tight_layout(); plt.show()
