import xlrd



def parse_bold(text_cell_runlist):
    segments = []
    for segment_idx in range(len(text_cell_runlist)):
        #find the beggining of the formatted text:
        #the loop find each tuple in text_cell_runlist and return the offset value
        #i.e.where bold or regular font starts
        start = text_cell_runlist[segment_idx][0]#segment_idx finds each tuple; [0] returns the value located in the first position of the tuple         # the last segment starts at given 'start' and ends at the end of the string
        end = None
        
        #now find the end of the formatted text, which is actually the beginning of the next text
        if segment_idx != len(text_cell_runlist) - 1:
            end = text_cell_runlist[segment_idx + 1][0] #the end of the formatted text is the beginning of the next tuple, that's why the '+1'
        segment_text = text_cell[start:end] #this is the wanted text
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
            #print 'This is a cue: ', cues

