from icecream import ic
import re
from typing import Set,Optional,List,Tuple
from time import perf_counter


def find_first_win(time: int, record: int) -> int:
    for speed in range(time+1):
        remaining_time = time-speed
        this_dist = remaining_time*speed
        if this_dist > record: #then win
            # ic(speed)
            # ic(this_dist)
            return speed

def count_wins(time: int, record: int) -> int:
    count = 0
    for speed in range(time+1):
        remaining_time = time-speed
        this_dist = remaining_time*speed
        if this_dist > record: #then win
            # ic(speed)
            # ic(this_dist)
            # return speed
            count += 1
    return count



if __name__ == "__main__":
    f_name = "in.txt"
    race_times = []
    race_record_dists = []
    ways_to_win_muld = 1

    try:
        with open(f_name,'r') as file:
            for i,line in enumerate(file):
                if i == 0:
                    race_times = [int(x) for x in line.split(':')[1].split()]
                else:
                    race_record_dists = [int(x) for x in line.split(':')[1].split()]
            first_win_speeds = []
            for time,record in zip(race_times,race_record_dists):
                # first_win_speed = find_first_win(time,record)
                # first_win_speeds.append(first_win_speed)
                # winning_speeds = time-first_win_speed*2-1
                # ic(winning_speeds)
                ways_to_win_muld *= count_wins(time,record)
            ic(race_times)
            ic(race_record_dists)
            ic(first_win_speeds)
            ic(ways_to_win_muld)



    except FileNotFoundError:
        print(f"file {f_name} not found")


"""
XXX Description XXX
Each value in times is a race time
Each Value in dist is corresponding record distance for that race
* for every millisecond that you hold down button boat speed increased by 1 millimeter per second
    * so holding one ms, then you have a boat that will go 1 mm/ms for the whole race

XXX goal XXX
figure out how many ways the race can be one, aka if holding button 1 or 2 or 3 ms all result in win, then their are 3 ways total,
for every race, find how many ways there are to win and multiply them together

XXX idea XXX
i believe its going to make a bell curve type answer every time, that is there will be an optimal amount of time to hold the button
and as you iterate away from the optimal to left and right, both left and right will be equally optimal, so could iterate up to find
first pass, then have second path by subtracting from other side of the array, could prob even binary search that, although input nums not that big

"""