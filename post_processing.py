'''
Applying post processing rule -
1. Take the longest predicted string
'''
import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics import precision_recall_fscore_support

class PostProcessing(object):
    def print_confusion_matrix(self, true, pred):
        array = np.zeros(shape=[4, 2, 2], dtype=np.float)
        matrix = np.zeros(shape=[2,2], dtype=np.float)

        for i in range(len(true)):
            true[i] = (true[i]).astype(bool)
            array[i:,:,:] = sklearn.metrics.confusion_matrix(true[i], pred[i])

        for i in range(2):
            for j in range(2):
                matrix[i][j] = np.mean(array[:,i,j])

        print (matrix)

    def takeLongest(self, all_data):
        blacklist = set(line.strip() for line in open('blacklist.txt'))

        print(precision_recall_fscore_support(all_data['label_x'], all_data['pred_label']))
        all_data.sort_values(by=['docID', 'position', 'term'], axis=0, ascending=True, inplace=True)
        all_data = all_data.reset_index(drop=True)
        for index, row in all_data.iterrows():
            #print (row['label_x'], row['true=pred'])
            if 'food' in row['term'].lower() or 'drinks' in row['term'].lower() \
                    or 'foods' in row['term'].lower() or row['term'].lower() in blacklist\
                    or 'and' in row['term'].lower().strip().split(' ')[-1] or 'and' in row['term'].lower().strip().split(' ')[0]:
                all_data.loc[index, 'pred_label'] = False
                all_data.loc[index, 'true=pred'] = all_data.loc[index, 'pred_label'] == all_data.loc[index, 'label_x']
            if row['true=pred'] and row['label_x']:
                words = set(row['term'].strip().split(' '))
                for i in range(1, 10):
                    if index-i < 0:
                        break
                    prev = all_data.loc[index-i, :]
                    if prev['docID'] != row['docID']:
                        break
                    prevwords = set(prev['term'].strip().split(' '))
                    if not prev['true=pred'] and words.intersection(prevwords):
                        all_data.loc[index-i, 'pred_label'] = False
                        all_data.loc[index - i, 'true=pred'] = all_data.loc[index-i, 'pred_label'] == all_data.loc[index-i, 'label_x']

                for i in range(1, 10):
                    if index+i >= len(all_data):
                        break
                    prev = all_data.loc[index + i, :]
                    if prev['docID'] != row['docID']:
                        break
                    prevwords = set(prev['term'].strip().split(' '))
                    if not prev['true=pred'] and words.intersection(prevwords):
                        all_data.loc[index + i, 'pred_label'] = False
                        all_data.loc[index + i, 'true=pred'] = all_data.loc[index + i, 'pred_label'] == all_data.loc[
                            index + i, 'label_x']




        all_data.to_csv('post_pruned.csv')
        print (precision_recall_fscore_support(all_data['actual_label'], all_data['pred_label']))
        #self.print_confusion_matrix(all_data['label_x'], all_data['pred_label'])

post = PostProcessing()
data = pd.read_csv('output.csv')
post.takeLongest(data)
