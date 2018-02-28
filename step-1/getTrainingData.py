import os
import glob
import string
import json
import re
import sys
from collections import OrderedDict


def preprocessingRules():
	"""
	Returns translator object which encapsulates all the string cleaning we do
	"""
	unnecessaryCharacters = string.punctuation + string.digits + '\n\t\r'

	# We need to retain the punctuation representing the tags we have used to mark up the dataset.
	unnecessaryCharacters = unnecessaryCharacters.replace("<","").replace(">","").replace("/","").replace(".",'')

	# translator will be used to map the characters in unnecessaryCharacters to None
	translator = str.maketrans('', '', unnecessaryCharacters)
	
	return translator
	
def mergeIntervals(intervals):
    output = []
    for i in sorted(intervals, key=lambda x: x[0]):
        if output and output[-1][1] > i[0]:
            output[-1][1] = max(output[-1][1], i[1])
        else:
            output.append(i)

    return output
	
def getTrainingData(reviewFolderPath):
	reviewDicts = []
	
	# Get the translator
	translator = preprocessingRules()
	
	# Read the files
	reviewFiles = glob.glob(reviewFolderPath + "*.txt")
	count = 0
	noncount = 0
	capitalizedWord = 0
	
	for file in reviewFiles:
		filePointer = open(file, 'r')
		review = filePointer.read()
		filePointer.close()
		
		review = review.translate(translator)
		
		capitalizedWord += sum(1 for c in review if c.isupper())
		
		review = review.replace("."," ")
		# Stores the food items detected
		foodItems = []
		
		# Stores the indices of the detected items
		indices = []
		
		# Regex for detecting the food items
		pattern = re.compile('<.*?\/>')
		
		# Find all the food items using regex
		foodMatches = pattern.findall(review)
		
		# Replace annotated items without the tags
		for annotatedFoodItem in foodMatches:
			foodItemWithoutTags = annotatedFoodItem[1:-2]
			review = review.replace(annotatedFoodItem, foodItemWithoutTags)
			
			foodItems.append(foodItemWithoutTags)
		
		for i in foodItems:
			if i[0].isupper():
				count += 1
			else:
				noncount += 1
				
		# Next, get the indices of the food items
		for item in foodItems:
			indices += [[i.start(), i.end()] for i in list(re.finditer(item, review))]
			
		# Merge intervals
		indices = mergeIntervals(indices)
		
		# Finally, build the json
		record = OrderedDict()

		# File name serves as record ID
		fileName = file.split("/")[-1].split("\\")[-1].split(".")[0]
		record["id"] = fileName
		
		# Since we skipped / as it was present in the tags, now we remove / as well
		review = review.replace("/"," ")
		
		record["review"] = review.replace("/","")
		record["foodItems"] = foodItems
		record["indices"] = indices
		
		reviewDicts.append(record)
	
	with open('reviews.json', 'w') as outfile:
		json.dump(reviewDicts, outfile)
	
	print("Successfully created JSON file!")
	print("Food with uppercase: " + str(count))
	print("Food without uppercase: " + str(noncount))
	print("All capitalized words: " + str(capitalizedWord))
	
if len(sys.argv) < 2:
	print("Usage:\npython getTrainingData <Path to folder with reviews>")
	sys.exit(0)
else:
	getTrainingData(sys.argv[1])
	
	
	
	
