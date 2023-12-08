from icecream import ic
from typing import Dict

def get_ranktype_as_int(occurrences: Dict[str,int],num_jokers: int) -> int:
    """rtype: int, where:
    7 = five kind = strongest
    6 = four kind
    5 = full house
    4 = three kind
    3 = two pair
    2 = one pair
    1 = high card"""
    best_rank_wout_jokers = 1
    num_pairs_wout_jokers = 0
    best_rank_with_jokers = 1 #with jokers ONLY being considered
    num_pairs_with_jokers = 0
    for card,count in occurrences.items():
        if count == 5:
            return 7
        if card == 'J':
            continue
        if count == 4:
            best_rank_wout_jokers = 6
        if count == 3:
            best_rank_wout_jokers = max(best_rank_wout_jokers,4)
        if count == 2:
            num_pairs_wout_jokers += 1
    if best_rank_wout_jokers == 4:
        if num_pairs_wout_jokers == 1:
            best_rank_wout_jokers = 5
    if num_pairs_wout_jokers == 2:
        best_rank_wout_jokers = 3
    if num_pairs_wout_jokers == 1:
        best_rank_wout_jokers = max(best_rank_wout_jokers,2)
    #if none of those then best rank will be one, aka high card

    #next look at hand including the jokers
    for card,count in occurrences.items():
        if card != 'J':
            continue
        if count == 4:
            best_rank_with_jokers = 6
        if count == 3:
            best_rank_with_jokers = max(best_rank_with_jokers,4)
        if count == 2:
            num_pairs_with_jokers += 1
    if best_rank_with_jokers == 4:
        if num_pairs_with_jokers == 1:
            best_rank_with_jokers = 5
    if num_pairs_with_jokers == 2:
        best_rank_with_jokers = 3
    if num_pairs_with_jokers == 1:
        best_rank_with_jokers = max(best_rank_with_jokers,2)
    
    ic(best_rank_with_jokers,best_rank_wout_jokers,num_jokers)
    return max(best_rank_wout_jokers + num_jokers, best_rank_with_jokers)






if __name__ == '__main__':


    occurrences = {'K':3,'J':2}
    rank = get_ranktype_as_int(occurrences=occurrences,num_jokers=2)
    ic(rank)
    (6, [13, 1, 1, 13, 13], 611)