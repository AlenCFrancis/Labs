# ============================================================
# Experiment No: 14
# NEURAL NETWORK WITH DIFFERENT ACTIVATION FUNCTIONS ON MNIST
# ------------------------------------------------------------
# Aim     : Compare Sigmoid, ReLU and Tanh activations in the same
#           network on handwritten-digit classification.
# Dataset : tensorflow.keras.datasets.mnist  (loaded from package,
#           downloads automatically). 60,000 train + 10,000 test
#           images of digits 0-9, each 28x28 pixels (0-255).
# ============================================================

import numpy as np                                       # numerical arrays
import matplotlib.pyplot as plt                          # plotting
import time                                              # training time
import tensorflow as tf
from tensorflow.keras.datasets import mnist              # dataset from package
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Input
from tensorflow.keras.utils import to_categorical        # one-hot encoding

# ---- Step 2 & 3: Load and preprocess ----
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = X_train / 255.0                 # pixels -> [0, 1]
X_test = X_test / 255.0

# ---- Step 4: One-hot encode labels ----
# e.g. 3 -> [0,0,0,1,0,0,0,0,0,0]  (needed for categorical cross-entropy)
y_train_oh = to_categorical(y_train, 10)
y_test_oh = to_categorical(y_test, 10)

activations = ['sigmoid', 'relu', 'tanh']
histories = {}

for act in activations:
    # ---- Step 5 & 6: Same architecture, only activation changes ----
    # Input(28x28) -> Flatten(784) -> Dense(128) -> Dense(64) -> Dense(10, softmax)
    model = Sequential([
        Input(shape=(28, 28)),
        Flatten(),                         # 28x28 image -> 784 vector
        Dense(128, activation=act),
        Dense(64, activation=act),
        Dense(10, activation='softmax'),   # Step 7: probabilities for 10 digits
    ])
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # ---- Step 8: Train for 20 epochs (10% of train used for validation) ----
    t0 = time.time()
    hist = model.fit(X_train, y_train_oh, epochs=20,
                     batch_size=128, validation_split=0.1,
                     verbose=0)
    elapsed = time.time() - t0

    # ---- Step 9: Test accuracy and training time ----
    loss, acc = model.evaluate(X_test, y_test_oh, verbose=0)
    print(f'{act.upper():8s} Acc={acc:.4f}  Loss={loss:.4f}  Time={elapsed:.1f}s')
    histories[act] = hist

# ---- Step 10: Plot validation accuracy and loss ----
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
for act, hist in histories.items():
    axes[0].plot(hist.history['val_accuracy'], label=act)
    axes[1].plot(hist.history['val_loss'], label=act)
axes[0].set_title('Validation Accuracy')
axes[1].set_title('Validation Loss')
for ax in axes:
    ax.set_xlabel('Epoch'); ax.legend()
plt.tight_layout(); plt.show()
