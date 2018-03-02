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
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_recall_fscore_support
import numpy as np

class Data(object):
    def __init__(self, train_features, train_labels, test_features, test_labels):
        self.train_data = []
        self.train_data_labels = []
        self.valid_data = []
        self.valid_data_labels = []

        self.test_data = test_features
        self.test_data_labels = test_labels

        stratifiedsplit = StratifiedShuffleSplit(n_splits=5, test_size=0.20, random_state=42)

        for train_index, valid_index in stratifiedsplit.split(train_features, train_labels):
            self.train_data.append(train_features[train_index])
            self.train_data_labels.append(train_labels[train_index])
            self.valid_data.append(train_features[valid_index])
            self.valid_data_labels.append(train_labels[valid_index])


class Classifiers(object):
    def __init__(self, data):
        self.train_data = data.train_data
        self.train_data_labels = data.train_data_labels
        self.valid_data = data.valid_data
        self.valid_data_labels = data.valid_data_labels
        self.test_data = data.test_data
        self.test_data_labels = data.test_data_labels
        self.folds = 5

    def print_report(self, scores):
        print ('Classification report - ')
        print (' Precision Recall f1-score support')

        prec_f = prec_nf = rec_f = rec_nf = f1_f = f1_nf = num_f = num_nf = 0

        for score in scores:
            prec_nf += score[0][0]
            prec_f += score[0][1]

            rec_nf += score[1][0]
            rec_f += score[1][1]

            f1_nf += score[2][0]
            f1_f += score[2][1]

            num_nf += score[3][0]
            num_f += score[3][1]

        print (' Not Food - %f %f %f %f' %(prec_nf*1.0/5, rec_nf*1.0/5, f1_nf*1.0/5, num_nf*1.0/5))
        print (' Food - %f %f %f %f' % (prec_f * 1.0 / 5, rec_f * 1.0 / 5, f1_f * 1.0 / 5, num_f * 1.0 / 5))

    def print_confusion_matrix(self, true, pred):
        array = np.zeros(shape=[4, 2, 2], dtype=np.float)
        matrix = np.zeros(shape=[2,2], dtype=np.float)

        for i in range(len(true)):
            true[i] = (true[i]).astype(bool)
            array[i:,:,:] = sklearn.metrics.confusion_matrix(true[i], pred[i])

        for i in range(2):
            for j in range(2):
                matrix[i][j] = np.mean(array[:,i,j])

        print (matrix)


    def svm_classify(self, kernel='linear', max_iter=10, *kwargs):
        svc = SVC(kernel=kernel, max_iter=max_iter)

        accuracy = 0
        scores = []
        pred = []

        print ('Learning using SVM')
        for f in range(self.folds):
            svc.fit(self.train_data[f], self.train_data_labels[f])

            valid_acc = svc.score(self.valid_data[f], self.valid_data_labels[f])
            valid_pred = svc.predict(self.valid_data[f])

            pred.append(valid_pred)
            scores.append(precision_recall_fscore_support(self.valid_data_labels[f], valid_pred))

            accuracy += valid_acc

        self.print_report(scores)
        self.print_confusion_matrix(pred, self.valid_data_labels)
        cv_acc = 1.0*accuracy/self.folds

        print ('Cross validated accuracy - %f' %cv_acc)
        print ('-----------------------------')
        return cv_acc

    def logisticRegression(self, penalty='l2', max_iter=10, *kwargs):
        logReg = LogisticRegression(penalty=penalty, max_iter=max_iter, class_weight='balanced')

        accuracy = 0
        scores = []
        pred = []

        print ('Learning using Logistic Regression')

        for f in range(self.folds):
            logReg.fit(self.train_data[f], self.train_data_labels[f])
            valid_acc = logReg.score(self.valid_data[f], self.valid_data_labels[f])
            valid_pred = logReg.predict(self.valid_data[f])
            pred.append(valid_pred)
            scores.append(precision_recall_fscore_support(self.valid_data_labels[f], valid_pred))

            accuracy += valid_acc

        self.print_report(scores)
        self.print_confusion_matrix(pred, self.valid_data_labels)
        cv_acc = 1.0 * accuracy / self.folds
        print ('Cross validated accuracy - %f' % cv_acc)
        print ('-----------------------------')

        return cv_acc

    def linearRegression(self, *kwargs):
        linReg = LinearRegression()

        accuracy = 0
        scores = []
        pred = []

        print ('Learning using Linear Regression')

        for f in range(self.folds):
            linReg.fit(self.train_data[f], self.train_data_labels[f])
            valid_acc = linReg.score(self.valid_data[f], self.valid_data_labels[f])
            valid_pred = linReg.predict(self.valid_data[f])

            pred.append(valid_pred)
            valid_pred = (valid_pred>0.5).astype(int)
            scores.append(precision_recall_fscore_support(self.valid_data_labels[f], valid_pred))

            accuracy += valid_acc

        self.print_report(scores)
        self.print_confusion_matrix(pred, self.valid_data_labels)
        cv_acc = 1.0 * accuracy / self.folds
        print ('Cross validated accuracy - %f' % cv_acc)
        print ('-----------------------------')

        return cv_acc

    def randomForest(self, n_estimators=10, criterion='gini', random_state=42, *kwargs):
        randForest = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion,
                                            random_state=random_state, class_weight='balanced')

        accuracy = 0
        scores = []
        pred = []

        print ('Learning using Random Forest')

        for f in range(self.folds):
            randForest.fit(self.train_data[f], self.train_data_labels[f])
            valid_acc = randForest.score(self.valid_data[f], self.valid_data_labels[f])
            valid_pred = randForest.predict(self.valid_data[f])

            pred.append(valid_pred)
            scores.append(precision_recall_fscore_support(self.valid_data_labels[f], valid_pred))

            accuracy += valid_acc

        self.print_report(scores)
        self.print_confusion_matrix(pred, self.valid_data_labels)
        print('Feature importance (higher => more important')
        print(randForest.feature_importances_)
        cv_acc = 1.0 * accuracy / self.folds
        print ('Cross validated accuracy - %f' % cv_acc)
        print ('-----------------------------')

        return cv_acc


    def decisionTree(self, criterion='gini', random_state=42, *kwargs):
        decTree = DecisionTreeClassifier(criterion=criterion,random_state=random_state,
                                         class_weight='balanced')

        accuracy = 0
        scores = []
        pred = []

        print ('Learning using Decision Tree')

        for f in range(self.folds):
            decTree.fit(self.train_data[f], self.train_data_labels[f])
            valid_acc = decTree.score(self.valid_data[f], self.valid_data_labels[f])
            valid_pred = decTree.predict(self.valid_data[f])

            pred.append(valid_pred)
            scores.append(precision_recall_fscore_support(self.valid_data_labels[f], valid_pred))

            accuracy += valid_acc

        self.print_report(scores)
        self.print_confusion_matrix(pred, self.valid_data_labels)
		
        test_pred = decTree.predict(self.test_data)
        print("TEST DATA")
        print(precision_recall_fscore_support(self.test_data_labels, test_pred))
        print("END OF TESTING")

        print ('Feature importance (higher => more important')
        print (decTree.feature_importances_)
        cv_acc = 1.0 * accuracy / self.folds
        print ('Cross validated accuracy - %f' % cv_acc)
        print ('-----------------------------')

        return cv_acc

    def gradientBoostingClassifier(self, n_estimators=100, *kwargs):
        gradBoostingClf = GradientBoostingClassifier(n_estimators=n_estimators)

        accuracy = 0
        scores = []
        pred = []

        print ('Learning using Gradient Boosting')

        for f in range(self.folds):
            gradBoostingClf.fit(self.train_data[f], self.train_data_labels[f])
            valid_acc = gradBoostingClf.score(self.valid_data[f], self.valid_data_labels[f])
            valid_pred = gradBoostingClf.predict(self.valid_data[f])

            pred.append(valid_pred)
            scores.append(precision_recall_fscore_support(self.valid_data_labels[f], valid_pred))

            accuracy += valid_acc

        self.print_report(scores)
        self.print_confusion_matrix(pred, self.valid_data_labels)
        cv_acc = 1.0 * accuracy / self.folds
        print ('Cross validated accuracy - %f' % cv_acc)
        print ('-----------------------------')

        return cv_acc