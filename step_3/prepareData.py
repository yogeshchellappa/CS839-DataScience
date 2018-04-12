'''
Make sure missing values are ''
Add ids to both the tables
'''

table1 = '../step_2/DATA/source1.csv'
table2 = '../step_2/DATA/source2.csv'

import pandas as pd
import numpy as np

def main():
    source_1 = pd.read_csv(table1)
    source_2 = pd.read_csv(table2)

    # Make all missing values nan
    source_1.replace("unknown", np.nan, inplace=True)
    source_1.replace(-1, np.nan, inplace=True)
    source_1.replace("0-0-0", np.nan, inplace=True)

    source_2.replace("unknown", np.nan, inplace=True)
    source_2.replace(-1, np.nan, inplace=True)
    source_2.replace("0-0-0", np.nan, inplace=True)

    # Print stats about missing values
    print ('Source 1 missing values per column')
    print (source_1.isnull().sum())
    print ('---------')
    print ('Source 2 missing values per column')
    print (source_2.isnull().sum())
    print ('---------')

    # Add indices
    source_1.insert(0, 'ID', range(0, len(source_1)))
    source_2.insert(0, 'ID', range(0, len(source_2)))

    # Save the cleaned files
    source_1.to_csv('source1_cleaned.csv', index=False)
    source_2.to_csv('source2_cleaned.csv', index=False)

def getNonOverlaps():
    source_1 = pd.read_csv('source1_cleaned.csv')
    source_2 = pd.read_csv('source2_cleaned.csv')

    source_1['Name'] = source_1.apply(lambda row : row['Name'].lower() if row['Name'] != np.nan else row['Name'], axis=1)
    source_2['Name'] = source_2.apply(lambda row: row['Name'].lower() if row['Name'] != np.nan else row['Name'], axis=1)

    joined = pd.merge(left=source_1, right=source_2, on=['Name'], how='inner')

    print ('Number of unique books in common')
    print (len(set(joined.ID_x)), len(set(joined.ID_y)))

    with open('nonoverlap_source1.txt', 'w+') as f:
        f.write(str(list(set(source_1.ID) - set(joined.ID_x))))

    with open('nonoverlap_source2.txt', 'w+') as f:
        f.write(str(list(set(source_2.ID) - set(joined.ID_y))))

if __name__ == "__main__":
    main()
    getNonOverlaps()