from bs4 import BeautifulSoup
import requests
import re
from collections import OrderedDict
import json
import time
import sys
import pandas as pd
import numpy as np
import glob
import os

def getNewHeader():
	desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
 
	return {'User-Agent': np.random.choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
 

def readJson(fileName):
	data = json.load(open(fileName), encoding='utf8')
	return data

	
def getIDsAlreadyScraped(fileName):
	fp = open(fileName, 'r')
	contents = fp.read()
	contents = contents.split("\n")
	return set(contents)

	
def clean(df):    
    # Drop duplicates
    df = df.drop_duplicates('ID')

    # Retain necessary columns and drop the rest
    toKeep = set(['ID','Name','Author','Rating','Publisher','Pages','Publishing Date', 'ISBN-10', 'ISBN-13'])
    toDrop = [i for i in df.columns.values if i not in toKeep]
    
    df = df.drop(toDrop, axis=1)

    # Add book format
    formats = ["Paperback", "Hardcover", "Kindle"]
    df.insert(4, "Format", np.random.choice(formats, len(df)))
    
    # Rearrange columns
    df = df[['ID','Name','Author','Rating','Format','Publisher','Pages','Publishing Date', 'ISBN-10', 'ISBN-13']]
    return df

	
def concatenate(sourceFile, df):
	df_cleaned = pd.read_csv(sourceFile, encoding='utf8', dtype=object)

	oldLen = len(df_cleaned)

	# Concatenate
	finalDf = df_cleaned.append(df, ignore_index=True)
	finalDf = finalDf.drop_duplicates('ID')

	# Write back to data store
	finalDf.to_csv("amazonCleaned.csv", encoding='utf-8', index=False)

	# Maintain list of IDs
	ids = set(finalDf['ID'].tolist())
	with open('ids.txt','w') as outputFile:
		outputFile.write("\n".join(str(x) for x in ids))

	# Changelog
	print("\nDatabase updated!")
	print("Added: " + str(len(ids) - oldLen) + " record(s).")
	print("Current size: " + str(len(ids)))

	
def cleanJsonAndAddToSource(outputFile, sourceFile):
	jVal = pd.read_json(outputFile, encoding='utf-8', dtype=object)
	if len(jVal) > 0:
		cleaned = clean(jVal)
		concatenate(sourceFile, cleaned)
	else:
		os.remove(outputFile)
		print("All records scraped in this range!")

		
def fetchDetails(datafileName, idFileName, start, end):
	BASE_URL = 'http://www.amazon.com/dp/{0}'
	
	# Read data
	data = readJson(datafileName)
	
	# Read IDs already scraped
	alreadyScraped = getIDsAlreadyScraped(idFileName)
	
	# Open file for writing errors
	name = 'dropped' + str(start) + str(end) + '.txt'
	fp = open(name, 'a')
	count = 0
	
	ids = [data[i]['id'] for i in range(len(data))]
	names = [data[i]['book_name'] for i in range(len(data))]
	
	ids = ids[start:end]
	
	records = []	
	for i, name in zip(ids, names):	
		if i in alreadyScraped:
			continue
		
		tags = OrderedDict()
		
		# Add details from existing data
		tags["ID"] = i
		tags["Name"] = name
		
		url = BASE_URL.format(i)
		
		# Get a new header for every call
		headers = getNewHeader()
		
		response = requests.get(url, headers)
		soup = BeautifulSoup(response.content, 'lxml')
		
		# Bot check
		strSoup = str(soup)
		if "Sorry, we just need to make sure you're not a robot" in strSoup:
			print("Bot warning! Switching user agent...")
			time.sleep(3)
			continue
		
		isAuthorPresent = False
		isDetailsPresent = False
		
		# Get author
		author = soup.select('a.a-link-normal.contributorNameID')
		if author:
			isAuthorPresent = True
			tags['Author'] = author[0].getText()
				
		author = soup.select('#byline > span > a')
		if isAuthorPresent is False and author:
			isAuthorPresent = True
			tags['Author'] = author[0].getText()
			
		# Rating might be null for newly rated books; hence we will accept empty rating
		rating = soup.select('span.arp-rating-out-of-text')		
		for span in rating:
			tags["Rating"] = span.getText()

		listItems = soup.select('table#productDetailsTable div.content ul li')
		if listItems:
			isDetailsPresent = True
			
			# Get book details
			for li in listItems:
				try:
					title = li.b
					key = title.text.strip().rstrip(':')
					value = None
					
					if title.next_sibling:
						value = title.next_sibling.strip().rstrip("(")

					if value:
						if key == "Publisher":
							splitval = value.split('(')
							publisherName = splitval[0].strip()
							publishingDate = splitval[1].rstrip(")")
							tags[key] = publisherName
							tags['Publishing Date'] = publishingDate					
						elif key == "Paperback" or key == "Mass Market Paperback":
							tags['Pages'] = value
						else:
							tags[key] = value.strip()
				except Exception as e:
					print("Error in retrieving ID: " + str(i))
					print(e)
					print()

		if isAuthorPresent and isDetailsPresent:
			records.append(tags)
			print("Scraped: " + str(len(records)) + "/" + str(end-start))
		else:
			count += 1
			print("Dropped: " + str(count) + "/" + str(end-start))
			fp.write(i + '\n')
		
		time.sleep(3)

	fp.close()
	
	# Write to json file
	outputName = 'AmazonRecords' + str(start) + str(end) + '.json'
	with open(outputName, 'w') as outfile:
		json.dump(records, outfile)
	
	return outputName

		
def main(amazonBooksJson, existingIDs, cleanDB, startRange, endRange):
	# Output of current scrape
	outputFile = fetchDetails(amazonBooksJson, existingIDs, startRange, endRange)
	
	# Add the cleaned output to DB
	cleanJsonAndAddToSource(outputFile, cleanDB)
	
	# Handle retries
	
	
		
if __name__ == "__main__":
	if len(sys.argv) < 5:
		print("Usage:\npython fetchDetails <Path to AmazonBooks.json> <Path to IDs already Scraped> <Path to amazonCleaned.csv> <start> <end>")
		sys.exit(0)
	else:
		main(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]))