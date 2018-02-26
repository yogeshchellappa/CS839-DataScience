'''
Pruning rules -
1. remove stopwords
'''
from stop_words import get_stop_words
import pandas as pd

class Prune(object):
    def __init__(self, filename):
        '''
        '''
        self.pronouns = set(["i", "you", "he", "she", "it", "we", "they", "what",
                         "who", "me", "him", "her", "it", "us", "you", "them",
                         "whom", "mine", "yours", "his", "hers", "ours", "theirs","shes",
                         "this", "that", "these", "those", "who", "whom", "which","ive",
                         "what", "whose", "whoever", "whatever", "whichever", "whomever",
                         "myself", "yourself", "himself", "herself", "itself", "ourselves",
                         "themselves", "each other", "one another", "anything", "everybody",
                         "another", "each", "few", "many", "none", "some", "all", "any",
                         "anybody", "anyone", "everyone", "everything", "no one", "nobody",
                         "nothing", "none", "other", "others", "several", "somebody", "someone",
                         "something", "most", "enough", "little", "more", "both", "either",
                         "neither", "one", "much", "such"])

        self.data = pd.read_csv(filename)
    
	
	def removeStopwords(self):
        stopwords = get_stop_words('en')
		stopwords = [i.replace("'","") for i in stopwords]
        
        todrop = []

        for term in self.data['term']:
            parts = term.split(" ")

            flag = False
            for p in parts:
                if p in stopwords:
                    flag = True
                    break
                else:
                    flag = False

            if flag:
                todrop.append(term)
        print len(todrop)
        print len(self.data)
        self.data = self.data[~self.data.term.isin(todrop)]
        print len(self.data)

        #data.to_csv('trainingdata_nostopwords.csv')

    def removePronouns(self):
        todrop = []

        for term in self.data['term']:
            parts = term.split(" ")

            flag = False
            for p in parts:
                if p in self.pronouns:
                    flag = True
                    break
                else:
                    flag = False

            if flag:
                todrop.append(term)
        print len(todrop)
        print len(self.data)
        self.data = self.data[~self.data.term.isin(todrop)]
        print len(self.data)

    def saveData(self):
        self.data.to_csv('trainingdata_nostopwords_nopronouns.csv')

p = Prune('reviews.csv')
p.removeStopwords()
p.removePronouns()
p.saveData()

