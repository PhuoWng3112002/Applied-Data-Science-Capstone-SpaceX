import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

data = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")
X = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv')

Y = data['Class'].to_numpy()
transform = preprocessing.StandardScaler()
X = transform.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=2)

# 1. Logistic Regression
logreg_cv = GridSearchCV(LogisticRegression(), {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}, cv=10).fit(X_train, Y_train)

# 2. SVM
svm_cv = GridSearchCV(SVC(), {'kernel': ('linear', 'rbf', 'poly', 'sigmoid'), 'C': np.logspace(-3, 3, 5), 'gamma': np.logspace(-3, 3, 5)}, cv=10).fit(X_train, Y_train)

# 3. Decision Tree
tree_cv = GridSearchCV(DecisionTreeClassifier(), {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_depth': [2*n for n in range(1, 10)],
    'max_features': ['sqrt'],
    'min_samples_leaf': [1, 2, 4],
    'min_samples_split': [2, 5, 10]
}, cv=10).fit(X_train, Y_train)

# 4. KNN
knn_cv = GridSearchCV(KNeighborsClassifier(), {'n_neighbors': list(range(1, 11)), 'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'], 'p': [1, 2]}, cv=10).fit(X_train, Y_train)

models = {
    'Logistic Regression': logreg_cv.score(X_test, Y_test),
    'SVM': svm_cv.score(X_test, Y_test),
    'Decision Tree': tree_cv.score(X_test, Y_test),
    'KNN': knn_cv.score(X_test, Y_test)
}
print("Test Accuracies:", models)

# Vẽ biểu đồ so sánh Accuracy
plt.bar(models.keys(), models.values(), color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
plt.ylabel('Test Accuracy')
plt.title('Classification Model Comparison')
plt.ylim(0, 1.0)
plt.show()

# Confusion Matrix cho Logistic Regression (hoặc mô hình tốt nhất)
yhat = logreg_cv.predict(X_test)
cm = confusion_matrix(Y_test, yhat)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Confusion Matrix')
plt.show()