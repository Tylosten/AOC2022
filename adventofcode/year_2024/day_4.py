""" Day 4 year 2024 """
from argparse import ArgumentParser
from common import get_input
import re

DAY = 4
YEAR = 2024
WORLD = r"XMAS"

def find_horizontal(puzzle, word):
    resum = 0
    for line in puzzle:
        resum += len(re.findall(word, line))
        resum += len(re.findall(word[::-1], line))
    return resum

def find_vertical(puzzle, word):
    # transpose the puzzle
    trsp = [''.join(arr) for arr in  list(zip(*puzzle))]
    return find_horizontal(trsp, word)

def find_diagonal(puzzle, word):
    # construct diagonals 
    diags_nb = len(puzzle) + len(puzzle[0]) - 1
    diags = ['' for _ in range(diags_nb)]
    diags2 = ['' for _ in range(diags_nb)]
    for i, line in enumerate(puzzle):
        for j, char in enumerate(line):
            diag1 = j - i + len(puzzle) - 1
            diag2 = j + i
            diags[diag1] += char
            diags2[diag2] += char
    return find_horizontal(diags, word) + find_horizontal(diags2, word)

def solve_part1(example = False):
    inpt = get_input(DAY, YEAR, example)
    return find_horizontal(inpt, WORLD) + find_vertical(inpt, WORLD) + find_diagonal(inpt, WORLD)

def search_x_mas(puzzle):
    resum = 0
    for i, line in enumerate(puzzle) :
        if i > len(puzzle) - 3:
            continue
        for match in re.finditer(r'(?=([MS].[MS]))', line):
            match_index = match.start()
            if puzzle[i + 1][match_index + 1] != 'A':
                continue
            match2 = re.match(r'([MS].[MS])', puzzle[i + 2][match_index:match_index+3])
            if match2 is not None and match2.group(1)[0] != match.group(1)[-1] and match2.group(1)[-1] != match.group(1)[0]:
                resum += 1
    return resum

def solve_part2(example = False):
    inpt = get_input(DAY, YEAR, example)
    return search_x_mas(inpt)

if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("-e", "--example", action="store_true")
    argparser.add_argument("-p", "--part", type=int, choices=[1, 2], default=1)
    args = argparser.parse_args()

    if args.part == 1:
        print(solve_part1(args.example))
    else:
        print(solve_part2(args.example))
