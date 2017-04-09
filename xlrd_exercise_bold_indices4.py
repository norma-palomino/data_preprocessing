#from __future__ import print_function

import xlrd
import xml.etree.ElementTree as ET

book = xlrd.open_workbook('./finalcorpusconversion1.xls', formatting_info=True)

first_sheet = book.sheet_by_index(0)

corpus = ET.Element("Corpus")

first_row = []
for col in range(first_sheet.ncols):
    first_row.append(first_sheet.cell_value(0, col))

excel_data = []
for row_idx in range(first_sheet.nrows):
    if row_idx is 0:
	continue
    row_data = {}
    for col_idx in range(first_sheet.ncols):
	# REFERENCES:
	# COL_IDXID = 0  # getting values from StrId column
	# COL_IDXPRID = 1  # getting ProjId values
	# COL_IDX = 2  # getting TweetText values
	# COL_LBL = 3  # getting Label values

	text_cell_id = first_sheet.cell_value(row_idx, 0)
	text_cell_project_id = first_sheet.cell_value(row_idx, 1)
	text_cell = first_sheet.cell_value(row_idx, 2)
	text_cell_label = first_sheet.cell_value(row_idx, 3)

	row_data['StrId'] = text_cell_id
	row_data['ProjId'] = text_cell_project_id
	row_data['TweetText'] = text_cell
	row_data['Label'] = text_cell_label
    excel_data.append(row_data)

    text_cell_xf = book.xf_list[first_sheet.cell_xf_index(row_idx, 2)]
    text_cell_runlist = first_sheet.rich_text_runlist_map.get((row_idx, 2))
    print 'Text cell runlist: ', text_cell_runlist


dic_offsets = {}


def add_cues(element):
    cue = ET.Element("Cue")
    if text_cell_runlist:
	# get a list of lists of cue indexes:
	cues_indexes = get_cue_indexes(text_cell_runlist)
	# (runlist start value) - (offset of the parent) = (real start value)

	for cue_list in cues_indexes:
	    # first element in the first list of lists is the start; second element is the end of that list
	    start = cue_list[0] - dic_offsets[element]
	    end = cue_list[1] - dic_offsets[element]
	    # from element.text, get the cue text based on the indexes
	    cue_text = element.text[start:end + 1]
	    # get the previous part of the tweet
	    left_c = element.text[:start]
	    # get the text after the cue as its tail
	    tail_c = element.text[end + 1:]
	    cue.text = unicode(cue_text)
	    cue.tail = unicode(tail_c)
	    element.text = left_c
	element.append(cue)
	#print cue

def get_cue_indexes(text_cell_runlist):
    found_first_cue = False
    cues = []
    start = None
    for index, format_type in text_cell_runlist:
	if format_type is 0 and not found_first_cue:
	    continue
	found_first_cue = True
	cue_is_started = start is not None
	if not cue_is_started:
	    start = index
	else:
	    end = index - 1
	    cues.append([start, end])
	    start = None
    print cues
    #return cues

def cueify(element):
    #print 'checking runlist: ', text_cell_runlist
    if text_cell_runlist:
	element = add_cues(element)


def add_scope(element):
    # create scope object
    scope = ET.Element("Scope")

    # find scope delimiters
    start = element.text.find('[')
    end = element.text.find(']')

    # add the offset of the scope element to the dictionary of offsets
    dic_offsets[scope] = start

    # find scope tokens
    scope_text = element.text[start + 1:end]
    left = element.text[:start]
    tail = element.text[end: +1]

    # put the sentence back together
    element.text = unicode(left)
    scope.text = unicode(scope_text)
    scope.tail = unicode(tail)
    # adding left + scope(+tail)
    element.append(scope)
    #print scope


def has_brackets(text_cell):
    return '[' in text_cell and ']' in text_cell


def scopify(element):
    if has_brackets(element.text):
	element = add_scope(element)


for row in excel_data:
    tweet = ET.Element("Tweet")
    for key in row:
	value = row[key]
	element = None
	if key is 'TweetText':
	    element = ET.Element("TweetText")
	    element.text = value
	    scopify(element)
	    cueify(element)
	else:
	    element = ET.Element(key)
	    element.text = unicode(value)
	tweet.append(element)
    corpus.append(tweet)

tree = ET.ElementTree(corpus)

tree.write('full_tweets_xml.xml')
