#xlrd used for identifyhing indexes of rich format text (cues)
import xlrd
import xml.etree.ElementTree as ET


def parse_bold(text, text_cell_runlist):
    #create a list with 'SEGMENTS' of rich text
    segments = []
    for segment_idx in range(len(text_cell_runlist)):
        #find the beggining of the formatted text:
        #the loop find each tuple in text_cell_runlist and return the offset value
        #i.e.where bold or regular font starts
        start = text_cell_runlist[segment_idx][0]#segment_idx finds each tuple; [0] returns the value located in the first position of the tuple
        # the last segment starts at given 'start' and ends at the end of the string
        end = None

        #now find the end of the formatted text, which is actually the beginning of the next text
        if segment_idx != len(text_cell_runlist) - 1:
            end = text_cell_runlist[segment_idx + 1][0] #the end of the formatted text is the beginning of the next tuple, that's why the '+1'
     
        segment_text = start, end #text_cell[start:end] #these are the text segments mapped by text_cell_runlist
        #creates a dictionary that maps each text segment to the corresponding type of font
        segments.append({
            'text': segment_text,
            'font': book.font_list[text_cell_runlist[segment_idx][1]] #'1' represents the second value in the tuple, which is the 'font_index' value
                })
       
    # segments did not start at beginning, assume cell starts with text styled as the cell
    if text_cell_runlist[0][0] != 0:
        segments.insert(0, {
            'text': text_cell[:text_cell_runlist[0][0]],
            'font': book.font_list[text_cell_xf.font_index]
        })        
        
    # separating the segments that are bold, which are the cues    
    for segment in segments: 
        #creating a list for the segments
        cues = []
        #putting in the list the bold segments of text, also eliminating empty spaces that have bold format:
        if segment['font'].bold ==1 and segment['text'] !=' ':
            cues.append(segment['text'])
            return cues
            #print 'This is a cue: ', cues, '\n'
            
    
            
#set a function that finds Scope marks ('[' and ']')
def has_brackets(value):
    return '[' in value and']' in value
    
    #takes the element and replaces the "[ ]" marks with a new scope object ("ET.element")
def add_scope(element):

    #create the "Scope" object
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
    #append the scope to the element
    element.append(scope)
    #run the function that makes an object out of the "Cue" marks
    cueify(scope)
    

#function that creates a scope when it finds square brackets	
def scopify(element):
    if has_brackets(element.text):
        element = add_scope(element)
        

def cueify(element):
    if parse_bold(text_cell_runlist): 
        element = add_cue(element)
        
        
#takes the element and replaces the "+  +*" marks with a new cue object ("ET.element")
def add_cue(element):    
    cue = ET.Element("Cue")     
    cue_text = parse_bold(element.text) 
    left_c= element.text[: cue_text]
    tail_c = element.text[cue_text + 1:]
    # put together the sentence with cue marked
    cue.text = unicode(cue_text)
    cue.tail = unicode(tail_c)
    element.text = left_c
    
    if parse_bold(cue.tail):
        element.append(cue)
        add_cue_from_tail(previous_cue_parent=element, previous_cue=cue)
        
def add_cue_from_tail(previous_cue_parent, previous_cue):
    new_cue = ET.Element("Cue")

    cue_text = parse_bold(previous_cue.tail)

    left_c = previous_cue.tail[: cue_text]
    tail_c = previous_cue.tail[cue_text + 1:]
    previous_cue.tail = left_c

    new_cue.text = unicode(cue_text)
    new_cue.tail = tail_c
    previous_cue_parent.append(new_cue)
    if parse_bold(new_cue.tail):
        add_cue_from_tail(previous_cue_parent=previous_cue_parent, previous_cue=new_cue)




if __name__ == '__main__':
    #open a workbook
    book = xlrd.open_workbook('./finalcorpusconversion1.xls', formatting_info=True)
    ## IMPORTANT NOTE: formatting_info does not work with xlsx files  
    
    #using sheet_by_index to retrieve the firs sheet in the workbook
    first_sheet = book.sheet_by_index(0)
    
    #getting value from columns
    COL_IDXID = 0 #getting values from StrId column
    COL_IDXPRID = 1 #getting ProjId values
    COL_IDX = 2 # getting TwitterText values
    COL_LBL = 3 # getting Label values
    
    
    #create the corpus object
    corpus = ET.Element("Corpus")

    #define the object "Tweet"
    tweet = ET.Element("Tweet")
    
   
    
    # iterates over cells, retuns an XF class object for each cell
    for row_idx in range(first_sheet.nrows):
        
        #retrieves the 'str_id' cell value    
        text_cell_id = first_sheet.cell_value(row_idx, COL_IDXID)
        #gets the project id cell value
        text_cell_project_id = first_sheet.cell_value(row_idx, COL_IDXPRID)
    
        #get label value    
        text_cell_label = first_sheet.cell_value(row_idx, COL_LBL)      
        #gets the tweet_text value
        
        text_cell = first_sheet.cell_value(row_idx, COL_IDX)    
        #gets the tweet_text cell value
        #identifies cells that have special formatting, called extended formatting (XF)
        #cell_xf_index gives the XF index of the cell in the given row and column.
        #book.xf_list returns a list of XF class instances, each corresponding to an XF record.    
        text_cell_xf = book.xf_list[first_sheet.cell_xf_index(row_idx, COL_IDX)]     
          
        #identifies cells in multi-style format. For 'finalcorpusconversion1.xls, this is bold
        # DEFINITION OF rich_text_runlist_map (from https://media.readthedocs.org/pdf/xlrd/latest/xlrd.pdf):
        #rich_text_runlist_map = {}
        #Mapping of (rowx, colx) to list of (offset, font_index) tuples. The offset defines where in the string the font begins to be used. 
        #Offsets are expected to be in ascending order. If the first offset is not zero, the meaning is that the cell’s XF‘s font should be used from offset 0.
        #This is a sparse mapping. There is no entry for cells that are not formatted with rich text.
        #this mapping returns tuples like (45,3) and (67,0), where '45' represents the position where font type 3 starts
        #and '67' the position where font type 0 starts.
    
        #this is my tweet text to create objects from (excel_data in my former program)
        text_cell_runlist = first_sheet.rich_text_runlist_map.get((row_idx, COL_IDX))
        
    
        #print text_cell_runlist, text_cell, text_cell_id, text_cell_project_id

        
        
        element = None
        element = ET.Element("TweetText")
        element.text= text_cell         
        
        if text_cell_runlist:
            scopify(element)
            cueify(element)
    

        else:
            element.text = unicode(text_cell)
    tweet.append(element)
corpus.append(tweet)
    
tree = ET.ElementTree(corpus)
    
tree.write('full_tweets_xml.xml')
