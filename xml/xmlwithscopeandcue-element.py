#find a package that will find the bold format, then find the character offset count to annotate cue

import xml.etree.ElementTree as ET

#from xml.etree.ElementTree import Element, SubElement as ET
#from xml.etree.ElementTree import SubElement

from openpyxl import load_workbook

workbook = load_workbook('./barelyfullforconversionxmlcue.xlsx')

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




corpus = ET.Element("Corpus")




# Marking Cue############################

# take text like "left [middle text] right"
# and make xml: <Text>left<Cue>middle text</Cue> right</Text>

#def make_text_with_cue(value):
	## create xml node elements "Text" and "Cue"
	#parent = ET.Element('Text')
	#child = ET.Element('Cue')

	## find the cue, annotated between '+' and '+*' characters
	#start = value.find('+')
	#end = value.find('+*')

	## indentify all tokens between 'start' and 'end', which constitutes the cue
	#cue_text = value[start + 1: end]
	#left_c = value[: start]
	#right_c = value[end + 2:]

	## put together the sentence with cue marked
	#parent.text = unicode(left_c)
	#child.text = unicode(scope_text)
	#child.tail = unicode(right_c)
	#parent.append(child)
	
	## return sentence with marked cue
	#return parent 
        

##make xml of text without cue
#def make_text_without_cue(value):
	#element = ET.Element('Text')
	#element.text = unicode(value)
	#return element

#def has_cue_marks(value):
	#return '+' in value and'+*' in value

#def make_cue(value):
	#element = None
	#if has_cue_marks(value):
		#element = make_text_with_cue(value)
	#else:
		#element = make_text_without_cue(value)
	#return element


# Marking Scope############################

# take text like "left [middle text] right"
# and make xml: <Text>left<Scope>middle text</Scope> right</Text>

def has_brackets(value):
	return '[' in value and']' in value


def add_scope(element):
	#takes the element and replaces the "[ ]" marks with a new scope object ("ET.element")
	
	scope = ET.Element("Scope")
	
	
	# find the scope, annotated in the file between square brackets
	start = element.text.find('[')
	end = element.text.find(']')

	# indentify all tokens between 'start' and 'end', which constitutes the scope
	scope_text = element.text[start + 1: end]
	left = element.text[: start]
	tail = element.text[end + 1:]

	# put together the sentence with scope marked
	element.text = unicode(left)
	scope.text = unicode(scope_text)
	scope.tail = unicode(tail)
	element.append(scope)
	cueify(scope)
	
	
def scopify(element):
	if has_brackets(element.text):
		element = add_scope(element)
		

def has_cue_marks(value):
	return '+' in value and'+*' in value

def add_cue(element):
	#use Find All inside add_cue
	
	#takes the element and replaces the "+ +*" marks with a new scope object ("ET.element")
	
	cue = ET.Element("Cue")
	
	
	# find the scope, annotated in the file between square brackets
	start = element.text.find('+')
	end = element.text.find('+*')

	# indentify all tokens between 'start' and 'end', which constitutes the scope
	cue_text = element.text[start + 1: end]
	left_c= element.text[: start]
	tail_c = element.text[end + 1:]

	# put together the sentence with scope marked
	element.text = unicode(left_c)
	cue.text = unicode(cue_text)
	cue.tail_c = unicode(tail_c)
	element.append(cue)
	
	
# gets an element, finds the cue marks, and then passes element object through the add_cue function
#if there are no cue marks, it won't do anything
def cueify(element):
	if has_cue_marks(element.text):
		element = add_cue(element)
		
	#do for the tail the same thing we did for the text
	#iterate the cueify function

	
#def make_text_with_scope(value):
	## create xml elements "Text" and "Scope"
	#parent = ET.Element('Text')
	#child = ET.Element('Scope')

	## find the scope, annotated in the file between square brackets
	#start = value.find('[')
	#end = value.find(']')

	## indentify all tokens between 'start' and 'end', which constitutes the scope
	#scope_text = value[start + 1: end]
	#left = value[: start]
	#right = value[end + 1:]

	## put together the sentence with scope marked
	#parent.text = unicode(left)
	#child.text = unicode(scope_text)
	#child.tail = unicode(right)
	#parent.append(child)
	
	## return sentence with marked scope
	#return parent 
        
#def with_cue(value): #at the end of the program, we pass the parent returned in make_text_with_scope function

#make xml of text without scope
#def make_text_without_scope(value):
	#element = ET.Element('Text')
	#element.text = unicode(value)
	#return element

#def make_scope(value):
	##element = None
	##if has_brackets(value):
		##element = make_text_with_scope(value)
	##else:
		##element = make_text_without_scope(value)
	##return element


#Mark scope in tweet text###########################


for row in excel_data:
	#define the object "Tweet"
	tweet = ET.Element("Tweet")
	#get the tweet text (as value of each key) to work on cue and scope
	for key in row:
		value = row[key]
		# there is no element defined yet
		element = None
		if key is 'Text':
			element = ET.Element("Text")
			element.text= value
			scopify(element)
			cueify(element)
		
		#if it's not text.... (?)
		else:
			element = ET.Element(key)
			element.text = unicode(value)
		tweet.append(element)
	corpus.append(tweet)

tree = ET.ElementTree(corpus)

tree.write('tweet_xml.xml')
