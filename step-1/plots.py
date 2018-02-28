'''
Plotting the words distribution before and after marked up words
'''

import pandas as pd
import matplotlib
import csv

matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


data = pd.read_csv('reviews_wp.csv')
pos_positions_before = set()
pos_positions_after = set()
'''
pos_terms = set()
for index, row in data.iterrows():
    if row['label'] == True:
        pos_terms.add(row['term'])

print len(pos_terms)
for index, row in data.iterrows():
    if row['term'] in pos_terms:
        row['label'] = True

data.to_csv('reviews_wp_labelcorrected.csv')
'''
for index, row in data.iterrows():
    if row['label'] == True:

        pos_positions_after.add((row['docID'], row['position']+1))
        pos_positions_before.add((row['docID'], row['position']-len(row['term'].split(' '))))
        
print pos_positions_before, pos_positions_after
window_size_before = 1
window_size_after = 1
words_after = {}
words_before = {}

for index, row in data.iterrows():
    for i in range(window_size_before):
        if len(row['term'].split(' ')) == 1 and (row['docID'], row['position']+i) in pos_positions_before:
            if row['term'] in words_before:
                words_before[row['term']] += 1
            else:
                words_before[row['term']] = 1

    for i in range(window_size_after):
        if len(row['term'].split(' ')) == 1 and (row['docID'], row['position']-i) in pos_positions_after:
            if row['term'] in words_after:
                words_after[row['term']] += 1
            else:
                words_after[row['term']] = 1

print words_after, words_before
print ('Number of words before - %d' %len(words_before.keys()))
print ('Number of words after - %d' %len(words_after.keys()))

with open('words_before_1.csv', 'w+') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in words_before.items():
       writer.writerow([key, value])

with open('words_after_1.csv', 'w+') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in words_after.items():
       writer.writerow([key, value])


# Reading back the above saved stuff
window_size_before = 1
window_size_after = 1
words_after_neg = {}
words_before_neg = {}

with open('words_before_1.csv', 'rb') as csv_file:
    reader = csv.reader(csv_file)
    words_before = dict(reader)

with open('words_after_1.csv', 'rb') as csv_file:
    reader = csv.reader(csv_file)
    words_after = dict(reader)

pos_before_negative = set()
pos_after_negative = set()

for index, row in data.iterrows():
    if row['label'] == False:
        pos_after_negative.add((row['docID'], row['position'] + 1))
        pos_before_negative.add((row['docID'], row['position'] - len(row['term'].split(' '))))

for index, row in data.iterrows():
    for i in range(window_size_before):
        if len(row['term'].split(' ')) == 1 and row['term'] in words_before and (row['docID'], row['position']+i) in pos_before_negative:
            if row['term'] in words_before_neg:
                words_before_neg[row['term']] += 1
            else:
                words_before_neg[row['term']] = 1

    for i in range(window_size_after):

        if len(row['term'].split(' ')) == 1 and row['term'] in words_after and (row['docID'], row['position']-i) in pos_after_negative:
            if row['term'] in words_after_neg:
                words_after_neg[row['term']] += 1
            else:
                words_after_neg[row['term']] = 1

with open('words_before_neg_1.csv', 'w+') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in words_before_neg.items():
       writer.writerow([key, value])

with open('words_after_neg_1.csv', 'wb') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in words_after_neg.items():
       writer.writerow([key, value])
