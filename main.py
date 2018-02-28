'''
1. Read all data
2. Prune it
3. Extract features
4. Run classifiers
'''
import sys
import pruning, features, classifiers
import numpy as np
import matplotlib
import pandas as pd

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def main():
    if len(sys.argv) > 2:
        filename_train = sys.argv[1]
        filename_test = sys.argv[2]
    else:
        filename_train = 'reviews_train.csv'
        filename_test = 'reviews_test.csv'

    data_orig = pd.read_csv(filename_train)
    data_test_orig = pd.read_csv(filename_test)

    # Call pruning rules
    prune_train = pruning.Prune(filename_train)
    prune_train.removeStopwords()
    prune_train.removePronouns()

    prune_test = pruning.Prune(filename_test)
    prune_test.removeStopwords()
    prune_test.removePronouns()

    # Generate features, labels
    feat_train = features.Features()
    feat_train.getAllFeatures(prune_train.data, data_orig, 'prefix_suffix.csv', saveTo='features_train.csv')

    feat_test = features.Features()
    feat_test.getAllFeatures(prune_test.data, data_test_orig, 'prefix_suffix.csv', saveTo='features_test.csv')

    # Split data

    data = classifiers.Data(feat_train.features, feat_train.labels, feat_test.features, feat_test.labels)

    # Train classifiers
    clf = classifiers.Classifiers(data)

    #linRegAcc = clf.linearRegression()
    logRegAcc = clf.logisticRegression()
    svmAcc = clf.svm_classify()
    dtAcc = clf.decisionTree()
    rfAcc = clf.randomForest()
    gradB = clf.gradientBoostingClassifier()
    xgb = clf.xgbClassifier()	

    #print ('Linear regression accuracy - %f', linRegAcc)
    print ('Logistic regression accuracy - %f', logRegAcc)
    print ('SVM accuracy - %f', svmAcc)
    print ('Decision Tree accuracy - %f', dtAcc)
    print ('Random Forest accuracy - %f', rfAcc)
    print ('Gradient Boosting accuracy - %f', gradB)
    print ('XGBoost accuracy - %f', xgb)

if __name__ == "__main__":
    main()




