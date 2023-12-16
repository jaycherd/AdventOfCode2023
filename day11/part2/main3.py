from time import perf_counter

start_t = perf_counter()

#interesting but a fat file in main memory, my logic seems to process in better, but maybe not a big deal?
#however this keeps all of input in main, and if file is huge then this is huge, and its not necessary
#however it does allow easy creation of galaxies later
input = open("../in.txt").read().strip().splitlines()
#as sus. this creates List[List[str]] ea/inner list is one of the Lines in the file
#this is not ideal because for large files this will cause problems and is unneccessary, and the logic
#of this approach is awesome because we can process line by line, store locations, then do the math
#with the locations of gals and the empty rows/cols no need to store the giant input file which in real world could be HUGE

empty_rows = [r for r, row in enumerate(input) if all(c == '.' for c in row)]
empty_cols = [c for c, col in enumerate(zip(*input)) if all(c == '.' for c in col)]

#this is awesome, way more clean way of making List of tuples, based on criteria
galaxies = [(i, j) for i in range(len(input)) for j in range(len(input[0])) if input[i][j] == '#']

res = 0
for r, g1 in enumerate(galaxies):
    for l, g2 in enumerate(galaxies[:r]):
        #dist could be done cleaner with some abs vals also
        dist = (max(g1[0], g2[0]) - min(g1[0], g2[0])) + (max(g1[1], g2[1]) - min(g1[1], g2[1]))
        #next check for empty rows, if any are between the curr pair, same for empty cols after
        for r in empty_rows:
            if min(g1[0], g2[0]) < r < max(g1[0], g2[0]):
                dist += 1_000_000 - 1
        for c in empty_cols:
            if min(g1[1], g2[1]) < c < max(g1[1], g2[1]):
                dist += 1_000_000 - 1
        res += dist

print(res)

end_t = perf_counter()
print(f"time: {end_t-start_t}")


"""
they did loops like for r in empty_rows, where empty rows held nums to all the empty rows, then for every r, from for r in emptyrows,
they check, is that r between the pair they are currently checking? if it is then add dist += 999_999 in this case we do 1 less, because, the
row should be replace by 1_000_000 so we already accounted for one of those when we do the regular addition that we were doing before, because
they still get the rest of the distance by manhattan distance, which is just the abs diff b/w dx and dy, i like this type of solution, much better
because of the fact we dont write to a file, in addition to NO matrix in main memory, instead we just do manhattan distance, plus 999_999 for any
empty row/col that is between the current pair we are considering and +1 for part 1, so this logic also works for both parts
a great solution, and can be seen on main3.py

what i dont like tho: reading the entire file into main memory when it can be read line by line, interestingly,
my approach which reads it, writes to a diff file with an expansion char to flag expansion, then moving down/left/right
through every step between pairs runs only marginally slower like 10% where i would have thought this sol. be much faster,
i think if we dont read all into main, and did a simpler manhattan dist. we could see some imp, as well as not iterating
over all empty rows, that is shortcutting when the rows are out of range, or targeting only those in range, that would be harder but doable maybe
however breaking the loop when r is greater, if r is sorted, could improve
interesting nonetheless and this solution is definitely better in not creating a matrix, and would be even better with lines
being processed one at a time
"""