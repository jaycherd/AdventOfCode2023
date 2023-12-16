from typing import Dict,List,Tuple
from itertools import combinations
from icecream import ic

def calc_line_arrangements(form1: List[str], form2: List[str]) -> int:
    for i in range(len(form1)):
        
    for i in range(len(form1),-1,-1):
        pass




if __name__ == "__main__":
    f_name = "../test.txt"
    arrangements = 0

    try:
        with open(f_name, 'r') as file:
            for line in (line.rstrip().split() for line in file):
                format1,format2 = list(line[0]),line[1].split(',')
                arrangements += calc_line_arrangements(format1,format2)
                ic(line)
                ic(format1,format2)
                exit()
    except FileNotFoundError:
        print(f"file {f_name} not found")

"""
operational = '.'
damaged = '#'
unkown = '?'
and the nums account for how many damaged there are, contiguous damaged, 

return the sum of all possible differnent arrangements
ie
???.### 1,1,3 - 1 arrangement --> ??? can only make "1.1" because of the 1,1,3 list at the end
.??..??...?##. 1,1,3 - 4 arrangements
?#?#?#?#?#?#?#? 1,3,1,6 - 1 arrangement
????.#...#... 4,1,1 - 1 arrangement
????.######..#####. 1,6,5 - 4 arrangements
?###???????? 3,2,1 - 10 arrangements

"""