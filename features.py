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
        print(df.keys())
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
        #tf = self.calculateTF(data)
        #idf = self.calculateIDF(tf)
        self.isCapitalized(data)

    def prefixSuffix(self, data, origData):
        pass
		
    def isCapitalized(self, data):
        data["isCapitalized"] = data['term'].str.contains('[A-Z]', regex=True)
		return data

    def extract_features(data, data_orig, path_adj, path_veg):
        '''
        Takes the complete dataframe and returns an array of features
        [prefix_food_desc, contains_veggie_or_fruit]
        '''

        doc_id = 'docID'
        term_id = 'term_id'
        term = 'term'

        p_doc_id, p_term = None, None
        prefix_food_desc, contains_veggie_or_fruit = [], []

        # read list of words describing food
        food_adj = pd.read_csv(path_adj)['words'].tolist()

        # read list of vegetable and fruit names
        veggie_and_fruit = pd.read_csv(path_veg)['words'].tolist()

        # iterate over each row in the dataframe
        for index, row in data.iterrows():
            # get index of current row in original dataframe
            orig_index = data_orig.index[(data_orig[doc_id] == row[doc_id]) & (data_orig[term_id] == row[term_id])][0]

            # get previous and next rows from original
            if orig_index > 0:
                print("index")
                print(orig_index)
                p_term = data_orig.iloc[[orig_index-1],:][term].values[0]
                p_doc_id = data_orig.iloc[[orig_index-1],:][doc_id].values[0]
            
            # if not the first word in the document and is contained in food adjectives list
            if p_doc_id and p_doc_id == row[doc_id] and p_term in food_adj:
                prefix_food_desc.append(1)
            else:
                prefix_food_desc.append(0)

            # if any sub-string of the word is a vegetable or fruit name
            contains_veggie_or_fruit.append(0)
            for s in getAllSubstrings(row[term]):
                if s in veggie_and_fruit:
                    contains_veggie_or_fruit.pop()
                    contains_veggie_or_fruit.append(1)
                    break

        data['hasDescriptivePrefix'] = prefix_food_desc
        data['hasIngredient'] = contains_veggie_or_fruit
        

    def getAllSubstrings(word):
        tok = word.strip().split(' ')
        if len(tok) == 1:
            return tok
        else:
            all_toks = list(tok)
            for i in range(len(tok)):
                for offset in range(2, len(tok)):
                    if i+offset > len(tok):
                        break
                    else:
                        all_toks.append(" ".join(tok[i:i+offset]))
                        all_toks.append(word)
                        return all_toks



'''
f = Features()
f.calculateTF('/Users/sukanya/PycharmProjects/cs839DataScience/reviews.csv')
#f.calculateIDF('/Users/sukanya/PycharmProjects/cs839DataScience/reviews.csv')
f.calculateTF('trainingdata_nostopwords_nopronouns_2.csv')
f.calculateIDF('trainingdata_nostopwords_nopronouns_2.csv')
'''

