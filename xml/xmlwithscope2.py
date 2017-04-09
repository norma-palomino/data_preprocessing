import xml.etree.ElementTree as ET
from openpyxl import load_workbook

workbook = load_workbook('./barelyfullforconversionxmlclean.xlsx')

sheet = workbook['Sheet1']


headers = ["StrId", "Id", "Text", "Label"]


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

#print excel_data

corpus = ET.Element("Corpus")

# SCOPE: take text like "left [middle text] right" ##########################
# and make xml: <Text>left<Scope>middle text</Scope> right</Text>

def make_text_with_scope(value):
	# create xml node elements "Text" and "Scope"
	parent = ET.Element('Text')
	child = ET.Element('Scope')

	# find the scope, annotated in the file between square brackets
	start = value.find('[')
	end = value.find(']')

	# indentify all tokens between 'start' and 'end', which constitutes the scope
	scope_text = value[start + 1: end]
	left = value[: start]
	right = value[end + 1:]

	# put together the sentence with scope marked
	parent.text = unicode(left)
	child.text = unicode(scope_text)
	child.tail = unicode(right)
	parent.append(child)
	
	# return sentence with marked scope
	#print parent
	return parent 
        

#make xml of text without scope
def make_text_without_scope(value):
	element = ET.Element('Text')
	element.text = unicode(value)
	return element

def has_brackets(value):
	return '[' in value and']' in value

def make_text(value):
	element = None
	if has_brackets(value):
		element = make_text_with_scope(value)
	else:
		element = make_text_without_scope(value)
	#print element
	return element

#CUE: ####################

# take text like "left [middle text] right"
# and make xml: <Text>left<Cue>middle text</Cue> right</Text>

def make_text_with_cue(value):
	# create xml node elements "Text" and "Cue"
	parent = ET.Element('Text')
	child = ET.Element('Cue')

	# find the cue, annotated between '+' and '+*' characters
	start = value.find('+')
	end = value.find('+*')

	# indentify all tokens between 'start' and 'end', which constitutes the cue
	cue_text = value[start + 1: end]
	left_c = value[: start]
	right_c = value[end + 1:]

	# put together the sentence with cue marked
	parent.text = unicode(left_c)
	child.text = unicode(cue_text)
	child.tail = unicode(right_c)
	parent.append(child)
	
	# return sentence with marked cue
        #print parent	
	return parent 
	
        

#make xml of text without cue
def make_text_without_cue(value):
	element = ET.Element('Text')
	element.text = unicode(value)
	#print element
	return element

def has_cue_marks(value):
	#print element
	return '+' in value and'+*' in value

def make_cue(value):
	element = None
	if has_cue_marks(value):
		element = make_text_with_cue(value)
	else:
		element = make_text_without_cue(value)
	#print element
	return element

#.####################################


for row in excel_data:
	tweet = ET.Element("Tweet")	
	for key in row:
		value = row[key]
		element = None
		if key is 'Text':
			element = make_text(value) #and make_cue(value)
		else:
			element = ET.Element(key)
			element.text = unicode(value)
	
	        tweet.append(element)
        corpus.append(tweet)


tree = ET.ElementTree(corpus)
tree.write('tweet_xml2.xml')
