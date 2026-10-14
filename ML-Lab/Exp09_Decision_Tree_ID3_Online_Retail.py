# ============================================================
# Experiment No: 9
# DECISION TREE (ID3) ON ONLINE RETAIL DATASET
# ------------------------------------------------------------
# Aim     : Segment customers (high / low value) from purchasing
#           behaviour using a Decision Tree with entropy (ID3 logic).
# Dataset : Datasets/Online_Retail.csv  (loaded with read_csv)
#           Columns: InvoiceNo, StockCode, Description, Quantity,
#                    InvoiceDate, UnitPrice, CustomerID, Country
#           Target : Segment (built from RFM features, see Step 5)
# ============================================================

import os                                                # build file paths
import numpy as np                                       # numerical arrays
import pandas as pd                                      # read_csv
import matplotlib.pyplot as plt                          # plotting
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Path to the Datasets folder (Ml lab/Datasets). On Colab use '/content'.
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Datasets')

# ---- Step 2: Load dataset ----
# The file contains some non-UTF-8 characters (e.g. £ in descriptions),
# so 'ISO-8859-1' encoding is used if UTF-8 fails.
path = os.path.join(DATA_DIR, 'Online_Retail.csv')
try:
    df = pd.read_csv(path, dtype={'CustomerID': str})
except UnicodeDecodeError:
    df = pd.read_csv(path, dtype={'CustomerID': str}, encoding='ISO-8859-1')

# Some versions of this dataset use slightly different column names - unify them
df = df.rename(columns={'Invoice': 'InvoiceNo', 'Price': 'UnitPrice',
                        'Customer ID': 'CustomerID'})
print(df.head())

# ---- Step 3: Clean ----
df = df[df['InvoiceNo'].astype(str).str[0] != 'C']    # invoices starting with 'C' = cancelled
df = df.dropna(subset=['CustomerID'])                 # need a customer to group by
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate']) # text -> datetime
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']   # amount spent per line

# ---- Step 4: RFM Features (one row per customer) ----
# Recency   = days since the customer's last purchase (lower = more recent)
# Frequency = number of distinct invoices (orders)
# Monetary  = total money spent
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)
rfm = df.groupby('CustomerID').agg(
    Recency=('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
    Frequency=('InvoiceNo', 'nunique'),
    Monetary=('TotalPrice', 'sum')
).reset_index()
print(rfm.head())

# ---- Step 5: Label – high value (1) if Monetary > median, else low (0) ----
threshold = rfm['Monetary'].median()
rfm['Segment'] = (rfm['Monetary'] > threshold).astype(int)

X = rfm[['Recency', 'Frequency', 'Monetary']].values
y = rfm['Segment'].values

# ---- Step 6: Split (80% / 20%) ----
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# ---- Step 7: Train ID3-style tree ----
# criterion='entropy' -> splits chosen by Information Gain (as in ID3)
# max_depth=5 limits tree size to avoid overfitting
clf = DecisionTreeClassifier(criterion='entropy',
                             max_depth=5, random_state=42)
clf.fit(X_train, y_train)

# ---- Step 8 & 9: Evaluate ----
y_pred = clf.predict(X_test)
print(f'Accuracy: {accuracy_score(y_test, y_pred):.4f}')
print(classification_report(y_test, y_pred,
                            target_names=['Low Value', 'High Value']))

# Feature importances: how much each feature reduced entropy overall
for name, imp in zip(['Recency', 'Frequency', 'Monetary'], clf.feature_importances_):
    print(f'{name:10s} importance = {imp:.4f}')

# ---- Step 10: Visualise tree ----
plt.figure(figsize=(16, 7))
plot_tree(clf, feature_names=['Recency', 'Frequency', 'Monetary'],
          class_names=['Low', 'High'], filled=True, fontsize=9)
plt.title('Decision Tree – Customer Segmentation')
plt.tight_layout(); plt.show()
