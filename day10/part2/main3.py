from dataclasses import dataclass
import numpy as np
import matplotlib.path as pth

with open("../in.txt") as f:
    lines = f.readlines()

# each rule is a pair of tuples representing the
# two grid points this pipe connects
rules = {
    "|": ((0,-1),(0,1)),
    "-": ((-1,0),(1,0)),
    "L": ((0,-1), (1,0)),
    "J": ((0,-1), (-1,0)),
    "7": ((-1,0), (0,1)),
    "F": ((1,0), (0, 1))
}

def apply_rule(rule, at_point, enter_from):
    rule_vector = rules[rule] # look up the rule
    ((rule_ix,rule_iy),(rule_ox,rule_oy)) = rule_vector
    (ax,ay) = at_point
    inbound = ((ax+rule_ix), (ay+rule_iy)) # identify the two endpoints
    outbound = ((ax+rule_ox), (ay+rule_oy))
    if inbound == enter_from: # return the one that *isn't* on our cursor
        return outbound 
    return inbound    

startingPoint = (0,0)

# input size is MAX 140, so we just hardcode that
board = np.zeros((140,140), dtype=str)

# populate the board one character at a time
for y,l in enumerate(lines):
    for x,p in enumerate(l.strip()):
        board[x,y] = p
        if p == "S":
            startingPoint = (x,y)

# find a pipe that connects to our starting point.
# it doesn't matter which direction
cx,cy = startingPoint
if cx-1 >= 0 and board[cx-1,cy] in ['-', 'L', 'F']:
    cx -= 1
elif cx+1 < 140 and board[cx+1,cy] in ['-', 'J', "7"]:
    cx += 1
elif cy-1 >=0 and board[cx,cy-1] in ["|", "7", "F"]:
    cy -= 1
elif cy+1 < 140 and board[cx,cy+1] in ["|", "J", "L"]:
    cy += 1

# build our path
lastPoint = startingPoint
cursor = (cx,cy)
pathLength = 1
path = []
while cursor != startingPoint:    
    cx,cy = cursor
    nextPoint = apply_rule(board[cx,cy], cursor, lastPoint)    
    lastPoint = cursor
    cursor = nextPoint
    pathLength += 1
    path.append(nextPoint)

print(pathLength // 2)

# cheat with matplotlib to find the area
poly = pth.Path(path)
points_inside = 0
points = []
for x in range(140): # by brute force
    for y in range(140):
        if (x,y) not in path:
            points.append((x,y))

inside = poly.contains_points(points)
print(len(inside[inside == True]))