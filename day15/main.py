from icecream import ic
from typing import List,Tuple,Dict,Counter,TypeVar,Generator
import numpy as np
from collections import defaultdict
from time import perf_counter


def get_next_str(f_name: str) -> Generator[str,None,None]:
    try:
        with open(f_name,'r')as file:
            curr_str = ""
            while True:
                char = file.read(1) #reads a single byte(char) at a time, no need to read all file in at once, just the current string
                if not char:
                    #end of file then
                    if curr_str:
                        yield curr_str.strip()
                    break
                if char != ',':
                    curr_str += char
                else: #we hit our separator, so return our curr_str
                    yield curr_str.strip()
                    curr_str = ""
    except FileNotFoundError:
        print(f"file {f_name} not found")
    return None

def custom_hash(s: str) -> int:
    curr_val = 0
    multiplier,modder = 17,256
    for ch in s:
        curr_val += ord(ch)
        curr_val *= multiplier
        curr_val = curr_val % modder
    return curr_val

def hash_for_label(s: str) -> Tuple[int,str,str]:
    curr_val,curr_str = 0,""
    multiplier,modder = 17,256
    stop_chars = {'-','='}
    for ch in s:
        if ch not in stop_chars:
            curr_val += ord(ch)
            curr_val *= multiplier
            curr_val = curr_val % modder
            curr_str += ch
        else:
            op = ch
            break
    return (curr_val,curr_str,op)


def part1(f_name: str) -> None:
    res = 0
    for s in get_next_str(f_name):
        res += custom_hash(s)
    ic(f_name,res)

def do_op(my_map : Dict[int,Dict[str,int]], box: int, label: str, op: str, s: str) -> None:
    if op == '=':
        my_map[box][label] = s.split('=')[1]
    elif op == '-':
        if label in my_map[box]:
            del my_map[box][label]
        
def focus(box_num: int,slot: int,focal: int) -> int:
    return (box_num+1)*(slot)*(focal)

def defaultdict_of_int():
    return defaultdict(int)

def part2(f_name: str) -> None:
    box_num_to_label_str_map : Dict[int,Dict[str,int]] = defaultdict(defaultdict_of_int) #Dict{box_num : Dict{label_str : focal_len}}
    for s in get_next_str(f_name):
        box_num,lens_label_str,op = hash_for_label(s) #label = box number to do stuff at
        do_op(box_num_to_label_str_map,box_num,lens_label_str,op,s)
        # ic(s,box_num,lens_label_str)
    # print(len(box_num_to_label_str_map)) #not 256 items in here, so collisions..?
    print(box_num_to_label_str_map)
    focusing_power = 0
    for box_num,dict in box_num_to_label_str_map.items():
        for i,(label,focal) in enumerate(dict.items()):
            # ic(box_num,label,focal,i+1)
            focusing_power += focus(box_num,i+1,int(focal))
    ic(focusing_power)




if __name__ == "__main__":
    start = perf_counter()
    f_names = ["test.txt","test2.txt","input.txt"]
    # part1(f_names[0])
    # part1(f_names[1])
    # part1(f_names[2])
    part2(f_names[1])
    part2(f_names[2])
    end = perf_counter()
    print(f"time: {end-start}")

"""
part2 - operation characters:
dash(-) = go to relevant box and rm the lens with the given label if it is present, then move errything else forwards asfaraspossible
equals(=) = will be followed by a num indicating the focal length of the lens that needs to go into the relevant box
NOTE: the relevant boxes is what we got in the beginning from the hash value, the boxes are 0-255
lens labels = 1-9, it is indicated by the sequence of letters in the start; 
run hash algo on the letters in the beginning, aka what comes before the (-) or (=) to find out WHICH label, the operation
will be performed on, label i believe corresponds to the 1-9 focal length? it seems so

AFTER TESTING
BOX NUM -> can be found by hashing the label (the chars before the =/-)
FOCAL LENGTH -> the minus and dash is followed by the FOCAL LENGTH
LABEL ->  the chars before the (=/-)


"""