'''
Class which initialises the following classifiers -
1. linear regression
2. logistic regression
3. SVM
4. Decision Trees
5. Random forest

Also splits the training data into training and validation sets
'''
import sklearn
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.tree import DecisionTreeClassifier

class Data(object):
    def __init__(self, train_features, train_labels, test_features, test_labels):
        self.train_data = []
        self.train_data_labels = []
        self.valid_data = []
        self.valid_data_labels = []

        self.test_data = test_features
        self.test_data_labels = test_labels

        stratifiedsplit = StratifiedShuffleSplit(n_splits=5, shuffle=False, random_state=42)

        for train_index, valid_index in stratifiedsplit.split(train_features, train_labels):
            self.train_data.append(train_features[train_index])
            self.train_data_labels.append(train_labels[train_index])
            self.valid_data.append(train_features[valid_index])
            self.valid_data_labels.append(train_features[valid_index])


class Classifiers(object):
    def __init__(self, data):
        self.train_data = data.train_data
        self.train_data_labels = data.train_data_labels
        self.valid_data = data.valid_data
        self.valid_data_labels = data.valid_data_labels
        self.test_data = data.test_data
        self.test_data_labels = data.test_data_labels
        self.folds = 5

    def svm_classify(self, kernel='linear', max_iter=10, *kwargs):
        svc = SVC(kernel=kernel, max_iter=max_iter)

        accuracy = 0
        print ('Learning using SVM')
        for f in range(self.folds):
            svc.fit(self.train_data[f], self.train_data_labels[f])
            print ('Training accuracy - %f' %svc.score(self.train_data[f], self.train_data_labels[f]))
            print ('Validation accuracy - %f' %svc.score(self.valid_data[f], self.valid_data_labels[f]))
            accuracy += svc.score(self.valid_data[f], self.valid_data_labels[f])

        cv_acc = 1.0*accuracy/self.folds
        print ('Cross validated accuracy - %f' %cv_acc)
        print ('-----------------------------')
        return cv_acc

    def logisticRegression(self, penalty='l2', max_iter=10, *kwargs):
        logReg = LogisticRegression(penalty=penalty, max_iter=max_iter)

        accuracy = 0
        print ('Learning using Logistic Regression')

        for f in range(self.folds):
            logReg.fit(self.train_data[f], self.train_data_labels[f])
            print ('Training accuracy - %f' % logReg.score(self.train_data[f], self.train_data_labels[f]))
            print ('Validation accuracy - %f' % logReg.score(self.valid_data[f], self.valid_data_labels[f]))
            accuracy += logReg.score(self.valid_data[f], self.valid_data_labels[f])

        cv_acc = 1.0 * accuracy / self.folds
        print ('Cross validated accuracy - %f' % cv_acc)
        print ('-----------------------------')

        return cv_acc

    def linearRegression(self, penalty='l2', max_iter=10, *kwargs):
        linReg = LinearRegression(penalty=penalty, max_iter=max_iter)

        accuracy = 0
        print ('Learning using Logistic Regression')

        for f in range(self.folds):
            linReg.fit(self.train_data[f], self.train_data_labels[f])
            print ('Training accuracy - %f' % linReg.score(self.train_data[f], self.train_data_labels[f]))
            print ('Validation accuracy - %f' % linReg.score(self.valid_data[f], self.valid_data_labels[f]))
            accuracy += linReg.score(self.valid_data[f], self.valid_data_labels[f])

        cv_acc = 1.0 * accuracy / self.folds
        print ('Cross validated accuracy - %f' % cv_acc)
        print ('-----------------------------')

        return cv_acc

    def randomForest(self, n_estimators=10, criterion='gini', random_state=42, *kwargs):
        randForest = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion,random_state=random_state)

        accuracy = 0
        print ('Learning using Random Forest')

        for f in range(self.folds):
            randForest.fit(self.train_data[f], self.train_data_labels[f])
            print ('Training accuracy - %f' % randForest.score(self.train_data[f], self.train_data_labels[f]))
            print ('Validation accuracy - %f' % randForest.score(self.valid_data[f], self.valid_data_labels[f]))
            accuracy += randForest.score(self.valid_data[f], self.valid_data_labels[f])

        cv_acc = 1.0 * accuracy / self.folds
        print ('Cross validated accuracy - %f' % cv_acc)
        print ('-----------------------------')

        return cv_acc


    def decisionTree(self, criterion='gini', random_state=42, *kwargs):
        decTree = DecisionTreeClassifier(criterion=criterion,random_state=random_state)

        accuracy = 0
        print ('Learning using Random Forest')

        for f in range(self.folds):
            decTree.fit(self.train_data[f], self.train_data_labels[f])
            print ('Training accuracy - %f' % decTree.score(self.train_data[f], self.train_data_labels[f]))
            print ('Validation accuracy - %f' % decTree.score(self.valid_data[f], self.valid_data_labels[f]))
            accuracy += decTree.score(self.valid_data[f], self.valid_data_labels[f])

        cv_acc = 1.0 * accuracy / self.folds
        print ('Cross validated accuracy - %f' % cv_acc)
        print ('-----------------------------')

        return cv_acc

