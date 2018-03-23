'''
Convert json file to csv
'''

import pandas as pd

def main():
    filename = 'goodreads-fantasy-adv.json'
    data = pd.read_json(filename)

    print (data.keys())
    data.to_csv('goodreadsCleaned.csv', index=False)

if __name__ == "__main__":
    main()