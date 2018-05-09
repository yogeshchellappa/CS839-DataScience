def getOlderDate(time1, time2):
    """
    Helper function to get the older of the 2 dates, time1 and time2.
    """
    # We have imputed missing day, month or year with a 0; Replacing the 0 with 1 here
    time1 = '-'.join(index if index != '0' else '1' for index in time1.split('-'))
    time2 = '-'.join(index if index != '0' else '1' for index in time2.split('-'))
    
    minValue =  min(datetime.strptime(time1, '%Y-%M-%d'), datetime.strptime(time2, '%Y-%M-%d'))
    return minValue.strftime('%Y-%M-%d')
	
	
def noneHandler(cell1, cell2):
	"""
	Handles nan present in the cells
	"""
    if cell1 == 'nan' and cell2 == 'nan':
        return None
    
    return cell1 if cell1 != 'nan' else cell2
	

def merge(matches):
    """
    Takes in the matches dataframe, extracts the matching 
    rows one by one from each table and then merges them.
    """
    output = []
    
    # Get the indices of the matching rows from each table as a tuple: e.g. (31, 26)
    indices = list(zip(matches['ltable_ID'].tolist(), matches['rtable_ID'].tolist()))
    
    for index1, index2 in indices:
        # Holds the merged row
        merged = []
        
        # take max length
        for column in ['Name','Author']:
            cell1 = str(A.at[index1, column])
            cell2 = str(B.at[index2, column])
            
            if cell1 != 'nan' and cell2 != 'nan':
                merged.append(max(cell1, cell2))
            else:
                merged.append(noneHandler(cell1, cell2))
        
        # take the oldest publishing date, publisher and format
        for column in ['Publishing_Date']:
            cell1 = str(A.at[index1, column])
            cell2 = str(B.at[index2, column])
            
            if cell1 != 'nan' and cell2 != 'nan':
                olderDate = getOlderDate(cell1, cell2)
                if olderDate == cell1:
                    merged += [A.at[index1, 'Publisher'], olderDate, A.at[index1, 'Format']]
                else:
                    merged += [B.at[index2, 'Publisher'], olderDate, B.at[index2, 'Format']]
            elif cell1 == 'nan' and cell2 == 'nan':
                # Publishing date is none for both
                pubCell1 = A.at[index1, 'Publisher']
                pubCell2 = B.at[index2, 'Publisher']
                formatCell1 = A.at[index1, 'Format']
                formatCell2 = B.at[index2, 'Format']
                
                # Take max of the publisher and format
                if pubCell1 != 'nan' and pubCell2 != 'nan' and formatCell1 != 'nan' and formatCell2 != 'nan':
                    merged += [max(pubCell1, pubCell2), None, max(formatCell1, formatCell2)]
                else:
                    merged += [noneHandler(pubCell1, pubCell2), None, noneHandler(formatCell1, formatCell2)]
            elif cell2 == 'nan':
                merged += [A.at[index1, 'Publisher'], A.at[index1, 'Publishing_Date'], A.at[index1, 'Format']]
            else:
                merged += [B.at[index2, 'Publisher'], B.at[index2, 'Publishing_Date'], B.at[index2, 'Format']]
                
        for column in ['Pages','Rating']:
            cell1 = str(A.at[index1, column])
            cell2 = str(B.at[index2, column])
            
            if cell1 != 'nan' and cell2 != 'nan':
                avgValue = np.mean([float(cell1), float(cell2)])
                # Round the number of pages to nearest int, as we cannot have 127.5 pages
                if column == 'Pages':
                    merged.append(str(round(avgValue)))
                else:
                    merged.append(str(round(avgValue, 2)))
            else:
                merged.append(noneHandler(cell1, cell2))
            
        output.append(merged)
    
    return pd.DataFrame(output, columns=['Name', 'Author', 'Publisher', 'Publishing_Date', 'Format','Pages', 'Rating'])	
	
merged = merge(matches)