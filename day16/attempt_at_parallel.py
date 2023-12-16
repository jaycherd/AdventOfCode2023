from icecream import ic
from typing import List,Tuple,Dict,Counter,TypeVar,Generator,Set
import utils
from collections import defaultdict
from time import perf_counter
from concurrent.futures import ThreadPoolExecutor, as_completed


class BeamShooter:
    def __init__(self,matrix: List[List[str]]):
        self.matrix = matrix
        self.m = len(matrix)
        self.n = len(matrix[0])
        self.backslash_map = {(0,1) : (1,0), (0,-1) : (-1,0), (1,0) : (0,1), (-1,0) : (0,-1)}
        self.fwrdslash_map = {(0,1) : (-1,0),(0,-1) : (1,0),  (1,0) : (0,-1),(-1,0) : (0,1)}
        self.horizontal_dirs = {(0,1),(0,-1)}
        self.vertical_dirs = {(1,0),(-1,0)}
        self.best_start_loc = (-1,-1)
        self.best_energy_lvl = -1
        

    def beam_valid(self,row: int,col: int) -> bool:
        return row < self.m and row >= 0 and col < self.n and col >= 0
    
    def is_corner(self,i: int, j: int) -> bool:
        return (i==0 and j==0) or (i==self.m-1 and j==self.n-1) or (i==0 and j==self.n-1) or (i==self.m-1 and j==0)
    
    def check_energy(self,row: int,col: int,location_to_beams_map) -> None:
        energy = len(location_to_beams_map)
        if energy > self.best_energy_lvl:
            self.best_energy_lvl = energy
            self.best_start_loc = (row,col)
        location_to_beams_map.clear()


    def shoot_beam(self, beam: Tuple[int,int,int,int],location_to_beams_map : Dict[Tuple[int,int],Set[Tuple[int,int]]]) -> Dict[Tuple[int,int],Set[Tuple[int,int]]]:
        while True:
            row,col,dx,dy = beam
            if (row,col) in location_to_beams_map and (dx,dy) in location_to_beams_map[(row,col)]:
                return location_to_beams_map #basically this means, a beam already traveled this path, lets not trav it again
            # ic(beam)
            if self.beam_valid(row,col):
                location_to_beams_map[(row,col)].add((dx,dy)) #i'm going to have the direction, as the direction, the light enters a given square
                if self.matrix[row][col] == '.':
                    beam = (row+dx,col+dy,dx,dy)
                elif self.matrix[row][col] == '|': #split ew
                    if (dx,dy) in self.horizontal_dirs: #then we must split
                        location_to_beams_map = self.shoot_beam((row-1,col,-1,0),location_to_beams_map) #shoot one up
                        location_to_beams_map = self.shoot_beam((row+1,col,1,0),location_to_beams_map) #shoot one down
                        return location_to_beams_map #so it looks neat, i shoot both and once both are done, we return
                    else: #else beam continues on the same path
                        beam = (row+dx,col+dy,dx,dy)
                elif self.matrix[row][col] == '-':
                    if (dx,dy) in self.vertical_dirs:
                        location_to_beams_map = self.shoot_beam((row,col-1,0,-1),location_to_beams_map) #shoot one left
                        location_to_beams_map = self.shoot_beam((row,col+1,0,1),location_to_beams_map)  #shoot one right
                        return location_to_beams_map
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
                return location_to_beams_map
            
    def shoot_beam_from_all_edges(self) -> None:
        with ThreadPoolExecutor() as executor:
            futures = []
            #shoot from top row down, and from bottom row up
            for col in range(self.n):
                futures.append(executor.submit(self.shoot_beam, (0,col,1,0),defaultdict(set)))
                futures.append(executor.submit(self.shoot_beam, (self.m - 1,col,-1,0),defaultdict(set)))
            #shoot from left row right, and from right left
            for row in range(self.m):
                futures.append(executor.submit(self.shoot_beam, (row,0,0,1),defaultdict(set)))
                futures.append(executor.submit(self.shoot_beam, (row,self.n - 1,0,-1),defaultdict(set)))
            
            for future in as_completed(futures):
                location_to_beams_map = future.result()
                self.check_energy(-1,-1,location_to_beams_map)


def part1(f_name: str) -> None:
    matrix = utils.generate_matrix(f_name)
    shooter = BeamShooter(matrix)
    location_to_beams_map = shooter.shoot_beam((0,0,0,1),defaultdict(set))
    print(f"part1:\ne_level = {len(location_to_beams_map)}")

def part2(f_name: str) -> None:
    matrix = utils.generate_matrix(f_name)
    shooter = BeamShooter(matrix)
    shooter.shoot_beam_from_all_edges()
    print(f"part2:\nbest start location = {shooter.best_start_loc}")
    print(f"best energy level   = {shooter.best_energy_lvl}")


if __name__ == "__main__":
    start = perf_counter()
    f_names = ["test.txt","input.txt"]
    part1(f_names[1])
    part2(f_names[1])
    end = perf_counter()
    print(f"time: {end-start}")


