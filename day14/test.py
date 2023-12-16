from icecream import ic
from typing import List,Tuple,Dict,Counter,TypeVar,Generator
import numpy as np

cache = {}
num_cycles_target = 10 #1-indexed, aka 10th cycle
val_strs = ['x','a','b','c','a','b','c','a','b','c','a','b','c']
"""okay so obviously here, we have x which is not a part of the cycle that we find
repeats, so we are gonna want an algorithm that will look at this array find where the pattern
repeats, then use that to predict any value; lets say 10th item so 9th index, 
that is the 'c'
['x':0,'a':1,'b':2,'c':3]
"""
cycle_end,cycle_length = None,None
for i,val in enumerate(val_strs):
    if val not in cache:
        cache[val] = i
    else:
        cycle_end = i
        cycle_length = i - cache[val]
        ic(cycle_end,cycle_length)
        break

offset = cycle_end-cycle_length
index = ((num_cycles_target - 1 - offset)% cycle_length) + offset
ic(offset,index,num_cycles_target,cycle_length)
for val,num in cache.items():
    if num == index:
        ic(val)
print("this is the correct value")





