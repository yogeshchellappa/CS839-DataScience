import pandas as pd

file = pd.read_csv('/Users/sukanya/Downloads/yelp_review.csv')
file = file[500:601]
file.to_csv('/Users/sukanya/Downloads/yelp_review_shorter_2.csv')
