from openpyxl import load_workbook
from get_data_excel import get_excel_data
import csv


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
  return skipper



if __name__ == '__main__':
  
  #sheet1 = workbook['SeldomAnnot']
  #sheet2 = workbook['SeldomAll']

  workbook_input = raw_input('enter spreadsheet name (should be xlsx): ') # open files
  workbook = load_workbook('./' + workbook_input + '.xlsx')
  #workbook column names: headers = ["StrId", "ProjId", "TweetText", "Label"]

  sheet_input1 = raw_input('enter first spreadsheet name (as it appears on the tab name): ') 
  sheet_input2 = raw_input('enter second spreadsheet name (as it appears on the tab name): ') 
  sheet1 = workbook[sheet_input1]
  sheet2 = workbook[sheet_input2]
  
  excel_data1 = get_excel_data(sheet1)
  
  excel_data2 = get_excel_data(sheet2)    

  skipper = create_skipper(get_identifier)
  
  new_workbook_input = raw_input('enter the name of your new csv file: ')
    
  writer = csv.writer(open('./' + new_workbook_input + '.csv', 'w'))
  
  for row in skipper(excel_data1):
    str_id=row['StrId']
    projid=row['ProjId']
    tweet_text = row['TweetText'].encode('utf-8')
    writer.writerow([str_id,projid, tweet_text])
  for row in skipper(excel_data2):
    str_id=row['StrId']
    projid=row['ProjId']
    tweet_text = row['TweetText'].encode('utf-8')
    writer.writerow([str_id,projid, tweet_text])
