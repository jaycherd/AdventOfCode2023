from icecream import ic
import re
from typing import Set,Optional,List,Tuple,Dict
from time import perf_counter
from collections import deque
import math
from functools import reduce


def calc_next_val(rows: List[List[int]]) -> int:
    for row_i in range(len(rows)-2,-1,-1):
        rows[row_i].append(rows[row_i][-1] + rows[row_i+1][-1])
    # print(rows)
    return rows[0][-1]


def generate_rows(vals: List[int]) -> int:
    rows : List[List[int]] = []
    rows.append(vals)
    while True:
        j = len(rows[-1])
        tmp = []
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
                line = [int(x) for x in line.strip().split()]
                # print(line)
                next_val_sum += generate_rows(vals=line)
    except FileNotFoundError:
        print(f"file {f_name} not found")
    
    ic(next_val_sum)


"""
XXX DESCRIPTION XXX
each line in the report contains the history of a single value
* start by making new sequence from difference at each step
* do that until difference is ALL zeroes
* then work your way back up, to determine last num in history, do that num + the next sequence last num

EX: if we start with line:
0 3 6 9 12 15
then the process of working towards all zeroes would look like:, adding first line again just for visual
0 3 6 9 12 15
 3 3 3 3  3  
  0 0 0 0
so that third line aka we do differences twice, we have ALL zeroes, now we have to work our way up, calc A and B, note
how many we calc depends on how many lines it took to get to all zeroes
0 3 6 9 12 15 B
 3 3 3 3  3 A  
  0 0 0 0  X=0
first is X, X is gonna be zero no matter what
next to calc A, we make the result of increasing val to left 3 by val below X=0, aka the last one we did, X = 3
0 3 6 9 12 15 B
 3 3 3 3  3 A=3  
  0 0 0 0  X=0
last for B, we need to figure out same, what is result of incrs val to left (15) by val below (A=3) = 18

XXX GOAL XXX
do that process and add together all the next values, aka last values in the line that we must fig out, return sum,
note the only next value we care about is the original line, not all that in between computations we had to do

XXX IDEA XXX
read a line, do all the calcs, return next val add that to the sum, continue to next line to end of file
"""