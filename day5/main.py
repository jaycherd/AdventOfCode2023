from icecream import ic
import re
from typing import Set,Optional,List,Tuple
from time import perf_counter

def clean_line(line: str) -> Tuple[int,int,int]:
    res = (int(x) for x in line.split())
    return res

def merge_intervals_special(intervalsA: List[Tuple[int, int, int]], intervalsB: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """
    Merge two lists of intervals. Only overlapping intervals are considered.
    If an interval in intervalsB overlaps with intervalsA, it takes priority.
    Parts of intervalsB that do not overlap with any interval in intervalsA are dropped.
    """
    result = []

    for a_start, a_end, a_diff in intervalsA:
        a_index = a_start
        while a_index <= a_end:
            overlap_found = False
            for b_start, b_end, b_diff in intervalsB:
                if b_start <= a_index <= b_end:
                    # Overlap found, use intervalsB's diff
                    overlap_end = min(b_end, a_end)
                    result.append((a_index, overlap_end, b_diff))
                    a_index = overlap_end + 1
                    overlap_found = True
                    break
            
            if not overlap_found:
                # No overlap, use intervalsA's diff
                next_b_start = min([b_start for b_start, _, _ in intervalsB if b_start > a_index], default=a_end + 1)
                result.append((a_index, min(a_end, next_b_start - 1), a_diff))
                a_index = next_b_start

    return sorted(result, key=lambda x: x[0])

def merge_intervals(intervals: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int]]:
    """
    Merge overlapping intervals based on their start and end values, 
    while preserving the identifier of the first interval in each merged pair.

    Args:
    intervals (List[Tuple[int, int, int]]): A list of intervals sorted by start value, 
                                            each with an identifier.

    Returns:
    List[Tuple[int, int, int]]: A list of merged intervals with their original identifiers.
    """
    if not intervals:
        return []

    # Initialize the merged intervals list with the first interval
    merged = [intervals[0]]

    for current in intervals[1:]:
        previous = merged[-1]

        # Check if the current interval overlaps with the previous interval (considering only the start and end)
        if current[0] <= previous[1]:
            # Merge the current interval with the previous one and keep the identifier of the first interval
            merged[-1] = (previous[0], max(previous[1], current[1]), previous[2])
        else:
            # No overlap, so add the current interval to the merged list
            merged.append(current)

    return merged

def get_seed_intervals(intervals: List[int]) -> List[Tuple[int,int]]:
    res = []
    for i in range(0,len(intervals),2):
        start = intervals[i]
        end = intervals[i] + intervals[i+1] - 1
        res.append((start,end))
    res.sort(key=lambda I: I[0]) #sort intervals by start, so we can merge them later
    res = merge_intervals(res)
    return res

def generate_srcintervals_withdiff(line: List[int]) -> List[Tuple[int,int,int]]:
    start = line[1]
    end = line[1] + line[2]-1
    diff = line[0] - line[1]
    return (start,end,diff)

def convert_src_to_dest(intervals: List[Tuple[int,int,int]]) -> List[Tuple[int,int,int]]:
    res = []
    for start_src,end_src,diff in intervals:
        res.append((start_src + diff, end_src + diff, 0))
    return res

def standardize_intervals(intervals: List[Tuple[int,int]],default_identifier = 0) -> List[Tuple[int,int,int]]:
    return [(start, end, default_identifier) for start,end in intervals]

def find_res_min(res: Tuple[int,int]) -> int:
    sol = float('inf')
    for a,b in res:
        if a < sol:
            sol = a
        if b < sol:
            sol = b
    return sol


if __name__ == '__main__':
    start_time = perf_counter()

    f_name = "day5in.txt"
    node_intervals = []
    locations = []
    current_intervals_source_and_diff : List[Tuple[int,int,int]] = [] #will be like so -> [(startsource,endsource,difference)] difference = destination-source


    try:
        with open(f_name,'r') as file:
            for line in file:
                line = line.strip().split(':')[1]
                node_intervals = [int(x) for x in line.split()]
                node_intervals = get_seed_intervals(node_intervals)
                node_intervals = standardize_intervals(node_intervals)
                # ic(node_intervals)
                break

            for line in file:
                line = line.strip()
                if line == '':
                    continue
                if "map" in line: #then process all lines in current map
                    for line in file:
                        line = line.strip()
                        if line == '' or "end" in line:
                            current_intervals_source_and_diff.sort(key=lambda V: V[0])
                            current_intervals_source_and_diff = merge_intervals(current_intervals_source_and_diff)
                            ic(current_intervals_source_and_diff)
                            node_intervals = merge_intervals_special(node_intervals,current_intervals_source_and_diff)
                            ic(node_intervals)
                            node_intervals = convert_src_to_dest(node_intervals)
                            ic(node_intervals)
                            current_intervals_source_and_diff.clear()
                            break
                        this_interval = [int(x) for x in line.split()]
                        this_interval = generate_srcintervals_withdiff(this_interval)
                        current_intervals_source_and_diff.append(this_interval)
            locations.append(node_intervals)
            file.seek(0)
        res = []
        for node_str,node_end,diff in node_intervals:
            res.append((node_str + diff,node_end + diff))
        # ic(res)
        sol = find_res_min(res)
        print(f"closest location = {sol}")
                    
    except FileNotFoundError:
        print(f"file {f_name} not found")

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time} seconds")


"""
XXX format - CHANGE XXX
seeds: 'seednum_start seednum_range_len'

for example seeds: 10  10 would mean seeds 10,11,12,13,14,15,16,..19, so ten seed nums, but starting at ten ending at 19


XXX additional notes XXX
any NON-mapped values -> source = destination
the ranges are ridiculous, so i dont thing its gonna be possible to just create the literal map and traverse
ie. 466206721 134904099 264145987
about 300 lines just like this one, so i dont think its feasible to create an actual map of this


XXX goal XXX
find the lowest location number, that is find the seed that ends at the LOWEST location, note the location is just the number we end
up at at the last map "humidity-to-location map"

XXX ideas XXX
sounds like a graph then, we map all the values, then traverse the map from the seed to the last map
* can not just make the map, too many values to do this
idea - iterate through the seeds, starting from seed, go to each mapping, see if that seed is mapped, compute destination and continue, i think a dfs
will be best, that is, fully go through to the location at the end, then go to the next seed, etc.
algo for this idea:
* for seed in seeds:
* check if this seed is in any of the sources in map:
    * to check this, compute intervals, interval = [source_range_start, source_range_start + range_length-1]
        * now just see if seed is in that interval, if it is then we need to compute destination
        * destination = seed_num + difference
            * difference = source_range_start - destination_range_start
* if it wasn't in that interval, then go to the next interval and check that one, if its in none of them, then destination=source
* do this for all the maps, until you get to location

NEW PROBLEM:
* we can't necessarily use the same logic, because even having a list of seeds would now be impossible as the lists would be 100 millions of numbers,
* maybe generate all the intervals for every map, then turn seeds into intervals of seeds, and turn those intervals into intervals of intervals that
fit into each mapping 

XXX how i got it working XXX
* turn the seeds into intervals, (start,end,diff) start and end is inclusive, and diff is how we will calculate traversal to the next node
    * later i'm going to call seed_intervals node_intervals because it makes more sense, like we are traversing a graph that
        starts at the seed values in the beginning and ending at the locations at the end, so node_intervals will change as we go
        through the graph
    * we initialize diff as zero for all the seeds cus if it does not fit into any of the intervals then node_dest = node_src
* next we start iterating through the file, for each map, we create a new map of intervals (start_src,end_src,diff)
    * now diff is going to hold a value that will later let us traverse from the src node to the destination node
* now we use our special merging function to merge node_intervals with the map_intervals
    * special bcs there are additional criteria, the criteria:
        * if node_intervals within map_intervals, then node_intervals[2] aka its diff equals map_intervals[2], we inherit diff from the mapping it fell within
        * if node_intervals NOT within map_intervals, then node_intervals[2] = 0, because its' dest. will be equal to source
        * for all the other values, that are in map_intervals but not node_intervals we drop it, because those values don't correspond
            to any of the beginning seeds
* After that merge, we now have a new node_intervals, this is still (start,end,diff) but now all of the intervals that fell
    within the mapping have the diff that corresponds
* next we can finally traverse the graph! we do this by changing node_intervals to (start + diff, end + diff, 0)
    * we change start of interval to its corresponding destination, and same for end, reset the diff to zero, because once we start looking at the next
        mapping, if we dont find anything we want source = destination
* repeat this and at the end we get node_intervals = (location_start,location_end,0) and we can just take the min start_location we come across
    * at the very end we just have an interval of the location where the location was calculated just like all the other node traversals, so the start
        will be less than the end of the interval and we can just take the smallest value, because we drop all parts of intervals that don't contain
        a value from the starting seeds and continue to do so, we never have any node_interval values that contain values outside of the interval,
        thus, at the end, we know the min_start is the min location that was possible to create
"""