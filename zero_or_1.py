import numpy as np
import sklearn.datasets
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.datasets._base import get_data_home

mnist = fetch_openml('mnist_784', version=1, cache=True, data_home='dataset')

N, d = mnist.data.shape

X_all = mnist.data
y_all = mnist.target


X0 = X_all[np.where(y_all == 0)[0]] # all digit 0
X1 = X_all[np.where(y_all == 1)[0]] # all digit 1
y0 = np.zeros(X0.shape[0]) # class 0 label
y1 = np.ones(X1.shape[0]) # class 1 label
X = np.concatenate((X0, X1), axis = 0) # all digits
y = np.concatenate((y0, y1)) # all labels
# split train and test

print(np.where(y_all == 0)[0])
