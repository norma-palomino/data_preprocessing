
from openpyxl import load_workbook

from collections import defaultdict

from operator import itemgetter



def compare_projids(listofdics):
    output = defaultdict(list)
    for item in listofdics:
        output[item.get('StrId')].append(item.get('ProjId'))
        dict(output)
    return output




if __name__ == '__main__':
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
        
    #print 'this is excel_data: ', excel_data    


    
    to_replace = compare_projids(excel_data)
    print to_replace    