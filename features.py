'''
Generates the following features -
1. TF
2. TF-IDF
...
'''

import pandas as pd
import json
class Labels(object):
    def __init__(self):
        # Labels dict has - (term, label) pairs
        self.labels = {}

    def extractLabels(self, data):
        for index, row in data.iterrows():
            if row['term'] in self.labels:
                if row['label'] != self.labels[row['term']]:
                    if row['label'] == True:
                        self.labels[row['term']] = True
            else:
                self.labels[row['term']] = row['label']

class Features(object):
    def __init__(self):
        # Features as - 1. tf 2. idf ...
        self.features = {}

    def calculateTF(self, data):
        '''
        Calculates tf for all words in the file
        :return: tf vector for all words as well as stores it in self.tf
        Feel free to change this as you see fit!
        '''

        #data = pd.read_csv(filename)
        data = data.groupby(['docID', 'term'], as_index=False).count()
        data = data.groupby(['term'], as_index=False).mean()
        tf = dict(zip(data['term'], data['position']))

        for key, value in tf.iteritems():
            self.features[key] = [value]

        label_c = data.groupby(['label', 'term'], as_index=False).count()
        print label_c
        label_c = label_c.groupby(['label']).count()
        print label_c
        print len(tf.keys())

    def calculateIDF(self, data):
        '''
        Calculates idf for all the words in the file
        :param filename:
        :return: idf dict for all words. stores them as well
        '''
        df = data.groupby(['term'], as_index=False)['docID'].count()

        df['docID'] = 1.0/df['docID']
        idf = dict(zip(df['term'], df['docID']))

        for key, value in idf.iteritems():
            if key not in self.features:
                print ('Error, key ' + key + ' not found')
            else:
                self.features[key].append(value)

        print len(idf.keys())

    def getAllFeatures(self, data):
        '''
        :param data: pandas data frame
        :return: None
        Calculates all the features of the data
        '''
        self.calculateTF(data)
        self.calculateIDF(data)

'''
f = Features()
f.calculateTF('/Users/sukanya/PycharmProjects/cs839DataScience/reviews.csv')
#f.calculateIDF('/Users/sukanya/PycharmProjects/cs839DataScience/reviews.csv')
f.calculateTF('trainingdata_nostopwords_nopronouns_2.csv')
f.calculateIDF('trainingdata_nostopwords_nopronouns_2.csv')
'''

