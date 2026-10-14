# ============================================================
# Experiment No: 7
# NAÏVE BAYES CLASSIFIER ON 20 NEWSGROUPS DATASET
# ------------------------------------------------------------
# Aim     : Classify news posts into topics and compare
#           Multinomial NB with Bernoulli NB.
# Dataset : sklearn.datasets.fetch_20newsgroups()  (loaded from package,
#           needs internet the first time). ~18,000 posts, 20 topics.
# ============================================================

import numpy as np                                       # numerical arrays
import matplotlib.pyplot as plt                          # plotting
from sklearn.datasets import fetch_20newsgroups          # dataset from package
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.metrics import accuracy_score, f1_score, classification_report

# ---- Step 2 & 3: Load dataset (headers/footers/quotes removed) ----
train_data = fetch_20newsgroups(subset='train',
                                remove=('headers', 'footers', 'quotes'))
test_data = fetch_20newsgroups(subset='test',
                               remove=('headers', 'footers', 'quotes'))
y_train, y_test = train_data.target, test_data.target   # topic number 0-19

# ---- Step 4: TF-IDF features for Multinomial NB ----
# TF-IDF = word frequency weighted down if the word is common in all posts
tfidf = TfidfVectorizer(stop_words='english', max_features=30000)
Xm_tr = tfidf.fit_transform(train_data.data)
Xm_te = tfidf.transform(test_data.data)

# ---- Step 5: Binary features for Bernoulli NB ----
# binary=True -> 1 if word is present in the post, 0 otherwise
bvec = CountVectorizer(stop_words='english',
                       max_features=30000, binary=True)
Xb_tr = bvec.fit_transform(train_data.data)
Xb_te = bvec.transform(test_data.data)

# ---- Step 6 & 7: Train ----
# Bayes rule: P(class | words) proportional to P(class) * product P(word | class)
mnb = MultinomialNB().fit(Xm_tr, y_train)
bnb = BernoulliNB().fit(Xb_tr, y_train)

# ---- Step 8 & 9: Evaluate ----
for name, clf, Xte in [('Multinomial NB', mnb, Xm_te),
                       ('Bernoulli NB', bnb, Xb_te)]:
    y_pred = clf.predict(Xte)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')   # average over 20 topics
    print(f'\n=== {name} ===')
    print(f'Accuracy : {acc:.4f}   Macro-F1 : {f1:.4f}')
    print(classification_report(y_test, y_pred,
                                target_names=train_data.target_names))
