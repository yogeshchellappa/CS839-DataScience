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

if __name__ == "__main__":
    main()