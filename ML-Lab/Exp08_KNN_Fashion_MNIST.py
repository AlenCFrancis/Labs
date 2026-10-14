# ============================================================
# Experiment No: 8
# K-NEAREST NEIGHBORS ON FASHION MNIST DATASET
# ------------------------------------------------------------
# Aim     : Classify clothing images with KNN and analyse how the
#           value of K affects accuracy and time.
# Dataset : Datasets/fashion-mnist_test.csv  (loaded with read_csv)
#           Columns: label (0-9) + pixel1 ... pixel784
#           (each 28x28 grey-scale image flattened to 784 values, 0-255)
#           The file has 10,000 images -> 8,000 train / 2,000 test.
# ============================================================

import os                                                # build file paths
import numpy as np                                       # numerical arrays
import pandas as pd                                      # read_csv
import matplotlib.pyplot as plt                          # plotting
from sklearn.neighbors import KNeighborsClassifier       # the model
from sklearn.metrics import accuracy_score               # % correct
import time                                              # timing each K

# Path to the Datasets folder (Ml lab/Datasets). On Colab use '/content'.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Datasets')

# ---- Step 2: Load Fashion MNIST from CSV ----
df = pd.read_csv(os.path.join(DATA_DIR, 'fashion-mnist_test.csv'))
print('Dataset shape:', df.shape)

y_all = df['label'].values                  # class label 0-9
X_all = df.drop('label', axis=1).values     # 784 pixel columns (already flat)

class_names = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

# ---- Step 3 & 4: (already flattened) Normalise to [0, 1] ----
# KNN uses Euclidean distance, so features should be on the same scale
X_all = X_all / 255.0

# ---- Step 5: Subset for speed ----
N_train, N_test = 8000, 2000
X_tr = X_all[:N_train];                 y_tr = y_all[:N_train]
X_te = X_all[N_train:N_train + N_test]; y_te = y_all[N_train:N_train + N_test]

# ---- Step 6 – 8: Evaluate different K ----
# KNN: label of a test image = majority label among its K nearest training images
k_values = [1, 3, 5, 7, 9, 11]
results = []
for k in k_values:
    t0 = time.time()
    clf = KNeighborsClassifier(n_neighbors=k, n_jobs=-1)   # n_jobs=-1 -> all CPU cores
    clf.fit(X_tr, y_tr)                                    # just stores training data
    acc = accuracy_score(y_te, clf.predict(X_te))          # distance calc + vote
    elapsed = time.time() - t0
    results.append((k, acc, elapsed))
    print(f'K={k:2d}  Acc={acc:.4f}  Time={elapsed:.1f}s')

# ---- Step 9: Plot accuracy vs K ----
ks, accs, _ = zip(*results)
plt.plot(ks, accs, marker='o')
plt.xlabel('K'); plt.ylabel('Accuracy')
plt.title('KNN Accuracy vs K – Fashion MNIST')
plt.tight_layout(); plt.show()

# ---- Step 10: Sample predictions using the best K ----
best_k = ks[int(np.argmax(accs))]
clf = KNeighborsClassifier(n_neighbors=best_k, n_jobs=-1).fit(X_tr, y_tr)
y_pred = clf.predict(X_te[:10])
fig, axes = plt.subplots(2, 5, figsize=(10, 4))
for i, ax in enumerate(axes.ravel()):
    ax.imshow(X_te[i].reshape(28, 28), cmap='gray')   # back to 28x28 image
    color = 'green' if y_pred[i] == y_te[i] else 'red'
    ax.set_title(f'P:{class_names[y_pred[i]]}\nT:{class_names[y_te[i]]}',
                 fontsize=8, color=color)
    ax.axis('off')
plt.suptitle(f'Sample predictions (K={best_k})  P=Predicted, T=True')
plt.tight_layout(); plt.show()
