'''
Pruning rules -
1. remove stopwords
'''
from stop_words import get_stop_words
import pandas as pd

class Prune(object):
    def __init__(self):
        ''''''

    def removeStopwords(self, filename):
        stopwords = get_stop_words('en')

        data = pd.read_csv(filename)
        todrop = []

        for term in data['term']:
            parts = term.split(" ")

            flag = False
            for p in parts:
                if p in stopwords:
                    flag = True

                else:
                    flag = False
                    break

            if flag:
                todrop.append(term)
        print len(todrop)
        print len(data)
        data = data[~data.term.isin(todrop)]
        print len(data)
        #data[data.term not in todrop]

        data.to_csv('trainingdata_nostopwords.csv')

p = Prune()
p.removeStopwords('/Users/sukanya/PycharmProjects/cs839DataScience/reviews.csv')


