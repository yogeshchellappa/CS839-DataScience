import pandas as pd

file = pd.read_csv('/Users/sukanya/Downloads/yelp_review.csv')
file = file[200:301]
file.to_csv('/Users/sukanya/Downloads/yelp_review_shorter.csv')
