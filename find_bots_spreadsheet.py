from openpyxl import load_workbook

from collections import defaultdict

from operator import itemgetter



def compare_projids(listofdics):
    output = defaultdict(list)
    for item in listofdics:
        output[item.get('StrId')].append(item.get('ProjId'))
        dict(output)
    return output