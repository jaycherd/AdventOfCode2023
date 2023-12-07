from icecream import ic
import re


f_name = "day2input.txt"
sumpowers = 0
try:
    with open(f_name,'r') as file:
        for line in file:
            line = line.strip().replace(" ","")
            delimiters = [',', ';', ':']
            pattern = '|'.join(map(re.escape, delimiters))
            game_set = re.split(pattern,line)[1:]
            max_green = 1
            max_red = 1
            max_blue = 1
            for cube_pull in game_set:
                #NOTE i do this in ascending order to avoid possible out of index error - i.e. 1red if you checked if last five are 'green' get index error
                if cube_pull[-3:] == "red":
                    num = int(cube_pull[0:-3])
                    if num > max_red:
                        max_red = num
                elif cube_pull[-4:] == "blue":
                    num = int(cube_pull[0:-4])
                    if num > max_blue:
                        max_blue = num
                else:
                    num = int(cube_pull[0:-5])
                    if num > max_green:
                        max_green = num
            sumpowers += max_red*max_blue*max_green

except FileNotFoundError:
    print(f"file {f_name} not found")

ic(sumpowers)