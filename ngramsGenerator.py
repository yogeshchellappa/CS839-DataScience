import json
import re
import csv
import sys
from collections import defaultdict

def getStartIndicesOfAllWordsInText(text):
    output = defaultdict()
    uniqueWords = list(set(text.split(" ")))
    for i in uniqueWords:
        if len(i) == 0:
            continue
        output[i] = [j.start() for j in list(re.finditer(i, text))]
    return output
	
def generateNGrams(reviewRecord, n):
    ngramList = []

    docId = reviewRecord['id']
    review = reviewRecord['review']
    foodItems = set(reviewRecord['foodItems'])
    
    wordPositions = getStartIndicesOfAllWordsInText(review)
    
    splitReview = review.split(' ')
    
    if n == 1:
        for i in range(len(splitReview)):
            if len(splitReview[i]):
                ngramList.append([docId, wordPositions[splitReview[i]].pop(0), splitReview[i], splitReview[i] in foodItems])
    elif n == 2:
        for i in range(len(splitReview)-1):
            if len(splitReview[i]) and len(splitReview[i+1]):
                combined = splitReview[i] + " " + splitReview[i+1]
                ngramList.append([docId, wordPositions[splitReview[i+1]].pop(0), combined, combined in foodItems])
    elif n == 3:
        for i in range(len(splitReview)-2):
            if len(splitReview[i]) and len(splitReview[i+1]) and len(splitReview[i+2]):
                combined = splitReview[i] + " " + splitReview[i+1] + " " + splitReview[i+2]
                ngramList.append([docId, wordPositions[splitReview[i+2]].pop(0), combined, combined in foodItems])
    
    return ngramList
	
	
def main(reviewsJsonPath):
	jsonData = json.load(open(reviewsJsonPath))
	trainingData = []
	
	for i in [1,2,3]:
		for j in jsonData:
			trainingData += generateNGrams(j, i)

	# Write to CSV file
	with open("reviews.csv", "w", newline="") as f:
		writer = csv.writer(f)
		writer.writerows(trainingData)
	
	print("Written to reviews.csv")
	
if len(sys.argv) < 2:
	print("Usage:\npython nGramsGenerator <Path to reviews.json file>")
	sys.exit(0)
else:
	main(sys.argv[1])
	