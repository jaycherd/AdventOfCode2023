from icecream import ic
import re
from typing import Set,Optional,List,Tuple

def clean_line(in_line: str) -> str:
    for i,char in enumerate(in_line):
        if char == ':':
            return in_line[i+1:]

def generate_winning_my_nums_lists(line: str) -> Tuple[List[int],List[int]]:
    winning_nums_str,mynums_str = line.split('|')
    #interesting trick below, if you dont specify " " as sep, it matches one OR more spaces rather than one
    winning_nums = winning_nums_str.split()
    mynums = mynums_str.split()
    for i,num in enumerate(winning_nums):
        winning_nums[i] = int(num)
    for i,num in enumerate(mynums):
        mynums[i] = int(num)
        
    return (winning_nums,mynums)

def calc_points(winners: List[int], nums: List[int]) -> int:
    points = 0
    winner_set = set(winners)
    for num in nums:
        if num in winner_set:
            if points == 0:
                points = 1
            else:
                points = points*2
            ic(num)
            ic(points)
    return points



f_name = "day4input.txt"
sum_points = 0

try:
    with open(f_name,'r') as file:
        for line in file:
            line = clean_line(in_line=line.strip())
            winning_nums,my_nums = generate_winning_my_nums_lists(line)
            sum_points += calc_points(winning_nums,my_nums)

            

            
            ic(line)
            print(winning_nums)
            print(my_nums)
        ic(sum_points)
            


except FileNotFoundError:
    print(f"file {f_name} not found")