# ============================================================
# Experiment No: 12
# SVM WITH MULTIPLE KERNELS ON FASHION MNIST DATASET
# ------------------------------------------------------------
# Aim     : Compare SVM with linear, polynomial and RBF kernels.
# Dataset : Datasets/fashion-mnist_test.csv  (loaded with read_csv)
#           Columns: label (0-9) + pixel1 ... pixel784 (values 0-255)
#           Subset used: 5,000 train / 1,000 test.
# ============================================================

import os                                                # build file paths
import numpy as np                                       # numerical arrays
import pandas as pd                                      # read_csv
import matplotlib.pyplot as plt                          # plotting
from sklearn.svm import SVC                              # SVM classifier
from sklearn.metrics import accuracy_score, f1_score     # evaluation
from sklearn.preprocessing import MinMaxScaler           # scale to [0, 1]

# Path to the Datasets folder (Ml lab/Datasets). On Colab use '/content'.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Datasets')

class_names = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# ---- Step 2: Load ----
df = pd.read_csv(os.path.join(DATA_DIR, 'fashion-mnist_test.csv'))
y_all = df['label'].values
X_all = df.drop('label', axis=1).values.astype(float)   # already flat (784 columns)

# ---- Step 4: Subset (non-overlapping train and test) ----
X_tr, y_tr = X_all[:5000], y_all[:5000]
X_te, y_te = X_all[5000:6000], y_all[5000:6000]

# ---- Step 3: Scale to [0, 1] (fit on train only) ----
scaler = MinMaxScaler().fit(X_tr)
X_train = scaler.transform(X_tr); y_train = y_tr
X_test = scaler.transform(X_te);  y_test = y_te

# ---- Step 5 – 7: Three kernels ----
# linear : straight hyperplane
# poly   : polynomial curves (degree=3)
# rbf    : Gaussian kernel, very flexible boundaries; C=10 -> less regularisation
kernels = [
    ('Linear', SVC(kernel='linear', C=1.0)),
    ('Polynomial', SVC(kernel='poly', degree=3, C=1.0)),
    ('RBF', SVC(kernel='rbf', C=10, gamma='scale')),
]

# ---- Step 8: Evaluate ----
predictions = {}
print(f"{'Kernel':15s} {'Accuracy':>10} {'Macro-F1':>10}")
for name, clf in kernels:
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    predictions[name] = y_pred
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')
    print(f'{name:15s} {acc:>10.4f} {f1:>10.4f}')

# ---- Step 9: Visualise misclassified samples for each kernel ----
fig, axes = plt.subplots(len(kernels), 5, figsize=(10, 7))
for row, (name, _) in enumerate(kernels):
    wrong = np.where(predictions[name] != y_test)[0][:5]   # first 5 mistakes
    for col in range(5):
        ax = axes[row, col]
        ax.axis('off')
        if col < len(wrong):
            i = wrong[col]
            ax.imshow(X_test[i].reshape(28, 28), cmap='gray')
            ax.set_title(f'P:{class_names[predictions[name][i]]}\n'
                         f'T:{class_names[y_test[i]]}', fontsize=7)
    axes[row, 0].text(-20, 14, name, fontsize=10, rotation=90, va='center')
plt.suptitle('Misclassified samples (P=Predicted, T=True)')
plt.tight_layout(); plt.show()
