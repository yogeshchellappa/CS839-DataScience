from bs4 import BeautifulSoup
import requests
import re
from collections import OrderedDict
import json
import time

# Append page number at the end
		   
#BASE_URL = 'https://www.amazon.com/s/ref=sr_pg_{0}?rh=n%3A283155%2Ck%3Afantasy%2Cp_n_feature_browse-bin%3A2656022011&page={1}'
#BASE_URL = 'https://www.amazon.com/s/ref=sr_pg_{0}?rh=n%3A283155%2Cn%3A18%2Ck%3Afantasy%2Cp_n_feature_browse-bin%3A2656022011&page={1}'
#BASE_URL =  'https://www.amazon.com/s/ref=sr_pg_{0}?rh=n%3A283155%2Cn%3A25%2Cn%3A16190%2Cn%3A10159265011%2Ck%3Afantasy%2Cp_n_feature_browse-bin%3A2656022011&page={1}'
BASE_URL = 'https://www.amazon.com/s/ref=sr_pg_{0}?rh=n%3A283155%2Cn%3A25%2Cn%3A16190%2Cn%3A14051773011%2Ck%3Afantasy%2Cp_n_feature_browse-bin%3A2656022011&page={1}'
headers={'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}

regex = re.compile('\/\d.*?\/')
records = []

# Generator; Last result ID: 588
results = (i for i in range(3000))

for pageNumber in range(1,50):
	url = BASE_URL.format(pageNumber, pageNumber)
	response = requests.get(url, headers=headers)
	
	soup = BeautifulSoup(response.content, 'lxml')
	
	# 11 results in each page, 0 to 11 inclusive
	for i in range(12):
		try:
			tags = OrderedDict()
			resultId = next(results)

			selector = '#result_{0} > div > div > div > div.a-fixed-left-grid-col.a-col-right > div.a-row.a-spacing-small a'.format(resultId)
			hyperlinks = soup.select(selector)
			#print(hyperlinks)
			
			tags['id'] = regex.search(hyperlinks[0]['href']).group(0).strip("\\").strip('/')
			tags['book_name'] = hyperlinks[0]['title']
				
			records.append(tags)
		except Exception as e:
			print("Error in page: " + str(pageNumber) + ", result ID: " + str(resultId))
	
	time.sleep(3)
	print("Page " + str(pageNumber) + " scraped")

print("Number of records scraped: " + str(len(records)))	
print("Last result ID: " + str(next(results)))
with open('AmazonBooks-1.json', 'w') as outputFile:
	json.dump(records, outputFile)

print("Successfully created JSON file!")