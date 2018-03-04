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
from imblearn.over_sampling import RandomOverSampler

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
        return row['position'] - len(row['term'].split(' ')) - window_size

    def pos_after(self, row, window_size):
        # Need to add support for window size > 1
        return row['position'] + 1 + window_size

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

        merged_all = pd.merge(left=merged_before, right=merged_after, on=['docID', 'term_x', 'position_x', 'label_x'], how='inner')

        merged_all.columns = ['docID', 'position', 'term', 'label', 'term_before', 'term_after']
        return merged_all

    def isCapitalized(self, data):
        data['isCapitalized'] = data['term'].str.contains('[A-Z]', regex=True)
        return data

    def attachDictFeatures(self, data_prune, data_orig, path_adj, path_veg):
        '''
        Takes the complete dataframe and returns an array of features
        [prefix_food_desc, contains_veggie_or_fruit]
        '''

        prefix_food_desc, suffix_food_desc, contains_veggie_or_fruit = [], [], []

        data_forpos = data_prune[['docID', 'position', 'term', 'label']]
        # join with original data to get positions
        data = self.getPosBeforeAfter(1, 1, data_forpos, data_orig)

        # read list of words describing food
        food_adj = set(line.strip() for line in open(path_adj))
        #food_adj = pd.read_csv(path_adj)['words'].tolist()

        # read list of vegetable and fruit names
        veggie_and_fruit = set(line.strip() for line in open(path_veg))
        #veggie_and_fruit = pd.read_csv(path_veg)['words'].tolist()

        # iterate over each row in the dataframe
        for index, row in data.iterrows():

            # get previous and next terms from the position data object
            p_term = row['term_before']
            n_term = row['term_after']

            # if term is contained in food adjectives list
            prefix_food_desc.append(1 if p_term and p_term in food_adj else 0)
            suffix_food_desc.append(1 if n_term and n_term in food_adj else 0)

            # if any sub-string of the word is a vegetable or fruit name
            contains_veggie_or_fruit.append(0)
            for s in row['term'].strip().split(' '): #self.getAllSubstrings(row['term']):
                if s.lower() in veggie_and_fruit:
                    contains_veggie_or_fruit.pop()
                    contains_veggie_or_fruit.append(1)
                    break

        data['hasDescriptivePrefix'] = prefix_food_desc
        data['hasDescriptiveSuffix'] = suffix_food_desc
        data['hasIngredient'] = contains_veggie_or_fruit

        return pd.merge(left=data_prune, right=data, left_on=['docID', 'position', 'term'], right_on=['docID', 'position', 'term'])

    def getAllSubstrings(self, word):
        tok = word.strip().split(' ')
        if len(tok) < 1:
            return []
        elif len(tok) == 1:
            return tok
        else:
            all_toks = list(tok)
            for s in range(len(tok)):
                for e in range(s + 2, len(tok) + 1):
                    all_toks.append(" ".join(tok[s:e]))
            return all_toks

    def getPrefixSuffixFeature(self, data, data_orig, prefixSuffixFile):
        reader = csv.reader(open(prefixSuffixFile), delimiter='\t')

        prefix_suffix = set()

        for row in reader:
            prefix_suffix.add((row[0], row[1]))

        data_pos = self.getPosBeforeAfter(0, 0, data, data_orig)
        data_pos['inPrefixSuffix'] = pd.Series(np.zeros(len(data_pos)), index=data_pos.index)

        for index, row in data_pos.iterrows():
            if (row['term_before'], row['term_after']) in prefix_suffix:
                data_pos.loc[index, 'inPrefixSuffix'] = 1.0
            else:
                data_pos.loc[index, 'inPrefixSuffix'] = 0.0

        return data_pos

    def getAllFeatures(self, data, data_orig, prefixsuffixFile, path_adj, path_veg, saveTo, withRos, readFrom):
        '''
        :param data: pandas data frame
        :return: None
        Calculates all the features of the data
        '''

        if readFrom:
            data_final = pd.read_csv(readFrom)
        else:
            feat_list = ['inPrefixSuffix', 'tf', 'idf', 'isCapitalized', 'hasDescriptivePrefix', 'hasDescriptiveSuffix', 'hasIngredient']

            data_prefsuff = self.getPrefixSuffixFeature(data, data_orig, prefixsuffixFile)
            data_tf = self.calculateTF(data_prefsuff)
            data_idf = self.calculateIDF(data_tf)
            data_cap = self.isCapitalized(data_idf)
            data_final = self.attachDictFeatures(data_cap, data_orig, path_adj, path_veg)

            data_final = data_final.drop(columns=['label_y', 'term_before_y', 'term_after_y'])
            data_final = data_final.drop_duplicates()
            data_final.to_csv(saveTo, index=False)

        if withRos:
            ros = RandomOverSampler(random_state=42)
            self.features, self.labels = ros.fit_sample(data_final[feat_list], data_final[data_final.columns[3]])
            self.data_all = data_final.as_matrix()
        else:
            self.features = data_final.as_matrix(columns=['inPrefixSuffix', 'tf', 'idf', 'isCapitalized', 'hasDescriptivePrefix', 'hasDescriptiveSuffix', 'hasIngredient'])
            self.labels = data_final.as_matrix(columns=['label_x'])
            self.data_all = data_final.as_matrix()

