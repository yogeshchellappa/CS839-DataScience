'''
Generates the following features -
1. TF
2. TF-IDF
...
'''

import pandas as pd
import json
import csv
import numpy as np

class Labels(object):
    def __init__(self):
        # Labels dict has - (term, label) pairs
        self.labels = {}

class Features(object):
    def __init__(self):
        ''''''
        # Features as - 1. tf 2. idf ...

    def calculateTF(self, data):
        '''
        Calculates tf for all words in the file
        :return: tf vector for all words as well as stores it in self.tf
        Feel free to change this as you see fit!
        '''

        grouped_data = data[['docID', 'term', 'label']]
        grouped_data = grouped_data.groupby(['docID', 'term'], as_index=False)['label'].count()
        grouped_data.columns = ['docID', 'term', 'tf']
        merged = pd.merge(left=data, right=grouped_data, on=['docID', 'term'], how='inner')
        return merged

    def calculateIDF(self, data):
        '''
        Calculates idf for all the words in the file
        :param filename:
        :return: idf dict for all words. stores them as well
        '''
        select_data = data[['term', 'docID']]
        df = select_data.groupby(['term'], as_index=False)['docID'].count()
        df['docID'] = 1.0/df['docID']
        df.columns = ['term', 'idf']

        merged = pd.merge(left=data, right=df, on=['term'], how='inner')
        return merged

    def pos_before(self, row, window_size):
        # Need to add support for window size > 1
        return row['position'] - len(row['term'].split(' '))

    def pos_after(self, row, window_size):
        # Need to add support for window size > 1
        return row['position'] + 1

    def getPosBeforeAfter(self, win_size_before, win_size_after, data, data_orig):

        data['pos_before'] = pd.Series(np.random.randn(len(data)), index=data.index)
        data['pos_after'] = pd.Series(np.random.randn(len(data)), index=data.index)

        data['pos_before'] = data.apply(lambda row: self.pos_before(row, win_size_before), axis=1)
        data['pos_after'] = data.apply(lambda row: self.pos_after(row, win_size_after), axis=1)

        data_single = data_orig[data_orig['term'].apply(lambda x: len(x.split(' ')) == 1)]

        merged_before = pd.merge(left=data, right=data_single, left_on=['docID', 'pos_before'],
                                 right_on=['docID', 'position'], how='inner')
        merged_before = merged_before.drop(
            columns=['pos_before', 'pos_after', 'position_y', 'label_y'])

        merged_after = pd.merge(left=data, right=data_single, left_on=['docID', 'pos_after'],
                                right_on=['docID', 'position'], how='inner')
        merged_after = merged_after.drop(
            columns=['pos_before', 'pos_after', 'position_y', 'label_y'])

        merged_all = pd.merge(left=merged_before, right=merged_after, on=['docID', 'term_x', 'position_x'], how='inner')
        merged_all = merged_all.drop(columns=['label_x_y'])

        merged_all.columns = ['docID', 'position', 'term', 'label', 'term_before', 'term_after']
        return merged_all

    def isCapitalized(self, data):
        data['isCapitalized'] = data['term'].str.contains('[A-Z]', regex=True)
        return data

    def extract_features(self, data, data_orig, path_adj, path_veg):
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
            for s in self.getAllSubstrings(row[term]):
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


    def getPrefixSuffixFeature(self, data, data_orig, prefixSuffixFile):
        reader = csv.reader(open(prefixSuffixFile), delimiter='\t')

        prefix_suffix = set()

        for row in reader:
            prefix_suffix.add((row[0], row[1]))

        data_pos = self.getPosBeforeAfter(1, 1, data, data_orig)
        data_pos['inPrefixSuffix'] = pd.Series(np.zeros(len(data_pos)), index=data_pos.index)

        for index, row in data_pos.iterrows():
            if (row['term_before'], row['term_after']) in prefix_suffix:
                data_pos.loc[index, 'inPrefixSuffix'] = 1.0
            else:
                data_pos.loc[index, 'inPrefixSuffix'] = 0.0

        return data_pos

    def getAllFeatures(self, data, data_orig, prefixsuffixFile, saveTo):
        '''
        :param data: pandas data frame
        :return: None
        Calculates all the features of the data
        '''
        data_prefsuff = self.getPrefixSuffixFeature(data, data_orig, prefixsuffixFile)
        data_tf = self.calculateTF(data_prefsuff)
        data_idf = self.calculateIDF(data_tf)
        data_cap = self.isCapitalized(data_idf)
        print (data_cap.keys())

        data_cap.to_csv(saveTo)
        self.features = data_cap.as_matrix(columns=['inPrefixSuffix', 'tf', 'idf', 'isCapitalized'])
        self.labels = data_cap.as_matrix(columns=['label'])
