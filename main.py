# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and setting
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
iris_dataset = load_iris()
x = iris_dataset.data
y = iris_dataset.target
x_train, x_test, y_train, y_test = train_test_split(x, y)
model = KNeighborsClassifier(n_neighbors=7, p=2, weights='distance')
new_model = model.fit(x_train, y_train)
print(new_model.score(x_test, y_test))


