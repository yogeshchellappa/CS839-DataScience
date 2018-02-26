'''
1. Read all data
2. Prune it
3. Extract features
4. Run classifiers
'''
import sys
import pruning, features, classifiers
import numpy as np

def main():
    if len(sys.argv) > 2:
        filename_train = sys.argv[1]
        filename_test = sys.argv[2]
    else:
        filename_train = 'reviews_train.csv'
        filename_test = 'reviews_test.csv'

    # Call pruning rules
    prune_train = pruning.Prune(filename_train)
    prune_train.removeStopwords()
    prune_train.removePronouns()

    prune_test = pruning.Prune(filename_test)
    prune_test.removeStopwords()
    prune_test.removePronouns()

    # Generate features, labels
    feat_train = features.Features()
    feat_train.getAllFeatures(prune_train.data)
    train_lab = features.Labels()
    train_lab.extractLabels(prune_train.data)

    feat_test = features.Features()
    feat_test.getAllFeatures(prune_test.data)
    test_lab = features.Labels()
    test_lab.extractLabels(prune_test.data)

    # Split data
    num_train = len(feat_train.features.keys())
    num_test = len(feat_test.features.keys())
    num_features = 2 #Change this after more features are added


    features_train = np.zeros(shape = [num_train, num_features], dtype=np.float32)
    labels_train = np.zeros(shape = [num_train, 1], dtype=np.float32)

    features_test = np.zeros(shape=[num_test, num_features], dtype=np.float32)
    labels_test = np.zeros(shape=[num_test, 1], dtype=np.float32)

    i = 0
    all_terms = []

    for key, value in feat_train.iteritems():
        features_train[i] = value
        labels_train[i] = train_lab[key]
        all_terms.append(key)
        i += 1

    i = 0
    for key, value in feat_test.iteritems():
        features_test[i] = value
        labels_test[i] = test_lab[key]

        all_terms.append(key)

    data = classifiers.Data(features_train, labels_train, features_test, labels_test)

    # Train classifiers
    clf = classifiers.Classifiers(data)

    linRegAcc = clf.linearRegression()
    logRegAcc = clf.logisticRegression()
    svmAcc = clf.svm_classify()
    dtAcc = clf.decisionTree()
    rfAcc = clf.randomForest()

    print ('Linear regression accuracy - %f', linRegAcc)
    print ('Logistic regression accuracy - %f', logRegAcc)
    print ('SVM accuracy - %f', svmAcc)
    print ('Decision Tree accuracy - %f', dtAcc)
    print ('Random Forest accuracy - %f', rfAcc)

if __name__ == "__main__":
	main()






