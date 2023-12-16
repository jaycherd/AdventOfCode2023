from icecream import ic
from typing import List,Tuple

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
    out_empty_line = '.'*out_line_length+'\n'
    try:
        with open(read,'r') as reader, open(write,'w') as writer:
            for row,line in enumerate(reader):
                line = line.strip()
                if row_is_empty[row]:
                    for _ in range(2):
                        writer.write(out_empty_line)
                    continue
                for col,ch in enumerate(line):
                    if col_is_empty[col]:
                        for _ in range(2):
                            writer.write(ch)
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
            res += abs(gal_locs[i][0]-gal_locs[j][0]) + abs(gal_locs[i][1]-gal_locs[j][1])
    return res




if __name__ == "__main__":
    f_name = "../in.txt"
    write_f_name = "../out.txt"
    sum_lengths = 0
    m = find_num_rows(f_name)
    n = find_num_cols(f_name)
    row_is_empty = [True]*m
    col_is_empty = [True]*n
    find_empty_row_cols(f_name)
    out_line_length = n + sum(col_is_empty) #sum True=1,False=0
    ic(out_line_length)
    expand_the_universe(f_name,write_f_name)
    gal_locs = find_gals(write_f_name)
    sum_lengths = calc_lens(gal_locs)
    
    
    ic(sum_lengths)
    # ic(gal_locs)
    # ic(row_is_empty)
    # ic(col_is_empty)




"""
XXX DESCRIPTION XXX
your puzzle input). The image includes empty space (.) and galaxies (#). For example:
example:
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....

however the light took time to reach us, and the galaxies have expanded, the rows/cols where there are no galaxies should be twice as big
so here are the rows/cols with no gals marked with arrows
   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^
after expanding those, making empty twice as big
....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
transforming gals, to nums
....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......
now we have to find the distance between every pair, with nine gals 36 pairs, why?
because first paired with everything else is 8 pairs, 1-2,1-3,...,1-9;
then we pair 2 with everything, so 2-3,...,2-9 (no 2-1) already done with 1-2
so: 8+7+6+5+4+3+2+1=36 pairs total; for every pair, find the shortest possible path;
only steps allowed are left,right,up,down; so we cant do pythags or anything;
here is a shortest path (between 5-9), marked;
....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......
this is 9 steps, 8 marked by '#' and one is the step it takes to get onto '9'
....1........
.........2...
3............
.............
.............
........4....
.5...........
.#...........
.#..........6
.#...........
.#.......7...
8####9.......
luckily, we dont need the steps to be done like the one before, we can just go down/up then make a 90 degree turn,
and if on same row/col then just go straight to it;


XXX idea XXX
find empty rows; expand them; write that to a file; then number gals; make dict: {galnum: (row,col)} then find ea/other and add up
"""