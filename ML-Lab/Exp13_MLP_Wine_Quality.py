# ============================================================
# Experiment No: 13
# MULTILAYER FEED-FORWARD NETWORK ON WINE QUALITY DATASET
# ------------------------------------------------------------
# Aim     : Train MLPs with different numbers of hidden layers /
#           neurons and compare their performance.
# Dataset : Red Wine Quality (UCI) - loaded with read_csv from the URL
#           (needs internet). Separator is ';'.
#           Columns: fixed acidity, volatile acidity, citric acid,
#                    residual sugar, chlorides, free sulfur dioxide,
#                    total sulfur dioxide, density, pH, sulphates, alcohol
#           Target : quality -> 1 (good) if quality >= 7 else 0 (poor)
#           To use a downloaded copy instead, put winequality-red.csv
#           in the Datasets folder - the code will pick it up.
# ============================================================

import os                                                # build file paths
import numpy as np                                       # numerical arrays
import pandas as pd                                      # read_csv
import matplotlib.pyplot as plt                          # plotting
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential           # layer-by-layer model
from tensorflow.keras.layers import Dense, Dropout, Input

# Path to the Datasets folder (Ml lab/Datasets). On Colab use '/content'.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Datasets')

# ---- Step 2: Load (local file if present, otherwise UCI URL) ----
local_path = os.path.join(DATA_DIR, 'winequality-red.csv')
url = ('https://archive.ics.uci.edu/ml/machine-learning-databases/'
       'wine-quality/winequality-red.csv')
df = pd.read_csv(local_path if os.path.exists(local_path) else url, sep=';')
print(df.head())

# ---- Step 3: Preprocess ----
X = df.drop('quality', axis=1).values
y = (df['quality'] >= 7).astype(int).values      # binary target
X = StandardScaler().fit_transform(X)            # neural nets train better on scaled data

# ---- Step 4: Split (80% / 20%) ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# ---- Step 5: Architectures to compare (neurons per hidden layer) ----
architectures = [
    ('1 Layer – 64', [64]),
    ('2 Layers – 128,64', [128, 64]),
    ('3 Layers – 128,64,32', [128, 64, 32]),
]

histories = {}
for name, layers in architectures:
    model = Sequential()
    model.add(Input(shape=(X_train.shape[1],)))            # 11 input features
    model.add(Dense(layers[0], activation='relu'))         # first hidden layer
    for units in layers[1:]:
        model.add(Dense(units, activation='relu'))         # extra hidden layers
        model.add(Dropout(0.3))                            # randomly drop 30% -> less overfitting
    model.add(Dense(1, activation='sigmoid'))              # output: probability of 'good'

    # ---- Step 6: Compile ----
    model.compile(optimizer='adam',
                  loss='binary_crossentropy', metrics=['accuracy'])

    # ---- Step 7: Train (50 epochs, 20% of train used for validation) ----
    hist = model.fit(X_train, y_train, epochs=50,
                     batch_size=32, validation_split=0.2, verbose=0)
    histories[name] = hist

    # ---- Step 8: Evaluate on test set ----
    loss, acc = model.evaluate(X_test, y_test, verbose=0)
    print(f'{name:30s} Test Acc={acc:.4f}  Loss={loss:.4f}')

# ---- Step 9: Training / validation curves ----
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for name, hist in histories.items():
    axes[0].plot(hist.history['val_accuracy'], label=name)
    axes[1].plot(hist.history['val_loss'], label=name)
axes[0].set_title('Validation Accuracy'); axes[0].set_ylabel('Accuracy')
axes[1].set_title('Validation Loss');     axes[1].set_ylabel('Loss')
for ax in axes:
    ax.set_xlabel('Epoch'); ax.legend()
plt.suptitle('MLP Architectures – Wine Quality')
plt.tight_layout(); plt.show()
