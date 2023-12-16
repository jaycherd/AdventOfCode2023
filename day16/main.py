from icecream import ic
from typing import List,Tuple,Dict,Counter,TypeVar,Generator,Set
import utils
from collections import defaultdict
from time import perf_counter


class BeamShooter:
    def __init__(self,matrix: List[List[str]]):
        self.matrix = matrix
        self.m = len(matrix)
        self.n = len(matrix[0])
        self.location_to_beams_map : Dict[Tuple[int,int],Set[Tuple[int,int]]] = defaultdict(set)
        self.backslash_map = {(0,1) : (1,0), (0,-1) : (-1,0), (1,0) : (0,1), (-1,0) : (0,-1)}
        self.fwrdslash_map = {(0,1) : (-1,0),(0,-1) : (1,0),  (1,0) : (0,-1),(-1,0) : (0,1)}
        self.start_row_dir_map = {0:1, self.m-1: -1}
        self.start_col_dir_map = {0:1, self.n-1: -1}
        self.horizontal_dirs = {(0,1),(0,-1)}
        self.vertical_dirs = {(1,0),(-1,0)}
        self.best_start_loc = (-1,-1)
        self.best_energy_lvl = -1
        

    def beam_valid(self,row: int,col: int) -> bool:
        return row < self.m and row >= 0 and col < self.n and col >= 0
    
    def is_corner(self,i: int, j: int) -> bool:
        return (i==0 and j==0) or (i==self.m-1 and j==self.n-1) or (i==0 and j==self.n-1) or (i==self.m-1 and j==0)
    
    def check_energy(self,row: int,col: int) -> None:
        energy = len(self.location_to_beams_map)
        if energy > self.best_energy_lvl:
            self.best_energy_lvl = energy
            self.best_start_loc = (row,col)
        self.location_to_beams_map.clear()


    def shoot_beam(self, beam: Tuple[int,int,int,int]) -> None:
        while True:
            row,col,dx,dy = beam
            if (row,col) in self.location_to_beams_map and (dx,dy) in self.location_to_beams_map[(row,col)]:
                return #basically this means, a beam already traveled this path, lets not trav it again
            # ic(beam)
            if self.beam_valid(row,col):
                self.location_to_beams_map[(row,col)].add((dx,dy)) #i'm going to have the direction, as the direction, the light enters a given square
                if self.matrix[row][col] == '.':
                    beam = (row+dx,col+dy,dx,dy)
                elif self.matrix[row][col] == '|': #split ew
                    if (dx,dy) in self.horizontal_dirs: #then we must split
                        self.shoot_beam((row-1,col,-1,0)) #shoot one up
                        self.shoot_beam((row+1,col,1,0)) #shoot one down
                        return #so it looks neat, i shoot both and once both are done, we return
                    else: #else beam continues on the same path
                        beam = (row+dx,col+dy,dx,dy)
                elif self.matrix[row][col] == '-':
                    if (dx,dy) in self.vertical_dirs:
                        self.shoot_beam((row,col-1,0,-1)) #shoot one left
                        self.shoot_beam((row,col+1,0,1))  #shoot one right
                        return
                    else:
                        beam = (row+dx,col+dy,dx,dy)
                elif self.matrix[row][col] == '/':
                    dx,dy = self.fwrdslash_map[(dx,dy)]
                    beam = (row+dx,col+dy,dx,dy)
                    # ic(beam)
                elif self.matrix[row][col] == '\\':
                    dx,dy = self.backslash_map[(dx,dy)]
                    beam = (row+dx,col+dy,dx,dy)                
            else:
                return
            
    def shoot_beam_from_all_edges(self) -> None:
        #shoot from top row down, and from bottom row up
        for col in range(self.n):
            self.shoot_beam((0,col,1,0))
            self.check_energy(0,col)
            self.shoot_beam((self.m - 1,col,-1,0))
            self.check_energy(self.m-1,col)
        #shoot from left row right, and from right left
        for row in range(self.m):
            self.shoot_beam((row,0,0,1))
            self.check_energy(row,0)
            self.shoot_beam((row,self.n - 1,0,-1))
            self.check_energy(row,self.n-1)


def part1(f_name: str) -> None:
    matrix = utils.generate_matrix(f_name)
    shooter = BeamShooter(matrix)
    shooter.shoot_beam((0,0,0,1))
    print(len(shooter.location_to_beams_map))

def part2(f_name: str) -> None:
    matrix = utils.generate_matrix(f_name)
    shooter = BeamShooter(matrix)
    shooter.shoot_beam_from_all_edges()
    print(f"best start location = {shooter.best_start_loc}")
    print(f"best energy level   = {shooter.best_energy_lvl}")


if __name__ == "__main__":
    start = perf_counter()
    f_names = ["test.txt","input.txt"]
    part1(f_names[1])
    part2(f_names[1])
    end = perf_counter()
    print(f"time: {end-start}")


"""
empty space (.), mirrors (/ and \), and splitters (| and -).

splitters split light if light going perp. ie  light ------> | , if light -----> - : then light just contin
energized = beam passes through the tile

i want to create a matrix and move the light, all the while, keep a dict[Tuple[row,col]: List[Tuple[beam_dx,beam_dy]]] aka the List will have all the beams
that are in that exact spot, as well as their direction via their current dx/dy

new idea, for the default dict, have it map to a set, and add tuples for dx,dy, if that location already had a beam traveling in that dir, then there is no need
to travel it yet again, just return early

find the best configuration for most energized tiles, starting anywhere in top/leftmost/bottom/righmost row then running the algo, 
NOTE corners can start going two dirs, all others just go in opposite dir of row, so for top, start going down, however
topleft can go rightwards or downwards beginning
"""