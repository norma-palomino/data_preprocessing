from openpyxl import load_workbook
from get_data_excel import get_excel_data
import csv


def get_ids(excel_data):
   strid = []
   for row in excel_data:
      strid.append(row['StrId'])
   return strid


def compare_ids(list1, list2):
   unused_ids = []
   for ids in list2:
      if ids not in list1:
         unused_ids.append(ids)
   return unused_ids

      
def compare_ids_in_sheets(sheet1, sheet2):
   ids_annot = get_ids(sheet1)       
   ids_new = get_ids(sheet2)
   to_annotate = compare_ids(ids_annot, ids_new)
   return to_annotate   


if __name__ == '__main__':


   workbook_input = raw_input('enter spreadsheet name (should be xlsx): ') # open files
   workbook = load_workbook('./' + workbook_input + '.xlsx')
   
   sheet_input1 = raw_input('enter annotated spreadsheet name (as it appears on the tab name): ') 
   sheet_input2 = raw_input('enter master list spreadsheet name (as it appears on the tab name): ') 
   sheet1 = workbook[sheet_input1]
   sheet2 = workbook[sheet_input2]
   excel_data1 = get_excel_data(sheet1)      
   excel_data2 = get_excel_data(sheet2)   
     
   
   new_uniq_list = compare_ids_in_sheets(excel_data1, excel_data2)

   
   myfile = open('./' + 'non-dups-' + workbook_input + '.csv', 'wb')
   wr = csv.writer(myfile)
   for row in excel_data2:
      if row['StrId'] in new_uniq_list:
         non_annot_tweet = row['StrId'], row['ProjId'], row['TweetText'].encode('utf-8')         
         wr.writerow(non_annot_tweet)

   
     