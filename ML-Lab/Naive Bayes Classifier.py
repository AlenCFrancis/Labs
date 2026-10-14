# ============================================================
# Experiment : Naive Bayes Text Classification
# Dataset    : 20 Newsgroups (downloaded automatically by sklearn,
#              needs internet the first time - no local CSV needed)
# Data       : ~18,000 news posts split into 20 topics
#              (e.g. sci.space, rec.autos, comp.graphics ...)
# Goal       : Compare Multinomial NB (word counts / TF-IDF) with
#              Bernoulli NB (word present / absent).
# ============================================================

import numpy as np                    # numerical arrays
import matplotlib.pyplot as plt       # plotting (imported, not used here)

from sklearn.datasets import fetch_20newsgroups                             # dataset loader
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer # text -> numbers
from sklearn.naive_bayes import MultinomialNB, BernoulliNB                  # the two NB models
from sklearn.metrics import accuracy_score, f1_score, classification_report # evaluation

# Load the training posts. Removing headers/footers/quotes stops the model
# from "cheating" using e-mail addresses or signatures.
train_data = fetch_20newsgroups(
    subset='train',
    remove=('headers', 'footers', 'quotes')
)

# Load the test posts (already separated by the dataset)
test_data = fetch_20newsgroups(
    subset='test',
    remove=('headers', 'footers', 'quotes')
)

# Target = topic number (0-19) of each post
y_train, y_test = train_data.target, test_data.target

# ---------- Features for Multinomial NB ----------
# TF-IDF: word frequency, down-weighting words common in every post.
# stop_words removes words like "the", "is"; keep the 30,000 most frequent words.
tfidf = TfidfVectorizer(
    stop_words='english',
    max_features=30000
)

Xm_tr = tfidf.fit_transform(train_data.data)   # learn vocabulary on train + transform
Xm_te = tfidf.transform(test_data.data)        # only transform test (same vocabulary)

# ---------- Features for Bernoulli NB ----------
# binary=True -> 1 if the word appears in the post, 0 if not (counts ignored)
bvec = CountVectorizer(
    stop_words='english',
    max_features=30000,
    binary=True
)

Xb_tr = bvec.fit_transform(train_data.data)
Xb_te = bvec.transform(test_data.data)

# Train both models.
# NB uses Bayes' theorem: P(topic | words) is proportional to P(topic) * product of P(word | topic)
mnb = MultinomialNB().fit(Xm_tr, y_train)
bnb = BernoulliNB().fit(Xb_tr, y_train)

# Evaluate each model on its own type of test features
for name, clf, Xte in [
    ('Multinomial NB', mnb, Xm_te),
    ('Bernoulli NB', bnb, Xb_te)
]:
    y_pred = clf.predict(Xte)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')   # macro = average F1 over all 20 topics equally

    print(f'\n=== {name} ===')
    print(f'Accuracy : {acc:.4f} Macro-F1 : {f1:.4f}')

    # Precision / recall / F1 for every topic
    print(
        classification_report(
            y_test,
            y_pred,
            target_names=train_data.target_names
        )
    )