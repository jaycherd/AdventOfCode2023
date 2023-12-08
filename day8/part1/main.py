from icecream import ic
import re
from typing import Set,Optional,List,Tuple,Dict
from time import perf_counter

def read_file_instr_and_graph(f_name: str) -> str: #graph is altered via ref
    try:
        with open(f_name,'r') as file:
            for line in file:
                instructions = line.strip()
                break
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                graph[line[0:3]] = (line[7:10],line[12:15])

    except FileNotFoundError:
        print(f"file {f_name} not found")

    return instructions





if __name__ == '__main__':
    instructions : str = None
    graph : Dict[str,Tuple[str,str]] = {} #example TFN = (SMC,LQT) will be "TFN" : ("SMC","LQT")
    f_name = "../in.txt"
    step_count = 0

    instructions = read_file_instr_and_graph(f_name=f_name)
    ic(instructions)
    ic(graph)

    current_node = "AAA"
    while current_node != "ZZZ": #because it may take multiple iterations through instructions to get to "ZZZ"
        for instruction in instructions:
            if current_node == "ZZZ":
                break
            if instruction == 'L':
                current_node = graph[current_node][0]
            else:
                current_node = graph[current_node][1]
            step_count += 1
    ic(step_count)
    









"""
XXX DESCRIPTION XXX
format:
example if we get:
RL
AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)

then that means to start from AAA we choose R element aka Right element of the following tuple it maps to, so of (BBB,CCC) we choose CCC cus that the Right element
then we go to CCC and choose Left cus that is the second instruction and CCC = (ZZZ,GGG) ZZZ is left, ZZZ is the goal of where we are trying to go
so we stop traversing at that point

XXX GOAL XXX
follow the instructions and track how many steps it takes to get from AAA to ZZZ, in our example RL, it took two steps to get to ZZZ, right then left

XXX idea XXX
well there are only 750 lines, so i think we could just make the map using the file, then traverse the graph
alternatively we could use less memory by reading the file to find the next node everytime, however it does not seem like
the memory savings would be worth the increased time complexity O(lines*instructions) instead of O(lines + instructions)
"""