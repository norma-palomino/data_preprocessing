from openpyxl import load_workbook
#from operator import itemgetter

workbook = load_workbook('./finalcorpusduplicatecounts.xlsx')

sheet = workbook['Seldom']
headers = ["StrId", "ProjId", "TweetText", "Label"]


excel_data = []#list of dictionaries ##NAME OF LIST of dict

for row_num, row in enumerate(sheet):
  if row_num is 0: # skip the first row (don't want headers)
    continue
  row_data = {}  #open a dictionary ##NAME OF DICTIONARY OF VALUES IN EACH ROW
  for col_num, cell in enumerate(row): # populating the dictionary with header names as keys and cell content as values# populating the dictionary with header names as keys and cell content as values
    if col_num > len(headers)-1: #ask Max what this is
      continue
    key = headers[col_num]
    value = cell.value
    row_data[key] = value
  excel_data.append(row_data) # adding each key-value pair to the excel_data list
#print excel_data

def get_identifier(row):
  return row['StrId']


def create_skipper(get_identifier):
  unique_item_identifiers = set([])
  def skipper(enumerable):
    for item in enumerable:
      if get_identifier(item) in unique_item_identifiers:
        continue # skip this one
      unique_item_identifiers.add(get_identifier(item))
      yield item
  #print skipper
  return skipper

skipper = create_skipper(get_identifier)


print '\nreading Excel file 1'
for row in skipper(excel_data):
  print row['StrId'], row['ProjId']
 


#WORKS:
#def get_identifier(excel_data):
  #for key in excel_data:
    #if 'StrId' and 'ProjectId' in key:
      #print 'the values are', key["StrId"], key['ProjectId']


#values=get_identifier(excel_data)  
  