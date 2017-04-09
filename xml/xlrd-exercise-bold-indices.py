from __future__ import print_function
import xlrd

# coding='utf8'
# accessing Column 'C' ('tweet_text') in this example
COL_IDX = 2
COL_IDXID = 0

# open a workbook
book = xlrd.open_workbook('./finalcorpusconversion1.xls', formatting_info=True)

# find the first sheet in the workook
first_sheet = book.sheet_by_index(0)

# iterates over cells, retuns an XF class object for each cell
for row_idx in range(first_sheet.nrows):
    text_cell = first_sheet.cell_value(row_idx, COL_IDX).encode('utf-8')
    # retrieves the 'str_id' cell value
    text_cell_id = first_sheet.cell_value(row_idx, COL_IDXID)
    # get identify cells that have special formatting, called extended formatting (XF)
    # cell_xf_index gives the XF index of the cell in the given row and column.
    # book.xf_list returns a list of XF class instances, each corresponding to an XF record.
    text_cell_xf = book.xf_list[first_sheet.cell_xf_index(row_idx, COL_IDX)]

    # print('Str_id: ', text_cell_id + ' -- ' + 'Cell value: ', str(text_cell) + ' -- ' + 'XF object: ', text_cell_xf)

    # skip rows where cell is empty - I DON'T NEED THIS BECAUSE I DONT HAVE EMPTY CELLS
    # if not text_cell:
    # continue
    # print text_cell,


    # identifies cells in multi-style format. For 'finalcorpusconversion1.xls, this is bold
    # DEFINITION OF rich_text_runlist_map (from https://media.readthedocs.org/pdf/xlrd/latest/xlrd.pdf):
    # rich_text_runlist_map = {}
    # Mapping of (rowx, colx) to list of (offset, font_index) tuples. The offset defines where in the string the font begins to be used.
    # Offsets are expected to be in ascending order. If the first offset is not zero, the meaning is that the cell’s XF‘s font should be used from offset 0.
    # This is a sparse mapping. There is no entry for cells that are not formatted with rich text.
    # this mapping returns tuples like (45,3) and (67,0), where '45' represents the position where font type 3 starts
    # and '67' the position where font type 0 starts.
    text_cell_runlist = first_sheet.rich_text_runlist_map.get((row_idx, COL_IDX))
    # print("Text_cell_runlist values: ", text_cell_runlist)
    if text_cell_runlist:
        # print('(cell multi style) SEGMENTS:')
        # create a list with 'SEGMENTS' of rich text
        segments = []
        for segment_idx in range(len(text_cell_runlist)):
            # find the beggining of the formatted text:
            # the loop find each tuple in text_cell_runlist and return the offset value
            # i.e.where bold or regular font starts
            start = text_cell_runlist[segment_idx][
                0]  # segment_idx finds each tuple; [0] returns the value located in the first position of the tuple         # the last segment starts at given 'start' and ends at the end of the string
            end = None
            # print("Start: ", start)

            # now find the end of the formatted text, which is actually the beginning of the next text
            if segment_idx != len(text_cell_runlist) - 1:
                end = text_cell_runlist[segment_idx + 1][
                    0]  # the end of the formatted text is the beginning of the next tuple, that's why the '+1'
                # print("End: ", end)
            segment_text = start, end  # this are segments of formatted or non-formatted text
            # print 'Text segment position: ', segment_text
            # creates a dictionary that maps each text segment to the corresponding type of font
            segments.append({
                'indices': segment_text,
                'font': book.font_list[text_cell_runlist[segment_idx][1]]
                # '1' represents the second value in the tuple, which is the 'font_index' value
            })
            # print('Segment text indices: ', segment_text)
            # print('This is the dictionary of segments: ', segments)

        # segments did not start at beginning, assume cell starts with text styled as the cell
        if text_cell_runlist[0][0] != 0:
            segments.insert(0, {
                'indices': text_cell[:text_cell_runlist[0][0]],
                'font': book.font_list[text_cell_xf.font_index]
            })

        for segment in segments:
            # print "Cue: ", segment['text'],
            # print 'bold:', segment['font'].bold #if this returned value is 1, then use it as an object for the cue

            cues = []
            if segment['font'].bold == 1:
                cues.append(segment['indices'])
                print('These is a cue: ', cues)


                # else:
                # print '(cell single style)',
                # print 'bold:', book.font_list[text_cell_xf.font_index].bold

                # now I have to take the cues from this list and use them in the program that we developed with Max
