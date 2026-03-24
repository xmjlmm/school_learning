import numpy as np
import time
import optuna
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def loadData(fileName):
    print('start to read data')
    dataArr = []
    labelArr = []
    fr = open(fileName, 'r')
    for line in fr.readlines():
        curLine = line.strip().split(',')
        if int(curLine[0]) >= 5:
            labelArr.append(1)
        else:
            labelArr.append(-1)
        dataArr.append([int(num) / 255 for num in curLine[1:]])
    return dataArr, labelArr


class Perceptron:
    def __init__(self, iter=50, h=0.0001):
        self.iter = iter
        self.h = h
        self.w = None
        self.b = None

    def fit(self, dataArr, labelArr):
        dataMat = np.mat(dataArr)
        labelMat = np.mat(labelArr).T
        m, n = np.shape(dataMat)
        self.w = np.zeros((1, np.shape(dataMat)[1]))
        self.b = 0

        for k in range(self.iter):
            for i in range(m):
                xi = dataMat[i]
                yi = labelMat[i]
                if -1 * yi * (self.w * xi.T + self.b) >= 0:
                    self.w = self.w + self.h * yi * xi
                    self.b = self.b + self.h * yi

    def predict(self, dataArr):
        dataMat = np.mat(dataArr)
        m, _ = np.shape(dataMat)
        predictions = []
        for i in range(m):
            xi = dataMat[i]
            result = np.sign(self.w * xi.T + self.b)
            predictions.append(int(result[0, 0]))
        return predictions


def objective_perceptron(trial):
    iter = trial.suggest_int('iter', 10, 100)
    h = trial.suggest_loguniform('h', 1e-5, 1e-2)
    perceptron = Perceptron(iter=iter, h=h)
    perceptron.fit(X_train, y_train)
    y_pred = perceptron.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


def objective_knn(trial):
    k = trial.suggest_int('k', 1, 10)
    from sklearn.neighbors import KNeighborsClassifier
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X_train, y_train)
    y_pred = knn.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


def objective_adaboost(trial):
    n_estimators = trial.suggest_int('n_estimators', 10, 100)
    learning_rate = trial.suggest_loguniform('learning_rate', 0.01, 1.0)
    adaboost = AdaBoostClassifier(n_estimators=n_estimators, learning_rate=learning_rate)
    adaboost.fit(X_train, y_train)
    y_pred = adaboost.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


def objective_svm(trial):
    kernel = trial.suggest_categorical('kernel', ['linear', 'rbf', 'poly'])
    C = trial.suggest_loguniform('C', 0.1, 10)
    gamma = trial.suggest_loguniform('gamma', 0.001, 1) if kernel != 'linear' else None
    svm = SVC(kernel=kernel, C=C, gamma=gamma)
    svm.fit(X_train, y_train)
    y_pred = svm.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


def objective_decision_tree(trial):
    max_depth = trial.suggest_int('max_depth', 3, 20)
    min_samples_split = trial.suggest_int('min_samples_split', 2, 10)
    decision_tree = DecisionTreeClassifier(max_depth=max_depth, min_samples_split=min_samples_split)
    decision_tree.fit(X_train, y_train)
    y_pred = decision_tree.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


def objective_naive_bayes(trial):
    var_smoothing = trial.suggest_loguniform('var_smoothing', 1e-10, 1e-2)
    naive_bayes = GaussianNB(var_smoothing=var_smoothing)
    naive_bayes.fit(X_train, y_train)
    y_pred = naive_bayes.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy


if __name__ == '__main__':
    trainData, trainLabel = loadData(r"F:\学习\大三下\机器学习实验\Mnist\mnist_train.csv")
    X_train, X_test, y_train, y_test = train_test_split(trainData, trainLabel, test_size=0.3, random_state=42)

    study_perceptron = optuna.create_study(direction='maximize')
    study_perceptron.optimize(objective_perceptron, n_trials=20)

    study_knn = optuna.create_study(direction='maximize')
    study_knn.optimize(objective_knn, n_trials=20)

    study_adaboost = optuna.create_study(direction='maximize')
    study_adaboost.optimize(objective_adaboost, n_trials=20)

    study_svm = optuna.create_study(direction='maximize')
    study_svm.optimize(objective_svm, n_trials=20)

    study_decision_tree = optuna.create_study(direction='maximize')
    study_decision_tree.optimize(objective_decision_tree, n_trials=20)

    study_naive_bayes = optuna.create_study(direction='maximize')
    study_naive_bayes.optimize(objective_naive_bayes, n_trials=20)

    print("Perceptron best accuracy:", study_perceptron.best_value)
    print("Perceptron best params:", study_perceptron.best_params)
    print("KNN best accuracy:", study_knn.best_value)
    print("KNN best params:", study_knn.best_params)
    print("Adaboost best accuracy:", study_adaboost.best_value)
    print("Adaboost best params:", study_adaboost.best_params)
    print("SVM best accuracy:", study_svm.best_value)
    print("SVM best params:", study_svm.best_params)
    print("Decision Tree best accuracy:", study_decision_tree.best_value)
    print("Decision Tree best params:", study_decision_tree.best_params)
    print("Naive Bayes best accuracy:", study_naive_bayes.best_value)
    print("Naive Bayes best params:", study_naive_bayes.best_params)
    