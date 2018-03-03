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
import post_processing

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
    feat_train.getAllFeatures(prune_train.data, data_orig, 'prefix_suffix.csv', 'food_adj.txt', 'food_veggie.txt', saveTo='features_train.csv', withRos=False, readFrom='features_train.csv')

    feat_test = features.Features()
    feat_test.getAllFeatures(prune_test.data, data_test_orig, 'prefix_suffix.csv', 'food_adj.txt', 'food_veggie.txt', saveTo='features_test.csv', withRos=False, readFrom='features_test.csv')

    # Split data
    data = classifiers.Data(feat_train.data_all, feat_train.features, feat_train.labels, feat_test.data_all, feat_test.features, feat_test.labels)

    # Train classifiers
    clf = classifiers.Classifiers(data)

    dtAcc = clf.decisionTree()
    linRegAcc = clf.linearRegression()
    logRegAcc = clf.logisticRegression()
    svmAcc = clf.svm_classify()
    rfAcc = clf.randomForest()
    gradB = clf.gradientBoostingClassifier()

    print ('Linear regression accuracy - %f', linRegAcc)
    print ('Logistic regression accuracy - %f', logRegAcc)
    print ('SVM accuracy - %f', svmAcc)
    print ('Decision Tree accuracy - %f', dtAcc)
    print ('Random Forest accuracy - %f', rfAcc)
    print ('Gradient Boosting accuracy - %f', gradB)

    # Postprocessing -
    print ('Validation results from Decision Tree')
    post = post_processing.PostProcessing()
    post.takeLongest('output.csv', 'pruned_train.csv')

    print ('----------')
    print ('Test results from Decision Tree')
    post.takeLongest('output_test.csv', 'pruned_test.csv')
    print('----------')

if __name__ == "__main__":
    main()




