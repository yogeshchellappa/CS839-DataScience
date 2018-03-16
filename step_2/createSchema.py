'''
Create compatible schemas for both amazon and good reads data
'''

import pandas as pd

def monthToNum(month):
    if month.lower() == 'january':
        return 1
    elif month.lower() == 'february':
        return 2
    elif month.lower() == 'march':
        return 3
    elif month.lower() == 'april':
        return 4
    elif month.lower() == 'may':
        return 5
    elif month.lower() == 'june':
        return 6
    elif month.lower() == 'july':
        return 7
    elif month.lower() == 'august':
        return 8
    elif month.lower() == 'september':
        return 9
    elif month.lower() == 'october':
        return 10
    elif month.lower() == 'november':
        return 11
    elif month.lower() == 'december':
        return 12
    else:
        return 0

def convertDateAmazon(date):
    parts = date.split(' ')
    parts = list(filter(None, parts))
    parts = [p for p in parts if p != ',']

    month = day = year = '0'

    if len(parts) == 0:
        return None

    if len(parts) <= 4:
        if monthToNum(parts[0]) == 0:
            try:
                if int(parts[0]) > 31:
                    year = parts[0]
                else:
                    day = parts[0]
                    year = parts[1]
            except:
                pass

    for i in range(len(parts)):
        if i == 0:
            month = monthToNum(parts[i])
        elif i == 1:
            day = parts[i]
        else:
            year = parts[i]

    else:
        return year+'-'+str(month)+'-'+day

def convertDateGR(date):
    parts = date.split(' ')

    if len(parts) >= 1:
        return parts[0]
    else:
        return None

def main():
    filename_amazon = 'amazonCleaned.csv'
    filename_goodreads = 'goodreadsCleaned.csv'

    data_amazon = pd.read_csv(filename_amazon)
    data_gr = pd.read_csv(filename_goodreads)

    numAmazon = len(data_amazon)
    numGR = len(data_gr)

    print ('Stats before')
    print (data_amazon.keys(), data_gr.keys())
    print (numAmazon, numGR)
    print ('-----')

    # Drop unnecessary columns
    data_amazon = data_amazon.drop(columns=['ID', 'ISBN-10', 'ISBN-13'])
    data_gr = data_gr.drop(columns=['book_name_alt', 'id', 'source'])

    # Convert amazon data dates, rating and no. of pages to match goodreads'
    data_amazon['Pages'] = data_amazon.apply(lambda row: int(str(row['Pages']).split(' ')[0]) if str(row['Pages']).lower() != 'nan' else -1, axis=1)
    data_amazon['Rating'] = data_amazon.apply(lambda row: float(str(row['Rating']).split(' ')[0]) if str(row['Rating']).lower() != 'nan' else -1, axis=1)
    data_amazon['Publishing Date'] = data_amazon.apply(lambda row: convertDateAmazon(row['Publishing Date']), axis=1)

    # Convert good reads date to match above date
    data_gr['date_published'] = data_gr.apply(lambda row: convertDateGR(row['date_published']) if str(row['date_published']).lower() != 'nan' else -1, axis=1)

    # Store with matching columns
    cols = ['Name', 'Author', 'Publisher', 'Publishing_Date', 'Format', 'Pages', 'Rating']
    data_amazon = data_amazon[['Name', 'Author', 'Publisher', 'Publishing Date', 'Format', 'Pages', 'Rating']]
    data_amazon.columns = cols

    data_gr = data_gr[['book_name', 'author', 'publisher', 'date_published', 'book_format', 'count_pages', 'avg_rating']]
    data_gr.columns = cols

    # Make sure no rows were dropped
    print('Stats After')
    print(data_amazon.keys(), data_gr.keys())
    print(len(data_amazon), len(data_gr))
    print('-----')

    assert len(data_amazon) == numAmazon and len(data_gr) == numGR

    # Save data
    data_amazon.to_csv('source1.csv', index=False)
    data_gr.to_csv('source2.csv', index=False)


if __name__ == "__main__":
    main()