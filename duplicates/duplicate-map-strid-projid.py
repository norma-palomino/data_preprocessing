
from openpyxl import load_workbook

from collections import Counter, defaultdict
#from collections import defaultdict

from operator import itemgetter



workbook = load_workbook('./FINAL-CORPUS-CueScopeNotes-TweetID-v6-NoDuplicates-ManuallyReviewed.xlsx')

sheet = workbook['Seldom']


headers = ["StrId", "ProjId", "TweetText", "Label"]


excel_data = []

for row_num, row in enumerate(sheet):
    # skip the first row (don't want headers)
    if row_num is 0:
        continue
    #open a dictionary
    row_data = {}
    # populating the dictionary with header names as keys and cell content as values
    for col_num, cell in enumerate(row):
        if col_num > len(headers) - 1:
            continue
        key = headers[col_num]
        value = cell.value
        row_data[key] = value
    # adding each key-value pair to the excel_data list
    excel_data.append(row_data)
    
#sort duplicate tweets by duplicate count
print Counter(map(itemgetter("StrId"), excel_data))


#for key, value in dups:
    ##str_id=key['StrId']
    ##projid=key['ProjId']    
    #print key['StrId'], key['ProjId']






#this solution works but it's less complete (it doesn't sort duplicate values)
dupl_Ids = defaultdict(int)

#for row in excel_data:
    #if 'StrId' in row:
        #dupl_Ids[row['StrId']] += 1
#print dupl_Ids, key[0], key[1]

