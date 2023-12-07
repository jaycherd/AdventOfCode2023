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

def calc_copies(winners: List[int], nums: List[int]) -> int:
    copies = 0
    winner_set = set(winners)
    for num in nums:
        if num in winner_set:
            ic(num)
            copies += 1
    ic(copies)
    return copies



f_name = "day4input.txt"
sum_scratchcards = 0
card_id = 0
current_copies_accumulated = 0
card_copy_count = []


try:
    with open(f_name,'r') as file:
        line_count = 0
        for line in file:
            line_count += 1
        card_copy_count = [0]*line_count
        print(card_copy_count)
        file.seek(0)

        
        for line in file:
            card_copies = 0
            line = clean_line(in_line=line.strip())
            winning_nums,my_nums = generate_winning_my_nums_lists(line)
            card_copies += calc_copies(winning_nums,my_nums)
            #num points equal num of copies to make of next cards
            for i in range(card_id+1,card_id + card_copies+1):
                ic(i)
                ic(card_id)
                if card_copy_count[card_id] > 0:
                    card_copy_count[i] += card_copy_count[card_id]+1
                else:
                    card_copy_count[i] += 1
            sum_scratchcards += (1 + card_copy_count[card_id])




            card_id += 1
            

            
            ic(line)
            print(card_copy_count)
            print(winning_nums)
            print(my_nums)
            # exit()
        ic(sum_scratchcards)
            


except FileNotFoundError:
    print(f"file {f_name} not found")



"""new rules
Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. So, if card 10 were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.

Copies of scratchcards are scored like normal scratchcards and have the same card number as the card they copied. 
So, if you win a copy of card 10 and it has 5 matching numbers, 
it would then win a copy of the same cards that the original card 10 won: cards 11, 12, 13, 14, and 15. 
This process repeats until none of the copies cause you to win any more cards. 
(Cards will never make you copy a card past the end of the table.)"""