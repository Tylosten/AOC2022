""" Day 6 year 2024 """
from argparse import ArgumentParser
from common import get_input

DAY = 6
YEAR = 2024
UP = [-1, 0]
DOWN = [1, 0]
LEFT = [0, -1]
RIGHT = [0, 1]

def go_to_next_obstacle(grid, pos, direction):
    # print(f"Moving from {pos} in direction {direction}")
    i,j = pos
    oldi, oldj = i,j
    while True:
        i += direction[0]
        j += direction[1]
        if i < 0 or j < 0 or i >= len(grid) or j >= len(grid[0]):
            return None
        if grid[i][j] == "#":
            return (oldi, oldj)
        oldj = j
        oldi = i
        grid[i][j] = "X"

def print_grid(grid):
    for row in grid:
        print("".join(row))

def solve_part1(example = False):
    inpt = get_input(DAY, YEAR, example)
    grid = [[char for char in line] for line in  inpt]
    startpos = None
    startdir = None
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == ">":
                startdir = RIGHT
                startpos = (i,j)
                break
            if cell == "<":
                startdir = LEFT
                startpos = (i,j)
                break
            if cell == "^":
                startdir = UP
                startpos = (i,j)
                break
            if cell == "v":
                startdir = DOWN
                startpos = (i,j)
                break
    while startpos is not None:
        startpos = go_to_next_obstacle(grid, startpos, startdir)
        # turn right
        startdir = [startdir[1], -startdir[0]]
    # print_grid(grid)
    return sum(row.count("X") for row in grid) + 1

def check_no_obs_between(grid, pt1, pt2):
    if pt1[0] == pt2[0]:
        for j in range(min(pt1[1], pt2[1]), max(pt1[1], pt2[1])):
            if grid[pt1[0]][j] == "#":
                return False
    if pt1[1] == pt2[1]:
        for i in range(min(pt1[0], pt2[0]), max(pt1[0], pt2[0])):
            if grid[i][pt1[1]] == "#":
                return False
    return True

def is_grid_looping(grid, startpos, startdir):     
    obstacles = []
    while True :
        startpos = go_to_next_obstacle(grid, startpos, startdir)
        if startpos is None :
            return grid, False
        obs = {
            "pos" : startpos,
            "dir" : startdir
        }
        if obs in obstacles :
            return grid, True
        obstacles.append(obs)
        # turn right
        startdir = [startdir[1], -startdir[0]]

def solve_part2(example = False):
    inpt = get_input(DAY, YEAR, example)
    grid = [[char for char in line] for line in  inpt]
    startpos = None
    startdir = None
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == ">":
                startdir = RIGHT
                startpos = (i,j)
                break
            if cell == "<":
                startdir = LEFT
                startpos = (i,j)
                break
            if cell == "^":
                startdir = UP
                startpos = (i,j)
                break
            if cell == "v":
                startdir = DOWN
                startpos = (i,j)
                break
            
    grid, looping = is_grid_looping(grid, startpos, startdir)
    
    resum = 0
    for i, row in enumerate(grid) :
        for j, cell in enumerate(row) :
            if cell == "X" :
                grid_copy = [row.copy() for row in grid]
                grid_copy[i][j] = "#"
                _, looping = is_grid_looping(grid_copy, startpos, startdir)
                if looping :
                    resum += 1
    return resum

if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("-e", "--example", action="store_true")
    argparser.add_argument("-p", "--part", type=int, choices=[1, 2], default=1)
    args = argparser.parse_args()

    if args.part == 1:
        print(solve_part1(args.example))
    else:
        print(solve_part2(args.example))

# 6,3   7,6   7,7    8,1  8,3 9,7