'''
Generates the following features -
1. TF
2. TF-IDF
...
'''

import pandas as pd
import json

class Features(object):
    def __init__(self):
        self.tf = {}
        self.idf = {}


    def gettf(self, word):
        if word in self.tf:
            return self.tf[word]
        else:
            print ('Error: word not found')

    def gettfidf(self, word):
        if word in self.idf:
            return self.idf[word]
        else:
            print ('Error: word not found')

    def calculateTF(self, filename):
        '''
        Calculates tf for all words in the file
        :return: tf vector for all words as well as stores it in self.tf
        Feel free to change this as you see fit!
        '''

        data = pd.read_csv(filename)
        tf = data.groupby(['docID', 'term'], as_index=False).count()
        tf = tf.groupby(['term'], as_index=False).mean()
        self.tf = dict(zip(tf['term'], tf['position']))
        label_c = data.groupby(['label', 'term'], as_index=False).count()
        print label_c
        label_c = label_c.groupby(['label']).count()
        print label_c
        print len(self.tf.keys())
        return self.tf

    def calculateIDF(self, filename):
        '''
        Calculates idf for all the words in the file
        :param filename:
        :return: idf dict for all words. stores them as well
        '''
        data = pd.read_csv(filename)
        df = data.groupby(['term'], as_index=False)['docID'].count()

        df['docID'] = 1.0/df['docID']
        self.idf = dict(zip(df['term'], df['docID']))

        print len(self.idf.keys())
        return self.idf



f = Features()
f.calculateTF('/Users/sukanya/PycharmProjects/cs839DataScience/reviews.csv')
#f.calculateIDF('/Users/sukanya/PycharmProjects/cs839DataScience/reviews.csv')
f.calculateTF('trainingdata_nostopwords_nopronouns.csv')
f.calculateIDF('trainingdata_nostopwords_nopronouns.csv')

