import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.metrics import accuracy_score, f1_score, classification_report

train_data = fetch_20newsgroups(
    subset='train',
    remove=('headers', 'footers', 'quotes')
)

test_data = fetch_20newsgroups(
    subset='test',
    remove=('headers', 'footers', 'quotes')
)

y_train, y_test = train_data.target, test_data.target

tfidf = TfidfVectorizer(
    stop_words='english',
    max_features=30000
)

Xm_tr = tfidf.fit_transform(train_data.data)
Xm_te = tfidf.transform(test_data.data)

bvec = CountVectorizer(
    stop_words='english',
    max_features=30000,
    binary=True
)

Xb_tr = bvec.fit_transform(train_data.data)
Xb_te = bvec.transform(test_data.data)


mnb = MultinomialNB().fit(Xm_tr, y_train)
bnb = BernoulliNB().fit(Xb_tr, y_train)

for name, clf, Xte in [
    ('Multinomial NB', mnb, Xm_te),
    ('Bernoulli NB', bnb, Xb_te)
]:
    y_pred = clf.predict(Xte)
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='macro')

    print(f'\n=== {name} ===')
    print(f'Accuracy : {acc:.4f} Macro-F1 : {f1:.4f}')

    print(
        classification_report(
            y_test,
            y_pred,
            target_names=train_data.target_names
        )
    )