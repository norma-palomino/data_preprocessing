# find a package that will find the bold format, then find the character offset count to annotate cue

import xml.etree.ElementTree as ET

from openpyxl import load_workbook

workbook = load_workbook('./HardlyForXML.xlsx')

sheet = workbook['ConvertedHardly']

headers = ["StrId", "Id", "Text", "Label"]

excel_data = []

for row_num, row in enumerate(sheet):
    # skip the first row (don't want headers)
    if row_num is 0:
        continue
    # open a dictionary
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

# create the corpus object
corpus = ET.Element("Corpus")


# set a function that finds Scope marks ('[' and ']')
def has_brackets(value):
    return '[' in value and ']' in value


# takes the element and replaces the "[ ]" marks with a new scope object ("ET.element")
def add_scope(element):
    # create the "Scope" object
    scope = ET.Element("Scope")

    # find the scope, annotated in the file between square brackets
    start = element.text.find('[')
    end = element.text.find(']')

    # indentify all tokens between 'start' and 'end', which constitutes the scope
    scope_text = element.text[start + 1: end]
    left = element.text[: start]
    tail = element.text[end + 1:]

    # put together the sentence with scope marked. The sentence belongs to the element attribute "text"
    element.text = unicode(left)
    scope.text = unicode(scope_text)
    scope.tail = unicode(tail)
    # append the scope to the element
    element.append(scope)
    # run the function that makes an object out of the "Cue" marks
    cueify(scope)


# function that creates a scope when it finds square brackets
def scopify(element):
    if has_brackets(element.text):
        element = add_scope(element)


# set a function that finds Cue marks ('+' and '+*')
def has_cue_marks(value):
    return '++' in value and '+*' in value


def find_all(string, sub):
    result = []
    k = 0
    while k < len(string):
        k = string.find(sub, k)
        if k == -1:
            return result
        else:
            result.append(k)
            k += 1
    return result


# takes the element and replaces the "+  +*" marks with a new cue object ("ET.element")
def add_cue(element):
    # use Find All inside add_cue

    # create a object named "cue and put it into a variable
    cue = ET.Element("Cue")

    # find the cue, annotated in the file between "+" and "+*"
    # start_c = element.text.find('+')
    # end_c = element.text.find('+*')
    start_c = find_all(element.text, '++')
    end_c = find_all(element.text, '+*')

    # indentify all tokens between 'start' and 'end', which constitutes the cue
    cue_text = element.text[start_c + 1: end_c]
    left_c = element.text[: start_c]
    tail_c = element.text[end_c + 1:]

    # put together the sentence with cue marked
    element.text = unicode(left_c)
    cue.text = unicode(cue_text)
    cue.tail = unicode(tail_c)
    element.append(cue)


# gets an element, finds the cue marks, and then passes element object through the add_cue function
# if there are no cue marks, it won't do anything
def cueify(element):
    if has_cue_marks(element.text):
        element = add_cue(element)

    # do for the tail the same thing we did for the text


for row in excel_data:
    # define the object "Tweet"
    tweet = ET.Element("Tweet")
    # get the tweet text (as value of each key) to work on cue and scope
    for key in row:
        value = row[key]
        # there is no element defined yet
        element = None
        if key is 'Text':
            element = ET.Element("Text")
            element.text = value
            scopify(element)
            cueify(element)

        # if it's not text.... (?)
        else:
            element = ET.Element(key)
            element.text = unicode(value)
        tweet.append(element)
    corpus.append(tweet)

tree = ET.ElementTree(corpus)

tree.write('convetedhardlyall.xml')
