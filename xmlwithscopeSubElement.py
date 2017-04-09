 from xml.etree.ElementTree import Element, SubElement
 
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
 
 #marking cue and scope at the same time, as subelements of 
 
 def make_text_with_cue_scope(value):
	 # create xml node elements "Text", "Scope", and "Cue"
	 parent = ET.Element('Text')
	 #scope = SubElement(parent, "Scope")
	 cue = SubElement(parent, "Cue")
 
        # find the cue, annotated between '+' and '+*' characters
	 start = value.find('+')
	 end = value.find('+*')
 
	 # indentify all tokens between 'start' and 'end', which constitutes the cue
	 scope_text = value[start + 1: end]
	 left_c = value[: start]
	 right_c = value[end + 1:] 

	 # put together the sentence with cue marked
	 parent.text = unicode(left_c)
	 cue.text = unicode(cue_text)
	 cue.tail = unicode(right_c)
	 parent.append(scope) 



 