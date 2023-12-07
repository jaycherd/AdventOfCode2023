from icecream import ic
import re


f_name = "day2input.txt"
id_sum = 0
MAX_RED = 12
MAX_GREEN = 13
MAX_BLUE = 14
id = 1
try:
    with open(f_name,'r') as file:
        for line in file:
            line = line.strip().replace(" ","")
            delimiters = [',', ';', ':']
            pattern = '|'.join(map(re.escape, delimiters))
            game_set = re.split(pattern,line)[1:]
            add_this_set = True
            for cube_pull in game_set:
                #NOTE i do this in ascending order to avoid possible out of index error - i.e. 1red if you checked if last five are 'green' get index error
                if cube_pull[-3:] == "red":
                    num = int(cube_pull[0:-3])
                    if num > MAX_RED:
                        add_this_set = False
                        break
                elif cube_pull[-4:] == "blue":
                    num = int(cube_pull[0:-4])
                    if num > MAX_BLUE:
                        add_this_set = False
                        break
                else:
                    num = int(cube_pull[0:-5])
                    if num > MAX_GREEN:
                        add_this_set = False
                        break
            if add_this_set:
                id_sum += id
            id += 1

except FileNotFoundError:
    print(f"file {f_name} not found")

ic(id_sum)