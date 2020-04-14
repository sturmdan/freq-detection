'''
class autoCorr :
    
    
    var_test = 1
    
    def __init__(self, name):
        self.name = name
'''      
        
        
        
        
        
import numpy as np
#hi = np.array([1, 2, 3, 4, 5])
hi_array = [1, 2, 3, 4, 5]
hi_not_array = 4

hi_array_not_define = 0

def test_1():
    #print(hi_array)
    #print(hi_not_array)
    
    hi_array[3] += 2
    #hi_not_array += 1  
    


def test_2():
    #print(hi_array)
    #print(hi_not_array)
    
    hi_array[3] += 2
    global hi_not_array
    hi_not_array += 1    
    
    global hi_array_not_define
    hi_array_not_define = np.array([1, 2, 3, 4, 5])
    
    
    
### conclusion of tests
    
'''
lets say we have two files, A and B. i can put some global variables in B, have a function 
that uses them, and then call this function in A

this is sufficient for the autocorr function

i can also make an object for the autocorr function

the latter is probably better in case i want to have multiple instances

the former is probably better for providing something closer to C code

for that reason i will go with the former approach 

if i need to, changing it all to an OO system shouldn't be too hard 
'''

'''
actually though, it turns out accessing global variables in python can get a little dicey
it assumes that you are trying to use a local variable 

will this be an issue?
hopefully not too bad, especially since i will be using a lot of arrays which tend 

not to be too bad
'''


''' 
actually, i'm going to use an OO approach

it's nicer, and easier for others to use

and i don't need to be modeling C perfectly here

'''