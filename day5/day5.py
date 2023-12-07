from icecream import ic
import re
from typing import Set,Optional,List,Tuple

def clean_line(line: str) -> Tuple[int,int,int]:
    res = (int(x) for x in line.split())
    return res

f_name = "day5in.txt"
seeds = ()
locations = []

try:
    with open(f_name,'r') as file:
        for line in file:
            line = line.strip().split(':')[1]
            seeds = (int(x) for x in line.split())
            break

        #now we have all the seeds, so lets go through the seeds
        for seed_num in seeds:
            node_num = seed_num
            #so the node we start as is seed num, now we traverse everything else like a graph
            des_found = False #this flag checks whether the destination has been found in the current mapping
            for line in file:
                line = line.strip()
                if line == '' or "map" in line or "seeds" in line:
                    des_found = False
                    continue
                if des_found:
                    continue
                des_ran_str,src_ran_str,ran_len = clean_line(line)
                interval = (src_ran_str,src_ran_str + ran_len - 1)
                if node_num >= interval[0] and node_num <= interval[1]:
                    diff = src_ran_str-des_ran_str
                    ic(node_num)
                    node_num = node_num - diff
                    ic(diff)
                    ic(interval)
                    ic(node_num)
                    ic(des_ran_str)
                    ic(src_ran_str)
                    ic(ran_len)
                    des_found = True
            locations.append(node_num)
            file.seek(0)
        print(locations)
        ic(min(locations))

                
                
except FileNotFoundError:
    print(f"file {f_name} not found")


"""
XXX format XXX
seeds: 'list of seed nums'

maps:
destination_range_start  source_range_start  range_length

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
"""