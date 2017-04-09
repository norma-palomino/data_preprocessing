# in another file, do 
# import get_cue_indexes from runlist_helper

PLAIN = 0
BOLD = 3
'''
takes a runlist and returns starts and ends of the cues
example:

runlist = [(0, 0), (81, 3), (87, 0), (98, 3), (104, 0)]
cue_indexes = [[81, 86], [98, 103]]

'''
def get_cue_indexes(runlist):
  # start with the first tuple that has a BOLD
  # create a list of cues
  # for each index and format type in the runlist:
  #   if we haven't started a cue, start a cue
  #   if we have started a cue, finish the cue, and add it to our list of cues
  # when done, return the list of cues


  found_first_cue = False
  cues = []
  
  start = None
  for index, format_type in runlist:
    if format_type is PLAIN and not found_first_cue:
      continue
    found_first_cue = True

    cue_is_started = start is not None

    if not cue_is_started:
      start = index
    else:
      end = index - 1 
      cues.append([start, end])
      start = None

  #print cues  
  return cues

runlist = [(0, 0), (81, 3), (87, 0), (98, 3), (104, 0)]
print get_cue_indexes(runlist)






# 0


# Segment text:   @AtheistRepublic not completely, but its relevancy will slowly wane until [it's 
# 1
# Segment text:  barely
# 2
# Segment text:   important 
# 3
# Segment text:  enough
# 4
# Segment text:   to consider.]