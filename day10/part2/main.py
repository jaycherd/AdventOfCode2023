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
        path.append((row-1,col))
        return (row-1,col)
    return None

def check_nbr_south(row: int, col: int) -> Optional[Tuple[int,int]]:
    if row+1 < len(matrix) and matrix[row+1][col] in north_connxns and (row+1,col) not in seen:
        seen.add((row+1,col))
        path.append((row+1,col))
        return (row+1,col)
    return None

def check_nbr_west(row: int, col: int) -> Optional[Tuple[int,int]]:
    if col-1 >= 0 and matrix[row][col-1] in east_connxns and (row,col-1) not in seen:
        seen.add((row,col-1))
        path.append((row,col-1))
        return (row,col-1)
    return None

def check_nbr_east(row: int, col: int) -> Optional[Tuple[int,int]]:
    if col+1 < len(matrix[0]) and matrix[row][col+1] in west_connxns and (row,col+1) not in seen:
        seen.add((row,col+1))
        path.append((row,col+1))
        return (row,col+1)
    return None

def find_s_type(row: int, col: int) -> str:
    """use: left,right,up,down --> as bools aka if we go left and it cnnx then left=True"""
    type_map = {
        (True, True, False,False): '-',
        (True, False,True, False): 'J',
        (True, False,False,True) : '7',
        (False,True, True, False): 'L',
        (False,True, False,True) : 'F',
        (False,False,True, True) : '|' 
        }
    #gonna look in order, left,right,up,down
    connexns = [None,None,None,None]
    if col-1 > 0 and matrix[row][col-1] in east_connxns:
        connexns[0] = True
    else:
        connexns[0] = False
    connexns[0] = True if col-1 > 0 and matrix[row][col-1] in east_connxns else False
    connexns[1] = True if col+1 < len(matrix[0]) and matrix[row][col+1] in west_connxns else False
    connexns[2] = True if row-1 > 0 and matrix[row-1][col] in south_connxns else False
    connexns[3] = True if row+1 < len(matrix) and matrix[row+1][col] in north_connxns else False
    connexns = tuple(connexns)
    return type_map[connexns]




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
    type_s = find_s_type(s_tuple[0],s_tuple[1])
    matrix[s_tuple[0]][s_tuple[1]] = type_s
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
    print(f"\n\n\n\n\n{path}")
    ic(len(seen)//2)
    

    


"""
XXX CHANGES XXX
now figure out how many tiles are enclosed by the loop, these are (.) that are fully enclosed by pipes aka no excape to outside of loop
for example:
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
where the enclosed, marked by I, and nonenclosed marked by O, looks like:
...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....
another problem is this is also considered outside, because they can squeeze through the pipe to out connxn
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........

XXX ideas XXX
an interesting idea ive seen, is go around the path, and flag the inside/outside parts of the pipe, then do a flood fill on all those;
that is, if going clockwise to its right would be inside and left would be out see below (i marks in, o out):
.ooooooooo.
oS-------7o
o|F-----7|o
o||ooooo||o
o||ooooo||o
o|L-7.F-J|o
o|ii|.|ii|o
oL--J.L--Jo
.ooooooooo.
so after this there are still some places not marked, and i guess we get those by flood fill

"""