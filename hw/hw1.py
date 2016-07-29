#1. spirit of code taken from quick sort section of: http://danishmujeeb.com/blog/2014/01/basic-sorting-algorithms-implemented-in-python
def sortwithloops(input):
    """ Implementation of quick sort """
    if len(input) > 1:
        pivot_index = len(input) / 2
        smaller_items = []
        larger_items = []

        for i, val in enumerate(input):
            if i != pivot_index:
                if val < input[pivot_index]:
                    smaller_items.append(val)
                else:
                    larger_items.append(val)

        sortwithloops(smaller_items)
        sortwithloops(larger_items)
        input[:] = smaller_items + [input[pivot_index]] + larger_items
    return input
    
#2. https://wiki.python.org/moin/HowTo/Sorting
def sortwithoutloops(input): 
    return sorted(input)

#3. loop to find the specified value in the input list
def searchwithloops(input, value):
    if len(input) > 0:
        for i, val in enumerate(input):
            if value == val:
				return True
    return False

#4. just use the python "in" keyword
def searchwithoutloops(input, value):
    return value in input

if __name__ == "__main__":	
    L = [5,3,6,3,13,5,6]	

    print sortwithloops(L) # [3, 3, 5, 5, 6, 6, 13]
    print sortwithoutloops(L) # [3, 3, 5, 5, 6, 6, 13]
    print searchwithloops(L, 5) #true
    print searchwithloops(L, 11) #false
    print searchwithoutloops(L, 5) #true
    print searchwithoutloops(L, 11) #false
