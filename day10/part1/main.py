from icecream import ic
import re
from typing import Set,Optional,List,Tuple,Dict
from time import perf_counter
from collections import deque
import math
from functools import reduce

def find_nbrs(row: int, col: int) -> Tuple[Tuple[int,int],Tuple[int,int]]:
    invalid_horizontal = {'.','|'}
    invalid_vertical   = {'.','-'}
    nbrs = []
    if row-1 > 0 and matrix[row-1][col] not in invalid_vertical:
        nbrs.append((row-1,col))
    if row+1 < len(matrix) and matrix[row+1][col] not in invalid_vertical:
        nbrs.append((row+1,col))
    if col-1 > 0 and matrix[row][col-1] not in invalid_horizontal:
        nbrs.append((row,col-1))
    if col+1 < len(matrix[0]) and matrix[row][col+1] not in invalid_horizontal:
        nbrs.append((row,col+1))
    ic(nbrs)
    return nbrs

def find_nbr(row: int, col: int) -> Optional[Tuple[int,int]]:
    invalid_horizontal = {'.','|'}
    invalid_vertical   = {'.','-'}
    if row-1 > 0 and matrix[row-1][col] in north_connxns and (row-1,col) not in seen:
        seen.add((row-1,col))
        return (row,col)
    if row+1 < len(matrix) and matrix[row+1][col] not in invalid_vertical and (row+1,col) not in seen:
        seen.add((row+1,col))
        return (row,col)
    if col-1 > 0 and matrix[row][col-1] not in invalid_horizontal and (row,col-1) not in seen:
        seen.add((row,col-1))
        return (row,col)
    if col+1 < len(matrix[0]) and matrix[row][col+1] not in invalid_horizontal and (row,col+1) not in seen:
        seen.add((row,col+1))
        return (row,col)
    return None

def check_nbr_north(row: int, col: int) -> Optional[Tuple[int,int]]:
    if row-1 >= 0 and matrix[row-1][col] in south_connxns and (row-1,col) not in seen:
        seen.add((row-1,col))
        return (row-1,col)
    return None

def check_nbr_south(row: int, col: int) -> Optional[Tuple[int,int]]:
    if row+1 < len(matrix) and matrix[row+1][col] in north_connxns and (row+1,col) not in seen:
        seen.add((row+1,col))
        return (row+1,col)
    return None

def check_nbr_west(row: int, col: int) -> Optional[Tuple[int,int]]:
    if col-1 >= 0 and matrix[row][col-1] in east_connxns and (row,col-1) not in seen:
        seen.add((row,col-1))
        return (row,col-1)
    return None

def check_nbr_east(row: int, col: int) -> Optional[Tuple[int,int]]:
    if col+1 < len(matrix[0]) and matrix[row][col+1] in west_connxns and (row,col+1) not in seen:
        seen.add((row,col+1))
        return (row,col+1)
    return None


if __name__ == "__main__":
    f_name = "../in.txt"
    s_tuple : Tuple[int,int] = None
    matrix : List[List[str]] = []
    path : List[Tuple[int,int]] = []
    seen : Set[Tuple[int,int]] = set()
    south_connxns : Set[str] = {'|','7','F'}
    north_connxns : Set[str] = {'|','L','J'}
    east_connxns  : Set[str] = {'-','F','L'}
    west_connxns  : Set[str] = {'-','J','7'}

    try:
        with open(f_name,'r') as file:
            #first lets create our matrix AND find S
            for i,line in enumerate(file):
                matrix.append(list(line.strip()))
                if s_tuple is None:
                    for j,val in enumerate(line):
                        if val == 'S':
                            s_tuple = (i,j)
                            path.append(s_tuple)
                            seen.add(s_tuple)
            # ic(matrix)
            ic(s_tuple)

    
    except FileNotFoundError:
        print(f"file {f_name} not found")

    #okay we can go through pipes now
    #s has exactly two types connecting to it per description, and so do others, so no need to check that loop is a valid loop
    curr_tuple = s_tuple
    while True:
        row,col = curr_tuple
        if matrix[row][col] == '|':
            tmp = check_nbr_north(row,col)
            if tmp:
                curr_tuple = tmp
                continue
            else:
                tmp = check_nbr_south(row,col)
                if tmp:
                    curr_tuple = tmp
                    continue
        elif matrix[row][col] == '-':
            tmp = check_nbr_east(row,col)
            if tmp:
                curr_tuple = tmp
                continue
            else:
                tmp = check_nbr_west(row,col)
                if tmp:
                    curr_tuple = tmp
                    continue
        elif matrix[row][col] == 'L':
            tmp = check_nbr_north(row,col)
            if tmp:
                curr_tuple = tmp
                continue
            else:
                tmp = check_nbr_east(row,col)
                if tmp:
                    curr_tuple = tmp
                    continue
        elif matrix[row][col] == 'J':
            tmp = check_nbr_north(row,col)
            if tmp:
                curr_tuple = tmp
                continue
            else:
                tmp = check_nbr_west(row,col)
                if tmp:
                    curr_tuple = tmp
                    continue
        elif matrix[row][col] == '7':
            tmp = check_nbr_south(row,col)
            if tmp:
                curr_tuple = tmp
                continue
            else:
                tmp = check_nbr_west(row,col)
                if tmp:
                    curr_tuple = tmp
                    continue
        elif matrix[row][col] == 'F':
            tmp = check_nbr_south(row,col)
            if tmp:
                curr_tuple = tmp
                continue
            else:
                tmp = check_nbr_east(row,col)
                if tmp:
                    curr_tuple = tmp
                    continue
        elif matrix[row][col] == '.':
            print("error we are at a (.)")
            exit()
        elif matrix[row][col] == 'S':
            tmp = check_nbr_north(row,col)
            if tmp:
                curr_tuple = tmp
                continue
            tmp = check_nbr_south(row,col)
            if tmp:
                curr_tuple = tmp
                continue
            tmp = check_nbr_east(row,col)
            if tmp:
                curr_tuple = tmp
                continue
            tmp = check_nbr_west(row,col)
            if tmp:
                curr_tuple = tmp
                continue
        break
    
    print(seen)
    ic(len(seen)//2)

    


"""
XXX DESCRIPTION XXX
The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

we know the animal is in one large, continuous loop
for example
.....
.F-7.
.|.|.
.L-J.
.....

If the animal had entered this loop in the northwest corner, the sketch would instead look like this:
.....
.S-7.
.|.|.
.L-J.
.....
so we know the S is a 90-degree F bend, because that would make a loop
However, it is much more complicated than just that, the input looks more like:
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
it still contains what we saw above, but it is much harder to see

Heres a more complex loop:
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
And with the surroundings in
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ

the goal is to find the tile in the loop that's farthest from the starting position, this is same spot
regardless of which way around the loop the animal went, so im guessing it will always have an even number? of items, then the exit
will be opposite of the entrance?
example
.....
.S-7.
.|.|.
.L-J.
.....
transformed to distance from start
.....
.012.
.1.3.
.234.
.....
as you can see, the loop is even, 8 pipes, and the furthest pipe is 4 steps away for both ways around

and the more complex one:
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
transformed
..45.
.236.
01.78
14567
23...

what to do: find the single giant loop starting at S, return How many steps along the loop it takes to get from the starting pos. to 
the point farthest from the starting pos.


XXX THOUGHTS XXX
go to S, look outward in every direction, if it is a pipe then go that way, then can traverse like normal next direction depends on the pipe we are in,
all the while have a seen set, that holds tuples (row,col) and if we come across a combo already in set, then we have found the loop, actually
maybe we want seen to be a list of tuples, for every tuple we've seen, so later we could just return the len of those tuples as we'll find the loop, i dont
think we have options cus each pipe only has one entrance and one exit, so only one we may have wory about could be S, but that also looks like it
only connects to two differnt pipes

only problem is i think i need to load all the lines into a matrix, so O(n) space complexity, other way i can think of is loading the lines
in as needed but then we have to iterate through the file lines every time to load a line above or below whatever line we are at if we need to
aka if a pipe leads that way, and that seems unneccessary
"""