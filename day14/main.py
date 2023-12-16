from icecream import ic
from typing import List,Tuple,Dict,Counter,TypeVar,Generator
import numpy as np



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
                load = calc_load(matrix)
                ic(cycle,load)
                print(matrix)
                print(f"repeat was found on cycle {cycle}")
                # cycle +=1 
                cycle_start = cycle
                cycle_length = cycle-cache[matrix_str]
                print(f"the length of the cycle is {cycle_length}")
                break
            else:
                cache[matrix_str] = cycle
            load = calc_load(matrix)
            ic(cycle,load)
            # print(matrix)
        cycle += 1
    # offset = cycles_limit - cycle_start
    offset = cycle_start - cycle_length #offset, where the cycle starts cycling bro
    # index = (offset % cycle_length)-3
    index = (cycles_limit - 1 - offset) % cycle_length + offset #index of answer, will be limit-1-offset
    """lets think about this bs, say we have the numbers 
    83,1,2,3,1,2,3,1,2,3
    obviously the cycle hadnt begun by the first number, so we gonna want to discard it
    the cycle begins at cycle=1 it then begins, with our algorithm we get back to a repeat
    at the fourth index, so when cycle=4 we see a repeat, thus
    cycle_start = 4, cache[matrix] = 1 -> the first time we saw it,
    cycle_length = 4-1 = 3; and that is indeed correct;
    the weird thing to me tho is that cache will contain more than just the repeating cycle
    cache = {str_a: 83, str_b: 1, str_c: 2, str_d: 3}; so we must take care of that with offset
    offset = start-len = 4-3 = 1, what is this? there is some invalid values in our
    cache, that is 83, because it is not a part of the repeating cycle, so we discard it, 
    by getting which cycle we saw the cycle going to repeat, and subtract length, aka
    where the cycle ended
    NOW: we can get the index of where the answer would be with our offset and modulo
    HOW?
    cycles_limit = lets say 10 for this problem, should be 3
    cycle_start = 4
    offset = 1
    (limit-1-offset) = 10-1-1
    length + offset = 3+1 = 4; which will be what we use with modulo, because in our cache;
    we are storing, the length of the cycle + the values that were'nt a part of the cycle
    index = (8)%4 = 0
    calculations:
    cycle_start = cycle
    = 4

    cycle_length = cycle-cache[matrix_str]
    = 4 - 1 = 3

    offset = cycle_start - cycle_length
    4 - 3 = 1

    index = (cycles_limit - 1 - offset) % cycle_length + offset
    = (10 - 1 - 1) % 3 + 1 = 2 + 1 = 3, had some problems, but % is higher
    pri than +/- and im dumb, so index is three, and thus when we go through the vals
    we will return cache where cycle was 3, and that would be zero indexed;
    so itd return 3, and that is the right answer, im also going to change the parens
    in revised version to show explicitly the Order of ops
    """
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

    
"""
O = RoundRock, # = Cube-shaped, . = empty spaces

caclulating load:
O -> number of rows from the rock to the south edge of plat, incl row rock is on
# -> don't contribute to load

part2:
we do cycles: north,west,south,east for 1_000_000_000 cycles, 
my thought is do my same algo, and i feel like at some point,
rocks will stop changing pos?, then we can just see what the 
load is after east rotation then return?
NOTE: for north and west, starting from top right and iterating left->right, up->down, is great, but if we want
to put things on the right side, or the bottom, aka for east, and south, we should iterate backwards, so that we dont
run into O rocks at spots where those rocks might be about to role also so they'd be at the wrong spot

after testing, there is a pattern that emerges after the third cycle, gonna check that it repeats without fail to 1000 or so

after looking at others code, it seems the key is not to find the point at which the mat stops changing, because the nature of this prob
is that it always changes, but it does go through cycles, so how could we find a cycle in the matrix? we can make a dictionary which we call cache
and in the cache we store the keys as the matrix after the cycle as a string, and the value, is the cycle that this result occurred, then we can continue
to add the matrices as strings to our cache until we find a matrix that has already been added, after this there is no patter recognition or anything
that we need to do, because if this matrix already occurred, this exact matrix that is, then we know what the next one will be already because we already
did the algo for this exact matrix and thus, once we have run into the same exact matrix twice, we have a cycle, and with this, we also know the 
length of the cycle, which is just, the current cycle number - the number we first saw this exact matrix occur!! very cool

"""