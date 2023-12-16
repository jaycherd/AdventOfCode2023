from icecream import ic
from typing import List,Tuple
from time import perf_counter

def find_num_rows(name: str) -> int:
    count = 0
    try:
        with open(name,'r') as file:
            for line in file:
                count += 1
    except FileNotFoundError:
        print(f"file {name} not found")
    return count

def find_num_cols(name: str) -> int:
    count = 0
    try:
        with open(name,'r') as file:
            for line in file:
                count = len(line.strip())
    except FileNotFoundError:
        print(f"file {name} not found")
    return count

def find_empty_row_cols(name: str) -> None:
    try:
        with open(name,'r') as file:
            for row,line in enumerate(file):
                line = line.strip()
                for col,ch in enumerate(line):
                    if ch == '#':
                        row_is_empty[row] = False
                        col_is_empty[col] = False
    except FileNotFoundError:
        print(f"file {name} not found")
    return None

def expand_the_universe(read: str, write: str) -> None:
    out_empty_line = 'e'*n+'\n'
    try:
        with open(read,'r') as reader, open(write,'w') as writer:
            for row,line in enumerate(reader):
                line = line.strip()
                if row_is_empty[row]:
                    writer.write(out_empty_line)
                    continue
                for col,ch in enumerate(line):
                    if col_is_empty[col]:
                        writer.write('e')
                        continue
                    
                    writer.write(ch)
                if row != m-1:
                    writer.write('\n')
    except FileNotFoundError:
        print(f"reader {read} or writer {write} not found")
    return None

    

def find_gals(f_name: str) -> List[Tuple[int,int]]:
    res : List[Tuple[int,int]] = []
    try:
        with open(f_name,'r') as file:
            for row,line in enumerate(file):
                for col,ch in enumerate(line.strip()):
                    if ch == '#':
                        res.append((row,col))
    except FileNotFoundError:
        print(f"file {f_name} not found")
    return res

def calc_lens(gal_locs: List[Tuple[int,int]]) -> int:
    res = 0
    #we have to pair them all up, sounds like nested for loop i,j
    for i in range(len(gal_locs)):
        #the very first pairs with num_gals-1,2nd num_gals-2, etc.
        for j in range(i+1,len(gal_locs)):
            row,col = gal_locs[i]
            row_end,col_end = gal_locs[j]
            while row < row_end:
                row += 1
                if matrix[row][col] == 'e':
                    res += expansion_multiplier
                else:
                    res += 1
            while col < col_end:
                col += 1
                if matrix[row][col] == 'e':
                    res += expansion_multiplier
                else:
                    res += 1
            #note if end col is left, then we need to go left and above while should not execute
            while col > col_end:
                col -= 1
                if matrix[row][col] == 'e':
                    res += expansion_multiplier
                else:
                    res += 1
    return res

def create_matrix(name: str) -> List[List[str]]:
    res : List[List[str]] = []
    try:
        with open(name,'r') as file:
            for row,line in enumerate(file):
                line = line.strip()
                res.append([])
                for col,ch in enumerate(line):
                    res[row].append(ch)
                    
    except FileNotFoundError:
        print(f"file {name} not found")
    return res

def draw_mat(mat: List[List[str]]) -> None:
    for line in mat:
        print(line)


if __name__ == "__main__":
    start_t = perf_counter()
    f_name = "../in.txt"
    write_f_name = "../out.txt"
    expansion_multiplier = 1000000
    sum_lengths = 0
    m = find_num_rows(f_name)
    n = find_num_cols(f_name)
    row_is_empty = [True]*m
    col_is_empty = [True]*n
    find_empty_row_cols(f_name)
    expand_the_universe(f_name,write_f_name)
    gal_locs = find_gals(f_name)
    matrix = create_matrix(write_f_name)
    res = calc_lens(gal_locs=gal_locs)

    ic(res)

    
    print(f"correct ans = 842645913794")
    end_t = perf_counter()
    print(f"time: {end_t-start_t}")    
    # draw_mat(matrix)
    # print(gal_locs)
    # ic(gal_locs)
    # ic(row_is_empty)
    # ic(col_is_empty)




"""
XXX CHANGES XXX
instead of expanding by one row more, aka doubling the empty rows, now each empty column/row replace with 1 000 000 (million) empty row/cols



XXX idea XXX
we cant write a million lines or cols to a file, seems stupid, instead, lets keep it the way it is;
so lets calc the distances in original file, then again in the new file, with that, could we extract which gals
got further then add million for every 1 unit change? lets see, if not, maybe we could track the unit change AS we are
calculating, or we could mark the row/cols that are empty with a special char, then go down/left/right/up and if we cross one
instead of dist += 1 dist += 1 000 000; this could be an easy way to do; but more code because right now my code does not use that logic, instead
it uses math to calc distance by difference between two points, but it would be possible to figure out which directions i'd need to travel between
two gals and traverse it in the file, but then again i'd also have to store the whole matrix in memory, but that shouldnt be a HUGE deal
well lets see if we can just add a mil for every unit change first

after testing with the test input, did not get expected value, so im gonna try the other solution of writing a special char and adding more units
when we see that char
NOTE: warning below is nonsense, dont need when making gals we located them from left to right, top to bottom, so we will never go up between a pair if we process them in order,
but we can go down,left,or right, because if on 
later row earlier col : down/left
same row later col    : right
next row later col    : down/right
later row same col    : down;
we could store this as a map, with tuples as down/left/right as dx,dy tuples, left = dx = -1, right = dx = 1, down = dy = 1, adding goes down in rows
whether row_src < row_dst can be the mapping keys like:
((row_src < row_dst, col_src < col_dst)) then the results can map to dx,dy results

this is silly, we can do three while loops, one to go down until same row, then two more, to go right until no longer less, then left until
no longer greater, if it starts right of then it will never go further right and vice versa
* all the while just track the distance adding expansion multiplier when we come across an expansion char

seems from reddit that my original logic would have worked but i guess it would have been multiply every 1 unit by 999 999 instead of a mil,
should have figured that, because my logic was sound, the differnce accounts for an expansion of 1 unit, so if we were to replace every exp spot
with a million, that does not mean add a million to it, we already added one for the first expansion, thus to account for the new
expansion we'd want to multiply the diff by 999 999 bcs one is already added
"""