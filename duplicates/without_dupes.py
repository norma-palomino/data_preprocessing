


def create_skipper(get_identifier):
  unique_item_identifiers = set([])
  def skipper(enumerable):
    for item in enumerable:
      if get_identifier(item) in unique_item_identifiers:
        continue # skip this one
      unique_item_identifiers.add(get_identifier(item))
      yield item
  return skipper


def read_excel():
  yield {'StrID': 'tweet1'}
  yield {'StrID': 'tweet2'} 
  yield {'StrID': 'tweet1'} 
  yield {'StrID': 'tweet3'} 
  yield {'StrID': 'tweet1'} 

def read_excel_2():
  yield {'StrID': 'tweet1'}
  yield {'StrID': 'tweet2'}   
  yield {'StrID': 'tweet3'}
  yield {'StrID': 'tweet2'} 
  yield {'StrID': 'tweet5'} 
  yield {'StrID': 'tweet6'} 
  yield {'StrID': 'tweet5'} 

# without using the skipper
# for row in read_excel():
#   print row

def get_identifier(row):
  return row['StrID']

# skipper is a function that transforms an enumerator
skipper = create_skipper(get_identifier)

print 'unique items found in Excel file 1'
for row in skipper(read_excel()):
  print 'found: ', row


print '\nunique items found in Excel file 1 and 2'
for row in skipper(read_excel_2()):
  print 'found: ', row
  
print '\ndouble-checking the output against files 1 and 2 again'
for row in skipper(read_excel()):
  print 'found: ',row





