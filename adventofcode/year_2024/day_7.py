""" Day 7 year 2024 """
from argparse import ArgumentParser
from common import get_input
import re 

DAY = 7
YEAR = 2024
REGEX = r'(\d+): ([\d ]+)'

def solve_part1(example = False):
    inpt = get_input(DAY, YEAR, example)
    resum = 0
    for line in inpt :
        match = re.match(REGEX, line)
        if match :
            test_res = int(match.group(1))
            numbers = [int(item) for item in match.group(2).split()]
            possibilities = [numbers[0]]
            for number in numbers[1:]:
                new_possibilities = []
                for possibility in possibilities:
                    new_possibilities.append(possibility + number)
                    new_possibilities.append(possibility * number)
                possibilities = [poss for poss in new_possibilities if poss <= test_res]
            if any(poss == test_res for poss in possibilities):
                resum += test_res
    return resum

def solve_part2(example = False):
    inpt = get_input(DAY, YEAR, example)
    resum = 0
    for line in inpt :
        match = re.match(REGEX, line)
        if match :
            test_res = int(match.group(1))
            numbers = [int(item) for item in match.group(2).split()]
            possibilities = [numbers[0]]
            for number in numbers[1:]:
                new_possibilities = []
                for possibility in possibilities:
                    new_possibilities.append(possibility + number)
                    new_possibilities.append(possibility * number)
                    new_possibilities.append(int(str(possibility) + str(number)))
                possibilities = [poss for poss in new_possibilities if poss <= test_res]
            if any(poss == test_res for poss in possibilities):
                resum += test_res
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
