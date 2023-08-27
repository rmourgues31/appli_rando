def flatten_list_of_list(lists: list[list]) -> list:
    '''
    Return an unique list for a list of lists
    '''
    #return list(chain(*lists))
    return [item for sublist in lists for item in sublist]

def reverse_list_in_list(x: list[list]) -> list[list]:
    '''
    Reverse the items of sublists
    '''
    return [l[::-1] for l in x]
