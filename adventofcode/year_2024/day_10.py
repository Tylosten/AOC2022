""" Day 10 year 2024 """
from argparse import ArgumentParser
from common import get_input

DAY = 10
YEAR = 2024

def get_trailends(grid, trailhead):
    i,j = trailhead
    curr_height = grid[i][j]
    trailends = []
    for nexti, nextj in [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]:
        if nexti < 0 or nexti >= len(grid) or nextj < 0 or nextj >= len(grid[0]):
            continue
        next_height = grid[nexti][nextj]
        if next_height != curr_height + 1:
            continue
        if next_height == 9:
            trailends.append((nexti, nextj))
        else :
            trailends += get_trailends(grid, (nexti, nextj))
    return set(list(trailends))

def get_trail_nb(grid, trailhead):
    i,j = trailhead
    curr_height = grid[i][j]
    trail_nb = 0
    for nexti, nextj in [(i+1,j), (i-1,j), (i,j+1), (i,j-1)]:
        if nexti < 0 or nexti >= len(grid) or nextj < 0 or nextj >= len(grid[0]):
            continue
        next_height = grid[nexti][nextj]
        if next_height != curr_height + 1:
            continue
        if next_height == 9:
            trail_nb += 1
        else :
            trail_nb += get_trail_nb(grid, (nexti, nextj))
    return trail_nb


def solve_part1(example = False):
    inpt = get_input(DAY, YEAR, example)
    grid = [[int(c) for c in line] for line in inpt]
    trailheads = [(i,j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 0]
    resum = 0
    for trailhead in trailheads:
        trailends = get_trailends(grid, trailhead)
        resum += len(trailends)
    return resum

def solve_part2(example = False):
    inpt = get_input(DAY, YEAR, example)
    grid = [[int(c) for c in line] for line in inpt]
    trailheads = [(i,j) for i in range(len(grid)) for j in range(len(grid[0])) if grid[i][j] == 0]
    resum = 0
    for trailhead in trailheads:
        resum += get_trail_nb(grid, trailhead)
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
