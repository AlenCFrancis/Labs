# ============================================================
# Experiment No: 5
# MLE AND MAP FOR MULTINOMIAL DISTRIBUTION ON 20 NEWSGROUPS DATASET
# ------------------------------------------------------------
# Aim     : Estimate word probabilities P(word | class) using MLE and
#           MAP (Dirichlet prior) and see the effect of the prior strength.
# Dataset : sklearn.datasets.fetch_20newsgroups()  (loaded from package,
#           needs internet the first time). 4 categories used.
# Formulas:
#   MLE : P(w|c) = count(w,c) / sum_w count(w,c)
#   MAP : P(w|c) = (count(w,c) + alpha) / (sum_w count(w,c) + alpha*V)
#         alpha = Dirichlet prior strength, V = vocabulary size
# ============================================================

import numpy as np                                       # numerical arrays
import matplotlib.pyplot as plt                          # plotting
from sklearn.datasets import fetch_20newsgroups          # dataset from package
from sklearn.feature_extraction.text import CountVectorizer  # text -> word counts
from sklearn.naive_bayes import MultinomialNB            # multinomial model
from sklearn.metrics import accuracy_score, f1_score     # evaluation

# ---- Step 2: Load 4 categories ----
cats = ['sci.space', 'rec.sport.hockey',
        'talk.politics.guns', 'comp.graphics']
# remove headers/footers/quotes so the model learns from the actual text only
train = fetch_20newsgroups(subset='train', categories=cats,
                           remove=('headers', 'footers', 'quotes'))
test = fetch_20newsgroups(subset='test', categories=cats,
                          remove=('headers', 'footers', 'quotes'))

# ---- Step 3: Vectorise (word counts) ----
vec = CountVectorizer(stop_words='english', max_features=5000)  # top 5000 words
X_train = vec.fit_transform(train.data)   # learn vocabulary from train
X_test = vec.transform(test.data)         # reuse same vocabulary for test
y_train, y_test = train.target, test.target
vocab = np.array(vec.get_feature_names_out())
V = len(vocab)

# ---- Step 4 & 5: Manual MLE and MAP estimates for one class ----
c = list(train.target_names).index('sci.space')          # sample category
counts = np.asarray(X_train[y_train == c].sum(axis=0)).ravel()  # count(w, c)
total = counts.sum()                                     # sum_w count(w, c)

p_mle = counts / total                                   # MLE
p_map = (counts + 1) / (total + 1 * V)                   # MAP with alpha = 1 (Laplace)
print(f'Words never seen in sci.space -> MLE prob 0 for {np.sum(p_mle == 0)} words, '
      f'MAP prob min = {p_map.min():.2e} (never zero)')

# ---- Step 6 – 8: Train and evaluate for different alpha values ----
# alpha ~ 0 behaves like MLE; larger alpha = stronger (smoother) prior
alphas = [1e-9, 0.01, 0.1, 1.0, 10.0]
print(f"\n{'Alpha':>12} {'Accuracy':>10} {'F1':>10}")
for alpha in alphas:
    clf = MultinomialNB(alpha=alpha)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')   # average F1 over the 4 classes
    label = 'MLE' if alpha < 1e-5 else f'MAP(a={alpha})'
    print(f'{label:>12} {acc:>10.4f} {f1:>10.4f}')

# ---- Step 9: Effect of alpha on top-word probabilities (sci.space) ----
top = np.argsort(counts)[::-1][:10]                      # 10 most frequent words
plt.figure(figsize=(10, 4))
width = 0.8 / len(alphas)
for i, alpha in enumerate(alphas):
    p = (counts + alpha) / (total + alpha * V)           # MAP formula
    plt.bar(np.arange(10) + i * width, p[top], width=width, label=f'alpha={alpha}')
plt.xticks(np.arange(10) + 0.4 - width / 2, vocab[top], rotation=45)
plt.ylabel('P(word | sci.space)')
plt.title('Effect of Dirichlet prior (alpha) on top-word probabilities')
plt.legend()
plt.tight_layout()
plt.show()
