import xlrd

# accessing  the StrId and ProjectId columns as well
COL_IDXID = 0
COL_IDXPRID = 1

# accessing Column 'C' ('tweet_text') in this example
COL_IDX = 2


#oen a workbook
book = xlrd.open_workbook('./finalcorpusconversion1.xls', formatting_info=True)
## IMPORTANT NOTE: formatting_info does not work with xlsx files

#using sheet_by_index to retrieve the firs sheet in the workbook
first_sheet = book.sheet_by_index(0)

# iterates over cells, retuns an XF class object for each cell
for row_idx in range(first_sheet.nrows):
    text_cell = first_sheet.cell_value(row_idx, COL_IDX)
    #retrieves the 'str_id' cell value
    text_cell_id = first_sheet.cell_value(row_idx, COL_IDXID)
    #gets the project id cell value
    text_cell_project_id = first_sheet.cell_value(row_idx, COL_IDXPRID)
    #get identify cells that have special formatting, called extended formatting (XF)
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
    text_cell_runlist = first_sheet.rich_text_runlist_map.get((row_idx, COL_IDX))
    if text_cell_runlist:
        print 'This is the output from text_cell_runlist: ', text_cell_runlist, '\n'
            
            
        #create a list with 'SEGMENTS' of rich text
        segments = []
        for segment_idx in range(len(text_cell_runlist)):
            #find the beggining of the formatted text:
            #the loop find each tuple in text_cell_runlist and return the offset value
            #i.e.where bold or regular font starts
            start = text_cell_runlist[segment_idx][0]#segment_idx finds each tuple; [0] returns the value located in the first position of the tuple
            # the last segment starts at given 'start' and ends at the end of the string
            end = None
            print start
            print end
            #now find the end of the formatted text, which is actually the beginning of the next text
            if segment_idx != len(text_cell_runlist) - 1:
                end = text_cell_runlist[segment_idx + 1][0] #the end of the formatted text is the beginning of the next tuple, that's why the '+1'
                print end        
            segment_text = text_cell[start:end] #this is the wanted text
            #creates a dictionary that maps each text segment to the corresponding type of font
            segments.append({
                'text': segment_text,
                'font': book.font_list[text_cell_runlist[segment_idx][1]] #'1' represents the second value in the tuple, which is the 'font_index' value
                    })
        #print 'This is segment_text: ', segment_text
        print 'This is segments: ', segments     
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
                print 'This is a cue: ', cues, '\n'
    
        

    