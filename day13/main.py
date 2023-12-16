from icecream import ic
from typing import List,Tuple,Dict,Counter,Generator


def generate_matrix(f_name: str) -> Generator[List[List[str]],None,None]:
    try:
        mat = []
        with open(f_name,'r') as file:
            for line in (list(line.strip()) for line in file):
                if line:
                    mat.append(line)
                else:
                    yield mat
                    mat = []
            if mat:
                yield mat
    except FileNotFoundError:
        print(f"file {f_name} not found")

def is_reflection(a: List[str], b: List[str]) -> bool:
    for vala,valb in zip(a,b):
        if vala != valb:
            return False
    return True

def col_to_line(mat: List[List[str]], i1: int, i2: int) -> Tuple[List[str],List[str]]:
    a,b = [],[]
    for row in mat:
        a.append(row[i1])
        b.append(row[i2])
    return a,b

def part1(f_name: str) -> None:
    ROW_MULTIPLIER = 100
    res_horizontals,res_verticals = [],[]
    for matrix in generate_matrix(f_name=f_name):
        vertical_line,horizontal_line = None,None
        for i in range(1,len(matrix)):
            if is_reflection(matrix[i],matrix[i-1]):
                horizontal_line = i
        for i in range(1,len(matrix[0])):
            a,b = col_to_line(matrix,i,i-1)
            if is_reflection(a,b):
                vertical_line = i
        res_horizontals.append(horizontal_line) if horizontal_line else res_verticals.append(vertical_line)
    ic(res_horizontals,res_verticals)

"""not what they wanted, i think that they want you to find the point of reflection for the whole pattern, but you can only discard
one line, not as many as you want, so you should make sure it reflects all the lines except at most one?"""
        






if __name__ == "__main__":
    f_name1 = "test.txt"
    f_name2 = "input.txt"
    part1(f_name1)
    # part1(f_name2)



"""
learned and using a generator function here, pretty cool, type hinting is a little different
you specify the [type of value it yields, type it can recieve, and return type]"""


"""
says reflxn is across only two rows/cols that matters, so i guess just look for that, by pairing rows/cols and checking
note only one line in each matrix(pattern)
find horiz/vertical lines of reflection, lines go b/w the cols/rows, and dont have to include
every row/col you start from the line of reflexn that you find, and work your way outwards, seeing
how many rows/cols of reflection there are,
1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7
this pattern has 4-5,3-6,2-7, and hypothetically 1-8 but no 8 however we still add the one, because we can prove nor disprove there would be an 8
and for the cols
123456789
    ><   
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><   
123456789
the cols reflect b/w cols 5-6,4-7,3-8,2-9, but we have nothing to compare 1 to, so we just include it

in the end return --> cols left of rflxn + rows above horiz rflxn*100
"""