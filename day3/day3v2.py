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
    return res

f_name = "day3input.txt"
sum_partnums = 0


try:
    with open(f_name,'r') as file:
        #lets find out how many lines there are
        count_lines = 0
        for line in file:
            count_lines += 1
        file.seek(0)

        #special cases first line and last line, so we can do the first one, seek to last do that, then do all tweeners
        i = 0
        #do first line, need first and second line
        first,second = "",""
        for line in file:
            if i == 0:
                first = line.strip()
            else:
                second = line.strip()
                break
            i += 1
        sym_colnums_set = find_nextorprev_sym_colnums(second)
        i = 0
        add_num_flag = False
        while i < len(first):
            char = first[i]
            if char != '.' and not char.isdigit():
                add_num_flag = True
            elif char.isdigit():
                #consume all the digits, then check if we can add it
                num = 0
                while i < len(first):
                    char = first[i]
                    if char.isdigit():
                        if add_num_flag or i in sym_colnums_set or i-1 in sym_colnums_set or i+1 in sym_colnums_set:
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
                    ic(num)
            else:
                add_num_flag = False
            i += 1
        print(first)
        print(second)
        ic(sum_partnums)

        #next lets do the middle lines aka all except first and last
        file.seek(0)
        first,second,third = None,None,None
        for line in file:
            first,second,third = second,third,line.strip()
            if first is None or second is None:
                continue
            sym_colnums_set = find_prevandnext_sym_colnums(prev_line=first,next_line=third)
            i = 0
            add_num_flag = False
            while i < len(second):
                char = second[i]
                if char != '.' and not char.isdigit():
                    add_num_flag = True
                elif char.isdigit():
                    #consume all the digits, then check if we can add it
                    num = 0
                    while i < len(second):
                        char = second[i]
                        if char.isdigit():
                            if add_num_flag or i in sym_colnums_set or i-1 in sym_colnums_set or i+1 in sym_colnums_set:
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
                        ic(num)
                else:
                    add_num_flag = False
                i += 1
            print(f"first: {first}")
            print(f"secnd: {second}")
            print(f"third: {third}")
            ic(sum_partnums)
        
        #lets process the last line
        sym_colnums_set = find_nextorprev_sym_colnums(second) #in this case its prev, cus third is last line now
        i = 0
        add_num_flag = False
        while i < len(third):
            char = third[i]
            if char != '.' and not char.isdigit():
                add_num_flag = True
            elif char.isdigit():
                #consume all the digits, then check if we can add it
                num = 0
                while i < len(third):
                    char = third[i]
                    if char.isdigit():
                        if add_num_flag or i in sym_colnums_set or i-1 in sym_colnums_set or i+1 in sym_colnums_set:
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
                    ic(num)
            else:
                add_num_flag = False
            i += 1

        print(f"first: {first}")
        print(f"secnd: {second}")
        print(f"third: {third}")
        ic(sum_partnums)


except FileNotFoundError:
    print(f"file {f_name} not found")
    exit()