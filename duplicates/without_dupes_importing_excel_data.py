from openpyxl import load_workbook
from get_data_excel import get_excel_data
import csv

workbook = load_workbook('./seldom_cleaning.xlsx')
#workbook column names: headers = ["StrId", "ProjId", "TweetText", "Label"]

sheet1 = workbook['SeldomAnnot']
sheet2 = workbook['SeldomAll']

excel_data1 = get_excel_data(sheet1)

excel_data2 = get_excel_data(sheet2)

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

skipper = create_skipper(get_identifier)

  
writer = csv.writer(open("./non-dups-seldom.csv", 'w'))
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


  