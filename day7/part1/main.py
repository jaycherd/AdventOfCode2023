from icecream import ic
import re
from typing import Set,Optional,List,Tuple,Dict
from time import perf_counter

def get_ranktype_as_int(occurrences: Dict[str,int]) -> int:
    """rtype: int, where:
    7 = five kind = strongest
    6 = four kind
    5 = full house
    4 = three kind
    3 = two pair
    2 = one pair
    1 = high card"""
    three_kind = False
    num_pairs = 0
    for count in occurrences.values():
        if count == 5:
            return 7
        if count == 4:
            return 6
        if count == 3:
            three_kind = True
            continue
        if count == 2:
            num_pairs += 1
    if three_kind:
        if num_pairs == 1:
            return 5
        return 4
    if num_pairs == 2:
        return 3
    if num_pairs == 1:
        return 2
    return 1



def get_ranks(hand: List[str]) -> Tuple[int,List[int]]:
    occurrences = {}
    ranks_tie = []
    rank_type = -1
    for card in hand:
        if card in occurrences:
            occurrences[card] += 1
        else:
            occurrences[card] = 1
        if card in letter_map:
            ranks_tie.append(letter_map[card])
        else:
            ranks_tie.append(int(card))
    rank_type = get_ranktype_as_int(occurrences=occurrences)
    return (rank_type,ranks_tie)


if __name__ == '__main__':
    f_name = "in.txt"
    total_winnings = 0
    letter_map = {'T':10,'J':11,'Q':12,'K':13,'A':14}
    hands_tuple : Tuple[int,List[int],int] = () #last int is just the bid number to get solution later
    hands_unordered : List[Tuple[int,List[int],int]] = []  #list containing the hands
    hands_ordered : List[Tuple[int,List[int],int]] = []    #list containing hands sorted
    
    try:
        with open(f_name,'r') as file:
            for line in file:
               hand,bid = line.strip().split()
               rank_type,ranks_tie = get_ranks(list(hand))
               bid = int(bid)
               hands_tuple = (rank_type,ranks_tie,bid)
               hands_unordered.append(hands_tuple)
            #    ic(line.strip())
            #    ic(hands_tuple)
            #    exit()

    except FileNotFoundError:
        print(f"file {f_name} not found")

    #order hands from weakest to strongest
    hands_ordered = sorted(hands_unordered, key=lambda V: (V[0],V[1][0],V[1][1],V[1][2],V[1][3],V[1][4]))
    for zero_index,hand in enumerate(hands_ordered):
        ranking = zero_index + 1
        total_winnings += (ranking*hand[2])

    ic(hands_ordered)
    ic(total_winnings)




"""
XXX DESCRIPTION XXX
In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. 
A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. 
The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456

If two hands have the same type, a second ordering rule takes effect. 
Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. 
If the first card in each hand have the same label, however, then move on to considering the second card in each hand. 
If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

This example shows five hands; each hand is followed by its bid amount. 
Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, 
and so on up to the strongest hand. 
Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid
 with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5).
 So the total winnings in this example are 6440.

XXX GOAL XXX
add up total winnings, by sum(rank*bid)

XXX IDEAS XXX
* each hand is something like "T6782 898"
* what we could do is create a tuple[int,int] where its like [ranktype,ranktiebreak], but if the first char is a tie you have to go
    to the second char, so on second thought, we could do tuple[int,List[int]], where first int is the ranktype because that takes the priority,
    and the second is a list of tiebreak chars, so for example if we had "T6782 898" then we'd have type high card, so thats the lowest rank possible of type
    and the tie breakers would be [t=10,6=6,etc.] bcs ranking is A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2, where A = highest pri, so we'll say it gets
    a value of 1, so when we sort by them A comes before, note although we start at 2 we can simplify our life and just use the actual chars as the int, unless
    it is a letter then convert it

"""