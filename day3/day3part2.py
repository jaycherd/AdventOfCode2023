from icecream import ic
import re
from typing import Set,Optional,List

def find_prevandnext_sym_colnums(prev_line: str,next_line: str) -> Set[int]:
    res = set()
    i = 0
    for char in prev_line:
        if char == '*':
            res.add(i)
        i += 1
    i = 0
    for char in next_line:
        if char == '*':
            res.add(i)
        i += 1
    return res
    

"""for when you on first line, and have no prev line to check or last line, and there is no next line to check
opted to do this in its' own fxn so no check for prev and next line everytime the other is called as this
case only happens twice over many lines"""
def find_nextorprev_sym_colnums(prev_or_next_line: str) -> Set[int]:
    res = set()
    i = 0
    for char in prev_or_next_line:
        if char == '*':
            res.add(i)
        i += 1
    return res

def check_left_right_up_down(i: int, curr_line: List[str], above_line: Optional[List[str]] = None, below_line: Optional[List[str]] = None) -> int: #how many nums were found, if two nums, mul them and return res
    res = [] #append all the nums that we find, and if res is len(2) at end then mul them
    """example of what the below vars will mean
    a b c
    a * c
    a b c

    abc, represent all the possible ways to be connected to the *"""
    a,b,c = i-1, i, i+1
    ptr = -1
    #seen sets track, nums (columns) already visited and added to res
    above_line_seen,curr_line_seen,below_line_seen = set(),set(),set()
    if above_line is None: #if we are at top, then curr_line and below_line were passed
        ptr = -1
        if a >= 0 and below_line[a].isdigit():
            ptr = a
            while ptr > 0 and below_line[ptr-1].isdigit(): #get to the very beginning of this particular digit
                ptr -= 1
            #now we should be at the start, so process this num, and add the vals
            num = 0
            while ptr < len(below_line) and below_line[ptr].isdigit():
                num = num*10 + int(below_line[ptr])
                below_line_seen.add(ptr)
                ptr += 1
            res.append(num)
        if b not in below_line_seen and below_line[b].isdigit():
            ptr = b
            while ptr > 0 and below_line[ptr-1].isdigit():
                ptr -= 1
            #now we should be at the start of this num
            num = 0
            while ptr < len(below_line) and below_line[ptr].isdigit():
                num = num*10 + int(below_line[ptr])
                below_line_seen.add(ptr)
                ptr += 1
            res.append(num)
        if c not in below_line_seen and below_line[c].isdigit():
            ptr = c
            while ptr > 0 and below_line[ptr-1].isdigit():
                ptr -= 1
            #now we should be at the start of this num
            num = 0
            while ptr < len(below_line) and below_line[ptr].isdigit():
                num = num*10 + int(below_line[ptr])
                below_line_seen.add(ptr)
                ptr += 1
            res.append(num)
        ptr = -1
        if a >= 0 and curr_line[a].isdigit():
            ptr = a
            while ptr > 0 and curr_line[ptr-1].isdigit(): #get to the very beginning of this particular digit
                ptr -= 1
            #now we should be at the start, so process this num, and add the vals
            num = 0
            while ptr < len(curr_line) and curr_line[ptr].isdigit():
                num = num*10 + int(curr_line[ptr])
                curr_line_seen.add(ptr)
                ptr += 1
            res.append(num)
        if c not in curr_line_seen and curr_line[c].isdigit():
            ptr = c #no need to track to beginning, to right of asterisk, def beginning already
            #now we should be at the start of this num
            num = 0
            while ptr < len(curr_line) and curr_line[ptr].isdigit():
                num = num*10 + int(curr_line[ptr])
                curr_line_seen.add(ptr)
                ptr += 1
            res.append(num)
        ptr = -1
        if len(res) == 2:
            ic(res[0])
            ic(res[1])
            return res[0]*res[1]        

    elif below_line is None: #if we are at last line
        pass
    else:#for the rest of file, the meat
        ptr = -1
        if a >= 0 and above_line[a].isdigit():
            ptr = a
            while ptr > 0 and above_line[ptr-1].isdigit(): #get to the very beginning of this particular digit
                ptr -= 1
            #now we should be at the start, so process this num, and add the vals
            num = 0
            while ptr < len(above_line) and above_line[ptr].isdigit():
                num = num*10 + int(above_line[ptr])
                above_line_seen.add(ptr)
                ptr += 1
            res.append(num)
        if b not in above_line_seen and above_line[b].isdigit():
            ptr = b
            while ptr > 0 and above_line[ptr-1].isdigit():
                ptr -= 1
            #now we should be at the start of this num
            num = 0
            while ptr < len(above_line) and above_line[ptr].isdigit():
                num = num*10 + int(above_line[ptr])
                above_line_seen.add(ptr)
                ptr += 1
            res.append(num)
        if c not in above_line_seen and above_line[c].isdigit():
            ptr = c
            while ptr > 0 and above_line[ptr-1].isdigit():
                ptr -= 1
            #now we should be at the start of this num
            num = 0
            while ptr < len(above_line) and above_line[ptr].isdigit():
                num = num*10 + int(above_line[ptr])
                above_line_seen.add(ptr)
                ptr += 1
            res.append(num)
        ptr = -1
        if a >= 0 and below_line[a].isdigit():
            ptr = a
            while ptr > 0 and below_line[ptr-1].isdigit(): #get to the very beginning of this particular digit
                ptr -= 1
            #now we should be at the start, so process this num, and add the vals
            num = 0
            while ptr < len(below_line) and below_line[ptr].isdigit():
                num = num*10 + int(below_line[ptr])
                below_line_seen.add(ptr)
                ptr += 1
            res.append(num)
        if b not in below_line_seen and below_line[b].isdigit():
            ptr = b
            while ptr > 0 and below_line[ptr-1].isdigit():
                ptr -= 1
            #now we should be at the start of this num
            num = 0
            while ptr < len(below_line) and below_line[ptr].isdigit():
                num = num*10 + int(below_line[ptr])
                below_line_seen.add(ptr)
                ptr += 1
            res.append(num)
        if c not in below_line_seen and below_line[c].isdigit():
            ptr = c
            while ptr > 0 and below_line[ptr-1].isdigit():
                ptr -= 1
            #now we should be at the start of this num
            num = 0
            while ptr < len(below_line) and below_line[ptr].isdigit():
                num = num*10 + int(below_line[ptr])
                below_line_seen.add(ptr)
                ptr += 1
            res.append(num)
        ptr = -1
        if a >= 0 and curr_line[a].isdigit():
            ptr = a
            while ptr > 0 and curr_line[ptr-1].isdigit(): #get to the very beginning of this particular digit
                ptr -= 1
            #now we should be at the start, so process this num, and add the vals
            num = 0
            while ptr < len(curr_line) and curr_line[ptr].isdigit():
                num = num*10 + int(curr_line[ptr])
                curr_line_seen.add(ptr)
                ptr += 1
            res.append(num)
        if c not in curr_line_seen and curr_line[c].isdigit():
            ptr = c #no need to track to beginning, to right of asterisk, def beginning already
            #now we should be at the start of this num
            num = 0
            while ptr < len(curr_line) and curr_line[ptr].isdigit():
                num = num*10 + int(curr_line[ptr])
                curr_line_seen.add(ptr)
                ptr += 1
            res.append(num)
        ptr = -1
        if len(res) == 2:
            ic(res[0])
            ic(res[1])
            return res[0]*res[1]
    return 0



f_name = "day3input.txt"
sum_gear_ratios = 0
#dont think i can use the same logic, cus we need TWO nums that are adjacent to '*', thus we need to tie
#ea/num to the same '*' which we cant do with the logic from part 1, so maybe we process chars one by one,
#and if we see a '*' then we search every adjacent char and see if two nums are around it, could use a queue, and
#as we come across an adj num we add the num to queue and see if we find two nums, if we do, then pop them,
#and multiply them together then sum
"""so i could use similar logic, process the lines and as I process them, flag ea/num i come across with an id, as we process
if digits are a part of the same num then we give all those cols the same id, then while going through the line, if it is an ast.
then go around and see if two different id's are adj."""
"""new idea: a sliding window, convert the strings, to lists, have first second third, then we can easily check col nums of first,second,
and third, because they will be as a list, will use 's' to mark as seen, no s in the input, no alpha's actually so should work"""
try:
    with open(f_name,'r') as file:
        first,second = None,None
        for line in file:
            first,second = second,list(line.strip())
            if first is None:
                continue
            break
        i = 0
        while i < len(first):
            char = first[i]
            if char == '*': #then check everywhere around it
                sum_gear_ratios += check_left_right_up_down(i=i,below_line=second,curr_line=first)
            i += 1
        #note it is a list but joining to a string so its easier to see
        print(f"first: {''.join(first)}")
        print(f"secnd: {''.join(second)}")
        ic(sum_gear_ratios)

        file.seek(0)
        first,second,third = None,None,None
        for line in file:
            first,second,third = second,third,list(line.strip())
            if first is None or second is None:
                continue
            
            i = 0
            while i < len(second):
                char = second[i]
                if char == '*':
                    sum_gear_ratios += check_left_right_up_down(i=i,above_line=first,curr_line=second,below_line=third)
                i += 1
            print(f"first: {''.join(first)}")
            print(f"secnd: {''.join(second)}")
            print(f"third: {''.join(third)}")
            ic(sum_gear_ratios)



        exit()

except FileNotFoundError:
    print(f"file {f_name} not found")
    exit()



"""NOTE: got it working, but could be a lot cleaner with more functions because there is a lot of reusable code
also i didnt implement the last line cus there were no asterisk on the last line, there actually weren't any
on the first line either so that part didnt matter either"""