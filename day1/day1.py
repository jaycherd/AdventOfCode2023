from icecream import ic
from typing import Tuple,Optional

def is_numword_fromleft(index: int, line: str) -> Optional[int]: #None if not a number, but returns the num if it is
    rbound = len(line)
    if line[index] == 'o':
        index += 1
        if index < rbound and line[index] == 'n':
            index += 1
            if index < rbound and line[index] == 'e':
                return 1
    elif line[index] == 't':
        index += 1
        if index < rbound and line[index] == 'w':
            index += 1
            if index < rbound and line[index] == 'o':
                return 2
        elif index < rbound and line[index] == 'h':
            index += 1
            if index < rbound and line[index] == 'r':
                index += 1
                if index < rbound and line[index] == 'e':
                    index += 1
                    if index < rbound and line[index] == 'e':
                        return 3
    elif line[index] == 'f':
        index += 1
        if index < rbound and line[index] == 'o':
            index += 1
            if index < rbound and line[index] == 'u':
                index += 1
                if index < rbound and line[index] == 'r':
                    return 4
        elif index < rbound and line[index] == 'i':
            index += 1
            if index < rbound and line[index] == 'v':
                index += 1
                if index < rbound and line[index] == 'e':
                    return 5
    elif line[index] == 's':
        index += 1
        if index < rbound and line[index] == 'i':
            index += 1
            if index < rbound and line[index] == 'x':
                return 6
        elif index < rbound and line[index] == 'e':
            index += 1
            if index < rbound and line[index] == 'v':
                index += 1
                if index < rbound and line[index] == 'e':
                    index += 1
                    if index < rbound and line[index] == 'n':
                        return 7
    elif line[index] == 'e':
        index += 1
        if index < rbound and line[index] == 'i':
            index += 1
            if index < rbound and line[index] == 'g':
                index += 1
                if index < rbound and line[index] == 'h':
                    index += 1
                    if index < rbound and line[index] == 't':
                        return 8
    elif line[index] == 'n':
        index += 1
        if index < rbound and line[index] == 'i':
            index += 1
            if index < rbound and line[index] == 'n':
                index += 1
                if index < rbound and line[index] == 'e':
                    return 9
    return None

def is_numword_fromright(index: int, line: str) -> Optional[int]: #None if not a number, but returns the num if it is
    if line[index] == 'e':
        index -= 1
        if index >= 0 and line[index] == 'n':
            index -= 1
            if index >= 0 and line[index] == 'o':
                return 1
            elif index >= 0 and line[index] == 'i':
                index -= 1
                if index >= 0 and line[index] == 'n':
                    return 9
        elif index >= 0 and line[index] == 'e':
            index -= 1
            if index >= 0 and line[index] == 'r':
                index -= 1
                if index >= 0 and line[index] == 'h':
                    index -= 1
                    if index >= 0 and line[index] == 't':
                        return 3
        elif index >= 0 and line[index] == 'v':
            index -= 1
            if index >= 0 and line[index] == 'i':
                index -= 1
                if index >= 0 and line[index] == 'f':
                    return 5
    elif line[index] == 'o':
        index -= 1
        if index >= 0 and line[index] == 'w':
            index -= 1
            if index >= 0 and line[index] == 't':
                return 2
    elif line[index] == 'r':
        index -= 1
        if index >= 0 and line[index] == 'u':
            index -= 1
            if index >= 0 and line[index] == 'o':
                index -= 1
                if index >= 0 and line[index] == 'f':
                    return 4
    elif line[index] == 'x':
        index -= 1
        if index >= 0 and line[index] == 'i':
            index -= 1
            if index >= 0 and line[index] == 's':
                return 6
    elif index >= 0 and line[index] == 'n':
        index -= 1
        if index >= 0 and line[index] == 'e':
            index -= 1
            if index >= 0 and line[index] == 'v':
                index -= 1
                if index >= 0 and line[index] == 'e':
                    index -= 1
                    if index >= 0 and line[index] == 's':
                        return 7
    elif line[index] == 't':
        index -= 1
        if index >= 0 and line[index] == 'h':
            index -= 1
            if index >= 0 and line[index] == 'g':
                index -= 1
                if index >= 0 and line[index] == 'i':
                    index -= 1
                    if index >= 0 and line[index] == 'e':
                        return 8
    return None


def find_lft_rt_and_combine(line: str) -> int:
    l,r = 0,len(line)-1
    while not line[l].isdigit():
        l += 1
    l = int(line[l])
    while not line[r].isdigit():
        r -= 1
    r = int(line[r])
    return r + l*10

# #test all nums
# numsaswords = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
# for numberword in numsaswords:
#     ri = len(numberword)-1
#     fromleft = is_numword_fromleft(0,numberword)
#     fromright = is_numword_fromright(ri,numberword)
#     ic(numberword)
#     ic(fromleft)
#     ic(fromright)
# exit()



starting_ending_set = {'o','t','f','s','e','n','r','x'}
filepath = "day1input.txt"
sum = 0
try:
    with open(filepath,'r') as file:
        num = 0
        for line in file:
            line = line.strip()
            num += 1
            l,r = 0,len(line)-1
            word_fromleft_found = False
            while not line[l].isdigit():
                if line[l] in starting_ending_set:
                    res = is_numword_fromleft(l,line)
                    if res:
                        word_fromleft_found = True
                        l = res
                        break
                l += 1
            if not word_fromleft_found:
                l = int(line[l])

            word_fromright_found = False
            while not line[r].isdigit():
                if line[r] in starting_ending_set:
                    res = is_numword_fromright(r,line)
                    if res:
                        word_fromright_found = True
                        r = res
                        break
                r -= 1
            if not word_fromright_found:
                r = int(line[r])

            ic(sum)
            sum += r + l*10
except FileNotFoundError:
    print(f"File {filepath} not found")

ic(sum)
