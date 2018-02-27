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

        grouped_data = data.groupby(['docID', 'term'], as_index=False).count()
        grouped_data = grouped_data.drop(columns = 'label')
        grouped_data.columns = ['docID', 'term', 'tf']
        merged = pd.merge(left=data, right=grouped_data, on=['docID', 'term'], how='inner')
        return merged

    def calculateIDF(self, data):
        '''
        Calculates idf for all the words in the file
        :param filename:
        :return: idf dict for all words. stores them as well
        '''
        df = data.groupby(['term'], as_index=False)['docID'].count()
        print df.keys()
        df['docID'] = 1.0/df['docID']
        df.columns = ['term', 'idf']

        merged = pd.merge(left=data, right=df, on=['term'], how='inner')
        return merged

    def getAllFeatures(self, data):
        '''
        :param data: pandas data frame
        :return: None
        Calculates all the features of the data
        '''
        tf = self.calculateTF(data)
        idf = self.calculateIDF(tf)

    def prefixSuffix(self, data, origData):




'''
f = Features()
f.calculateTF('/Users/sukanya/PycharmProjects/cs839DataScience/reviews.csv')
#f.calculateIDF('/Users/sukanya/PycharmProjects/cs839DataScience/reviews.csv')
f.calculateTF('trainingdata_nostopwords_nopronouns_2.csv')
f.calculateIDF('trainingdata_nostopwords_nopronouns_2.csv')
'''

