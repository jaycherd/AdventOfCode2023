from icecream import ic
import re
from typing import Set,Optional

def find_prevandnext_sym_colnums(prev_line: str,next_line: str) -> Set[int]:
    res = set()
    i = 0
    for char in prev_line:
        if not char.isdigit() and char != '.':
            res.add(i)
        i += 1
    i = 0
    for char in next_line:
        if not char.isdigit() and char != '.':
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
        if not char.isdigit() and char != '.':
            res.add(i)
        i += 1

f_name = "day3input.txt"
sum_partnums = 0


try:
    with open(f_name,'r') as file:
        #lets find out how many lines there are
        count_lines = 0
        for line in file:
            count_lines += 1
        file.seek(0)

        line_num = 0
        prev = ""
        add_num_flag = False
        for tmp_line in file:
            tmp_line = tmp_line.strip()
            if line_num == 0:
                prev = tmp_line
                continue
            next = tmp_line
            if line_num == 1:
                #lets figure out sym cols for the first line aka line 0
                sym_colnums_set = find_nextorprev_sym_colnums(next)
                i = 0
                while i < len(prev):
                    char = prev[i]
                    add_num_flag = False
                    if char != '.' and not char.isdigit():
                        add_num_flag = True
                    elif char.isdigit():
                        #consume all the digits, then check if we can add it
                        num = 0
                        while i < len(prev):
                            char = prev[i]
                            if char.isdigit():
                                if add_num_flag or i-1 in sym_colnums_set or i+1 in sym_colnums_set:
                                    add_num_flag = True
                                num = num*10 + int(char)
                                i += 1
                            else:
                                if char != '.':
                                    add_num_flag = True
                                i -= 1
                                break
                        #alright now we have a num, and we must check, whether it should be added
                        if add_num_flag:
                            sum_partnums += num
                    i += 1
            elif line_num == count_lines-1: #check if its the last num
                #lets figure out sym cols for the first line aka line 0
                sym_colnums_set = find_nextorprev_sym_colnums(next)
                i = 0
                while i < len(prev):
                    char = prev[i]
                    add_num_flag = False
                    if char != '.' and not char.isdigit():
                        add_num_flag = True
                    elif char.isdigit():
                        #consume all the digits, then check if we can add it
                        num = 0
                        while i < len(prev):
                            char = prev[i]
                            if char.isdigit():
                                if add_num_flag or i-1 in sym_colnums_set or i+1 in sym_colnums_set:
                                    add_num_flag = True
                                num = num*10 + int(char)
                                i += 1
                            else:
                                if char != '.':
                                    add_num_flag = True
                                i -= 1
                                break
                        #alright now we have a num, and we must check, whether it should be added
                        if add_num_flag:
                            sum_partnums += num
                    i += 1
            


            
            ic(line)
            exit()

except FileNotFoundError:
    print(f"file {f_name} not found")
    exit()