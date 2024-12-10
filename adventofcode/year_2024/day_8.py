""" Day 8 year 2024 """
from argparse import ArgumentParser
from common import get_input

DAY = 8
YEAR = 2024

def get_antinodes(pos1, pos2, max_i, max_j):
    antinode_1 = (2*pos2[0] - pos1[0], 2*pos2[1] - pos1[1])
    antinode_2 = (2*pos1[0] - pos2[0], 2*pos1[1] - pos2[1])
    res = []
    if is_antinode_in_grid(antinode_1, max_i, max_j):
        res.append(antinode_1)
    if is_antinode_in_grid(antinode_2, max_i, max_j):
        res.append(antinode_2)
    return res
    
def is_antinode_in_grid(antinode, max_i, max_j):
    return 0 <= antinode[0] < max_i and 0 <= antinode[1] < max_j
    
def get_antennas(inpt):
    antennas= {}
    for i, row in enumerate(inpt):
        for j, cell in enumerate(row):
            if cell !=".":
                if cell not in antennas : 
                    antennas[cell] = [(i,j)]
                else:
                    antennas[cell].append((i,j))
    return antennas

def solve_part1(example = False):
    inpt = get_input(DAY, YEAR, example)
    row_nb = len(inpt)
    col_nb = len(inpt[0])
    print(f"Row number: {row_nb}, col number: {col_nb}")
    antennas = get_antennas(inpt)
    
    antinodes = []
    for antennas_pos in antennas.values():
        for i, pos1 in enumerate(antennas_pos):
            for j, pos2 in enumerate(antennas_pos):
                if i < j:
                    antinodes += get_antinodes(pos1, pos2, row_nb, col_nb)
    return len(list(set(antinodes)))

def get_antinodes2(pos1, pos2, max_i, max_j):
    diff = (pos2[0] - pos1[0], pos2[1] - pos1[1])
    # print(f'pos1: {pos1}, pos2: {pos2}, diff: {diff}')
    antinodes = []
    i = 0
    while True:
        antinode = (pos1[0] + i*diff[0], pos1[1] + i*diff[1])
        # print(f'   i {i}, antinode: {antinode} ({pos1[0]} + {i}*{diff[0]}, {pos1[1]} + {i}*{diff[1]})')
        if is_antinode_in_grid(antinode, max_i, max_j):
            antinodes.append(antinode)
        else:
            break
        i += 1
    i = 1
    while True :
        antinode = (pos1[0] - i*diff[0], pos1[1] - i*diff[1])
        if is_antinode_in_grid(antinode, max_i, max_j):
            antinodes.append(antinode)
        else:
            break
        i += 1
    return antinodes

def solve_part2(example = False):
    inpt = get_input(DAY, YEAR, example)
    row_nb = len(inpt)
    col_nb = len(inpt[0])
    print(f"Row number: {row_nb}, col number: {col_nb}")
    antennas = get_antennas(inpt)
    
    antinodes = []
    for antennas_pos in antennas.values():
        for i, pos1 in enumerate(antennas_pos):
            for j, pos2 in enumerate(antennas_pos):
                if i < j:
                    antinodes += get_antinodes2(pos1, pos2, row_nb, col_nb)
    return len(list(set(antinodes)))

if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("-e", "--example", action="store_true")
    argparser.add_argument("-p", "--part", type=int, choices=[1, 2], default=1)
    args = argparser.parse_args()

    if args.part == 1:
        print(solve_part1(args.example))
    else:
        print(solve_part2(args.example))
