import os
import glob
import string
import json
import re
import sys
from collections import OrderedDict

def clean(s):
    return re.sub('[ \t\n]+', ' ', re.sub(r'[\<\/\>]', ' ', s)).strip()

def find_entities(s):
    n = 0
    stack = []
    tag_locs = []
    entityList = []
    for i, c in enumerate(s):
        if s[i] == '<':
            stack.append(i)
            print("stack at " + c + ": " + '[%s]' % ', '.join(map(str, stack)))
        elif s[i] == '/' and s[i+1] == '>':
            try:
                tag_locs.append((stack.pop(), i))
                print("locs at " + c + ": " + '[%s]' % ', '.join(map(str, tag_locs)))
            except IndexError:
                raise IndexError('Too many closing tags at index {} in {}'.format(i,s))
        if not stack and tag_locs:
            entity_loc = tag_locs.pop() 
            entity = clean(s[entity_loc[0]:entity_loc[1]])
            entityList.append(({entity : [entity] + [clean(s[loc[0]:loc[1]]) for loc in tag_locs]}))
            tag_locs = []
            print("entity list: " + '[%s]' % ', '.join(map(str, entityList)))
    if stack:
        print("stack: " + '[%s]' % ', '.join(map(str, stack)))
        raise IndexError('Unbalanced tags at index {} in {}'.format(stack.pop(),s))
    return entityList

def preprocessingRules():
	"""
	Returns translator object which encapsulates all the string cleaning we do
	"""
	unnecessaryCharacters = string.punctuation + string.digits + '\t\n\r'

	# We need to retain the punctuation representing the tags we have used to mark up the dataset.
	unnecessaryCharacters = unnecessaryCharacters.replace("<","").replace(">","").replace("/","").replace(".","")

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
	
	for file in reviewFiles:
		filePointer = open(file, 'r')
		review = filePointer.read()
		filePointer.close()

		top_lvl_fo = [list(k.keys())[0] for k in find_entities(review)]
		
		review = review.lower()
		review = review.translate(translator)
		
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
		
		# Next, get the indices of the food items
		for item in foodItems:
			indices += [[i.start(), i.end()] for i in list(re.finditer(item, review))]
			
		# Merge intervals
		indices = mergeIntervals(indices)
		
		# Finally, build the json
		record = OrderedDict()

		# File name serves as record ID
		record["id"] = file[-7:-4]
		
		record["review"] = review
		record["foodItems"] = top_lvl_fo
		record["indices"] = indices
		
		reviewDicts.append(record)
	
	with open('reviews.json', 'w') as outfile:
		json.dump(reviewDicts, outfile)
	
	print("Successfully created JSON file!")
	
if len(sys.argv) < 2:
	print("Usage:\npython getTrainingData <Path to folder with reviews>")
	sys.exit(0)
else:
	getTrainingData(sys.argv[1])
	
	