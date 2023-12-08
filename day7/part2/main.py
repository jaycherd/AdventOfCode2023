from icecream import ic
import re
from typing import Set,Optional,List,Tuple,Dict
from time import perf_counter

def is_better_card(card_a: str, card_b: str) -> bool:
    a_rank,b_rank = 0,0
    if card_a in letter_map:
        a_rank = letter_map[card_a]
    else:
        a_rank = int(card_a)
    if card_b in letter_map:
        b_rank = letter_map[card_b]
    else:
        b_rank = int(card_b)
    return a_rank > b_rank


def get_ranktype_as_int(occurrences: Dict[str,int],num_jokers: int) -> int:
    """rtype: int, where:
    7 = five kind = strongest
    6 = four kind
    5 = full house
    4 = three kind
    3 = two pair
    2 = one pair
    1 = high card"""
    ## remem. check edge case all J, otherwise changing j for the next highest card should result in best possible type?
    ## note: dont need any of this extra stuff if 'J' not even a card in the hand, so check that
    if 'J' in occurrences:
        max_card_not_joker,max_occ_not_joker = None,0
        for card,count in occurrences.items():
            if card == 'J':
                continue
            if count > max_occ_not_joker:
                max_card_not_joker = card
                max_occ_not_joker = count
            elif count == max_occ_not_joker and is_better_card(card,max_card_not_joker): # J may change, if two diff types of pairs, take the pair which is the best card strength, same for if we have all single cards and some Jokers
                max_card_not_joker = card
                max_occ_not_joker = count
        if not max_card_not_joker:
            return 7 #this would only happen if 'J' is only card, meaning that we have five Jokers
        occurrences[max_card_not_joker] += num_jokers
        occurrences['J'] = 0 #dont need to check if in map, did that earlier before the adjustments
    
    #now we can do the normal ranking function, our hand has been adjusted to account for any Jokers
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
    num_jokers = 0
    for card in hand:
        if card in occurrences:
            occurrences[card] += 1
        else:
            occurrences[card] = 1
        if card in letter_map:
            ranks_tie.append(letter_map[card])
            if card == 'J':
                num_jokers += 1
        else:
            ranks_tie.append(int(card))
    rank_type = get_ranktype_as_int(occurrences=occurrences,num_jokers=num_jokers)
    return (rank_type,ranks_tie)


if __name__ == '__main__':
    f_name = "in.txt"
    total_winnings = 0
    letter_map = {'T':10,'J':1,'Q':12,'K':13,'A':14} #update joker to lowest individual rank
    """hands represented as Tuple --> (type_rank, [card1_strength,...,card5_strength], bid)"""
    hands_tuple : Tuple[int,List[int],int] = () #last int is just the bid number to get solution later
    hands_unordered : List[Tuple[int,List[int],int]] = []  #list containing the hands
    hands_ordered : List[Tuple[int,List[int],int]] = []    #list containing hands sorted
    
    try:
        with open(f_name,'r') as file:
            line_num = 0
            for line in file:
               hand,bid = line.strip().split()
               rank_type,ranks_tie = get_ranks(list(hand))
               bid = int(bid)
               hands_tuple = (rank_type,ranks_tie,bid)
               hands_unordered.append(hands_tuple)
               line_num += 1
                
            #    ic(line.strip())
            #    ic(hands_tuple)
            #    if line_num == 4:
            #        exit()

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
XXX Part TWO modifications XXX
J = Joker --> wildcards that act as whatever card would make the hand the strongest, but on their own they are considered the weakest
that is, QJJQ2 = 4 of a kind, Jokers act as Q, but during tie break J = 1, aka lower rank even than 2, so for example
JKKK2 is weaker than QQQQ2 because both make four of a kind, but the J during tie break loses to Q

XXX idea XXX
do things the same way, but to handle the jokers, lets track the number of them, then when finding out the type, 
we see whatever the best pair we had, if we had 3 of a kind, and 2 jokers, then the best type we had was 3 of a kind, add two aka two jokers,
then best we have now is 5 of a kind, cool
so i think only thing we change is map 'j' --> 1 aka lowest rank, and also track num Jokers for our type calculation, which will also be altered

"""