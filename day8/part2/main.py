from icecream import ic
import re
from typing import Set,Optional,List,Tuple,Dict
from time import perf_counter
from collections import deque
import math
from functools import reduce

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

def find_nodes_ending_A() -> List[str]:
    res = []
    for node in graph.keys():
        if node[2] == 'A':
            res.append(node)
    return res

def calc_steps(node: str) -> int:
    steps = 0
    while node[2] != 'Z': #because it may take multiple iterations through instructions to get to "ZZZ"
        for instruction in instructions:
            if node[2] == "Z":
                return steps
            if instruction == 'L':
                node = graph[node][0]
            else:
                node = graph[node][1]
            steps += 1
    return steps

def lcm(a: int,b: int) -> int:
    return abs(a*b) // math.gcd(a,b)

def lcm_of_lst(numbers: List[int]) -> int:
    return reduce(lcm,numbers)




if __name__ == '__main__':
    instructions : str = None
    graph : Dict[str,Tuple[str,str]] = {} #example TFN = (SMC,LQT) will be "TFN" : ("SMC","LQT")
    f_name = "../in.txt"
    step_count = 0
    start_nodes : List[str] = []
    steps_required : List[int] = [] #will run parallel to start nodes tracking how many steps to get to ZZZ

    instructions = read_file_instr_and_graph(f_name=f_name)
    ic(instructions)
    ic(graph)

    start_nodes = find_nodes_ending_A()
    ic(start_nodes)

    for start_node in start_nodes:
        steps_required.append(calc_steps(node=start_node))
    ic(steps_required)
    res = lcm_of_lst(steps_required)
    ic(res)


"""
XXX MODIFICATION XXX
start from all the nodes that end in A, then traverse all those simulataneously, based on the instruction, and continue to do this
until every node that you are on ends with Z

XXX idea XXX
use a queue, start by finding all the nodes that end with A and add all those to the queue, then look at queue len, pop everything
that is currently in the queue, traverse and add those results all back to the queue, everytime have a flag, that starts as true, which if 
you come across a NON-Z ending node change to False, if the flag is True at the end of a node processing, then all the nodes you just added
must be Z at the end, so we have found the solution, otherwise continue with the queue process

NOTE: coded this, i think it is working, however, if they are taking thousands of steps each, then the num of steps they will all be Z, could
be an INSANE number, therefore, how about instead, we individually find the step count for all the nodes, then we can find the lowest common multiple
of all the nodes that we are considering, which just requires math instead of a zillion operations

NOTE on python reduce function: it takes a list of items, looks at two of them at a time, does whatever you tell it to do with them, then that combination
becomes the result it uses to look at the next item, and so on, [0,1,2,3] then [0,1] used to become [0] and that result is used to compute [0] again
but this time with the value result from [0,1] and [2] and so on
"""