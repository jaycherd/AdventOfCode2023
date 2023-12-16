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
    gal_locs1 = find_gals(f_name)
    sum_lengths1 = calc_lens(gal_locs1)
    expand_the_universe(f_name,write_f_name)
    gal_locs2 = find_gals(write_f_name)
    sum_lengths2 = calc_lens(gal_locs2)
    diff = sum_lengths2 - sum_lengths1
    res = sum_lengths2 + diff*1000000


    ic(diff)
    ic(res)
    print(f"correct ans = 842645913794")
    ic(sum_lengths2)
    # ic(gal_locs)
    # ic(row_is_empty)
    # ic(col_is_empty)




"""
See main3 for a great solution, logic exp for main3 is under here and in main3
seems what some people did is store the special rows/cols in a list or set and got them out, then checked if curr row and end row/cols
had a special row/col between them then mul by factor to get ans
* they did loops like for r in empty_rows, where empty rows held nums to all the empty rows, then for every r, from for r in emptyrows,
they check, is that r between the pair they are currently checking? if it is then add dist += 999_999 in this case we do 1 less, because, the
row should be replace by 1_000_000 so we already accounted for one of those when we do the regular addition that we were doing before, because
they still get the rest of the distance by manhattan distance, which is just the abs diff b/w dx and dy, i like this type of solution, much better
because of the fact we dont write to a file, in addition to NO matrix in main memory, instead we just do manhattan distance, plus 999_999 for any
empty row/col that is between the current pair we are considering and +1 for part 1, so this logic also works for both parts
a great solution, and can be seen on main3.py

still wrong even when changed to 999999, not sure what is wrong, why can't we just get the diff, and mul the diff? not sure..
bcs when we expand by one, why wouldnt we then multiply by mil idk

okay lets imagine 3 dots between a and b, so we have:
a...b
now if we expand all the dots, that is make each dot two dots then we have
a......b now there are 6 dots between, so difference between these two values is 6-3=3 if we mul 1000000 = 3,000,000 then
that would indeed be the right answer, hmm

XXX idea XXX
find empty rows; expand them; write that to a file; then number gals; make dict: {galnum: (row,col)} then find ea/other and add up
"""