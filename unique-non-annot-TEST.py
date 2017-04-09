

def compare_ids(list1, list2):
    #used_ids = []
    unused_ids = []
    for x in list2:
        if x not in list1:
            #used_ids.append(x)
        #else:
            unused_ids.append(x)
    return unused_ids

    
    
    
if __name__ == '__main__':
    
    list1 = ['banana', 'pera', 'pera', 'manzana', 'uva']
    list2 = ['banana', 'pera', 'oliva', 'manzana', 'damasco', 'aceituna']
    
    newids = compare_ids(list1,list2)
    print newids