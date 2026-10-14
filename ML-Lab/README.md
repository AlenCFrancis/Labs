# Machine Learning Laboratory (24CSL507)

Python programs for all 14 experiments of the Machine Learning Laboratory record.
Every program has `#` comments explaining each step.

---

## Experiments

| No. | File | Dataset | How it is loaded |
|---|---|---|---|
| 1 | `Exp01_Linear_Regression_California_Housing.py` | California Housing | `read_csv` (features) + `fetch_california_housing` (target) |
| 2 | `Exp02_Polynomial_Regression_AutoMPG.py` | Auto MPG | `read_csv('AUTOMPG.csv')` |
| 3 | `Exp03_Ridge_Lasso_Diabetes.py` | Diabetes (sklearn) | `load_diabetes()` |
| 4 | `Exp04_Logistic_MLE_MAP_Breast_Cancer.py` | Breast Cancer Wisconsin | `read_csv('breast-cancer-wisconsin-data_data.csv')` |
| 5 | `Exp05_MLE_MAP_Multinomial_20Newsgroups.py` | 20 Newsgroups | `fetch_20newsgroups()` |
| 6 | `Exp06_Logistic_Regression_Pima_Diabetes.py` | Pima Indians Diabetes | `read_csv('diabetes_dataset.csv')` |
| 7 | `Exp07_Naive_Bayes_20Newsgroups.py` | 20 Newsgroups | `fetch_20newsgroups()` |
| 8 | `Exp08_KNN_Fashion_MNIST.py` | Fashion MNIST | `read_csv('fashion-mnist_test.csv')` |
| 9 | `Exp09_Decision_Tree_ID3_Online_Retail.py` | Online Retail | `read_csv('Online_Retail.csv')` |
| 10 | `Exp10_Logistic_vs_Decision_Tree_Adult.py` | Adult Income | `read_csv('adult.csv')` |
| 11 | `Exp11_Linear_SVM_Iris.py` | Iris | `load_iris()` |
| 12 | `Exp12_SVM_Kernels_Fashion_MNIST.py` | Fashion MNIST | `read_csv('fashion-mnist_test.csv')` |
| 13 | `Exp13_MLP_Wine_Quality.py` | Red Wine Quality | `read_csv` from UCI URL |
| 14 | `Exp14_NN_Activation_Functions_MNIST.py` | MNIST | `keras.datasets.mnist` |

---

## Important: Dataset Setup & File Paths

The CSV programs read from a `Datasets` folder two levels above this one:

```
Ml lab/
├── Datasets/          <- put the CSV files here
└── Labs/
    └── ML-Lab/        <- these programs
```

Each program has a `DATA_DIR` variable near the top. On **Google Colab**, upload the CSV
and change it to `DATA_DIR = '/content'`.

Package datasets (sklearn / keras) download automatically and need internet the first time.

## Requirements

```
pip install numpy pandas matplotlib scikit-learn tensorflow
```
