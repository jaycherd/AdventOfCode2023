from icecream import ic
from typing import List,Tuple,Dict,Counter,TypeVar,Generator
import numpy as np

"""GOAL:
this files goal is to clear up the confusion i had with out the indexing
and use of cache was working, i get it now, so gonna rename some vars and what not"""

def generate_matrix(f_name: str) -> np.ndarray[str,str]:
    res = []
    try:
        with open(f_name,'r')as file:
            for line in (list(line.strip()) for line in file):
                res.append(line)
    except FileNotFoundError:
        print(f"file {f_name} not found")
    return np.array(res,dtype=str)

def np_ndarr_from_str(mat_str: str) -> np.ndarray[str,str]:
    mat_strs = mat_str.split('\n')
    res = []
    for line in mat_strs:
        res.append(list(line))
    return np.array(res,dtype=str)

def tilt_north(matrix: np.ndarray[str,str]) -> None: #matrix altered in place
    direction = (-1,0) #changing row+-1,col+0; moves upwards, NORTH
    for i in range(1,matrix.shape[0]):#no need look at first row it has nowhere to move, remem, matrix.shape = (numrows,numcols)
        for j in range(matrix.shape[1]):
            rock = matrix[i][j]
            if rock == '.' or rock == '#':
                continue
            i_walker = i + direction[0]
            while i_walker >= 0 and matrix[i_walker][j] == '.':
                matrix[i_walker-direction[0]][j] = '.'
                matrix[i_walker][j] = 'O'
                i_walker += direction[0]
    return None

def tilt_south(matrix: np.ndarray[str,str]) -> None:
    direction = (1,0) #changing row+-1,col+0; moves upwards, NORTH
    for i in range(matrix.shape[0]-2,-1,-1):#no need look at first row it has nowhere to move, remem, matrix.shape = (numrows,numcols)
        for j in range(matrix.shape[1]-1,-1,-1):
            rock = matrix[i][j]
            if rock == '.' or rock == '#':
                continue
            i_walker = i + direction[0]
            while i_walker < matrix.shape[0] and matrix[i_walker][j] == '.':
                matrix[i_walker-direction[0]][j] = '.'
                matrix[i_walker][j] = 'O'
                i_walker += direction[0]
    return None

def tilt_west(matrix: np.ndarray[str,str]) -> None:
    direction = (0,-1)
    for i in range(matrix.shape[0]):
        for j in range(1,matrix.shape[1]):
            rock = matrix[i][j]
            if rock == '.' or rock == '#':
                continue
            j_walker = j + direction[1]
            while j_walker >= 0 and matrix[i][j_walker] == '.':
                matrix[i][j_walker-direction[1]] = '.'
                matrix[i][j_walker] = 'O'
                j_walker += direction[1]
    return None

def tilt_east(matrix: np.ndarray[str,str]) -> None:
    direction = (0,1)
    for i in range(matrix.shape[0]-1,-1,-1):
        for j in range(matrix.shape[1]-2,-1,-1):
            rock = matrix[i][j]
            if rock == '.' or rock == '#':
                continue
            j_walker = j + direction[1]
            while j_walker < matrix.shape[1] and matrix[i][j_walker] == '.':
                matrix[i][j_walker-direction[1]] = '.'
                matrix[i][j_walker] = 'O'
                j_walker += direction[1]
    return None

def calc_load(matrix: np.ndarray[str,str]) -> None:
    load_causers = {'O'}
    total_load = 0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            rock = matrix[i][j]
            if rock in load_causers:
                total_load += matrix.shape[0]-i
    return total_load

def is_changing(mat_a: np.ndarray[str,str], mat_b: np.ndarray[str,str]) -> bool:
    return not np.array_equal(mat_a,mat_b)

def mat2str(mat: np.ndarray[str,str]) -> str:
    return "\n".join("".join(line) for line in mat)


def part1(f_name: str) -> None:
    matrix = generate_matrix(f_name)
    # ic(matrix,type(matrix))
    tilt_north(matrix)
    # ic(matrix)
    ic(calc_load(matrix))

def part2(f_name: str) -> None:
    cycles_limit = 1_000_000_000
    cache = {} #we can hold the string version of the matrix in memory!!!
    cycle_length = None #look for a cycle of the same numbers repeating so we can warp to the end! with math yay
    matrix = generate_matrix(f_name)
    cycle = 0
    while cycle < cycles_limit:
        tilt_north(matrix)
        tilt_west(matrix)
        tilt_south(matrix)
        tilt_east(matrix)
        if not cycle_length:
            matrix_str = mat2str(matrix)
            if matrix_str in cache:
                print(f"repeat was found on cycle {cycle}")
                # cycle +=1 
                cycle_repeat_found = cycle
                cycle_length = cycle-cache[matrix_str]
                print(f"the length of the cycle is {cycle_length}")
                break
            else:
                cache[matrix_str] = cycle
            load = calc_load(matrix)
        cycle += 1
    cycling_start = cycle_repeat_found - cycle_length #offset, where the cycle starts cycling bro
    index = ((cycles_limit - 1 - cycling_start) % cycle_length) + cycling_start
    #note our limit is 1-indexed, we want 1 billion cycles to occur, and our cache is zero-indexed
    #so we subtract one to account
    #cycle repeats so we mod by cycle then add where the cycle begins in our cache, and that
    #is the index in the cache
    res = None
    # print(cache)
    for mat_str, cycle_num in cache.items():
        if cycle_num == index:
            res = calc_load(np_ndarr_from_str(mat_str))
            cycle_res = cycle_num
    ic(res) if res else ic("-1")
    ic(cycle_res)


if __name__ == "__main__":
    f_name1 = "test.txt"
    f_name2 = "input.txt"
    # part1(f_name2)
    part2(f_name2)
