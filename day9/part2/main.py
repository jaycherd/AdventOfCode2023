from icecream import ic
import re
from typing import Set,Optional,List,Tuple,Dict,Deque
from time import perf_counter
from collections import deque
import math
from functools import reduce


def calc_next_val(rows: List[List[int]]) -> int:
    for row_i in range(len(rows)-2,-1,-1):
        rows[row_i].appendleft(rows[row_i][0] - rows[row_i+1][0])
    # print(rows)
    return rows[0][0]


def generate_rows(vals: Deque[int]) -> int:
    rows : List[Deque[int]] = [] #notice the deque for faster append left operation
    rows.append(vals)
    while True:
        j = len(rows[-1])
        tmp = deque()
        all_are_zero = True
        for i in range(j-1): #will reduce list by one each time
            diff = rows[-1][i+1]-rows[-1][i]
            if diff != 0:
                all_are_zero = False
            tmp.append(diff)
        rows.append(tmp)
        if all_are_zero:
            break
    # print(rows)
    res = calc_next_val(rows=rows)
    rows.clear()
    # ic(res)
    return res
        




if __name__ == "__main__":
    f_name = "../in.txt"
    next_val_sum = 0

    try:
        with open(f_name,'r') as file:
            for line in file:
                line = deque([int(x) for x in line.strip().split()])
                # print(line)
                next_val_sum += generate_rows(vals=line)
    except FileNotFoundError:
        print(f"file {f_name} not found")
    
    ic(next_val_sum)


"""
XXX MODIFICATION XXX
extrapolate for the first value instead, so to get value before a num, you do LEFTMOST num of the list, MINUS the value of the first value
of the list below, so changes = LEFTMOST AND MINUS

XXX IDEA XXX
almost want to do everything the exact same HOWEVER, appending to the front of the list should be time complexity of O(n) and we have to do that
operation times the number of rows, time the size of the input so O(n**3)? not so good, how about do it all the same but with a deque instead for 
the faster appendleft operation
"""