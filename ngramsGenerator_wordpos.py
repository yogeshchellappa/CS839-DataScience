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

    docId = str(reviewRecord['id'])
    if len(docId) > 2 and docId[0] == '0':
        docId = "1" + docId
    docId = int(docId)
    review = reviewRecord['review']
    foodItems = set(reviewRecord['foodItems'])
    indices = reviewRecord['indices']
    wordPositions = getStartIndicesOfAllWordsInText(review)

    #splitReview = review.strip().split(' ')
    splitReview = list(filter(None, review.strip().split(' ')))

    if n == 1:
        for i in range(len(splitReview)):
            if len(splitReview[i]):
                if 'beef tartar' in splitReview:
                    print (splitReview[i])
                ngramList.append([docId, i, splitReview[i], splitReview[i] in foodItems and i in indices])

    elif n == 2:
        for i in range(len(splitReview)-1):
            if len(splitReview[i]) and len(splitReview[i+1]):
                combined = splitReview[i] + " " + splitReview[i+1]
                if 'beef tartar' in combined:
                    print (combined, indices, i+1)
                ngramList.append([docId, i+1, combined, combined in foodItems and i+1 in indices])

    elif n == 3:
        for i in range(len(splitReview)-2):
            if len(splitReview[i]) and len(splitReview[i+1]) and len(splitReview[i+2]):
                combined = splitReview[i] + " " + splitReview[i+1] + " " + splitReview[i+2]
                if 'beef tartar' in combined:
                    print (combined)
                ngramList.append([docId, i+2, combined, combined in foodItems and i+2 in indices])

    #print (len(ngramList))
    return ngramList


def main(reviewsJsonPath):
    jsonData = json.load(open(reviewsJsonPath))
    trainingData = []

    for j in jsonData:
        for i in [1, 2, 3]:
            trainingData += generateNGrams(j, i)

    # Write to CSV file
    with open("reviews_wp.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["docID", "position", "term", "label"])
        writer.writerows(trainingData)

    print("Written to reviews_wp.csv")

if len(sys.argv) < 2:
    print("Usage:\npython nGramsGenerator <Path to reviews.json file>")
    sys.exit(0)
else:
    main(sys.argv[1])
