""" Day 3 year 2024 """
from argparse import ArgumentParser
import re
from common import get_input

DAY = 3
YEAR = 2024

REGEX = r"mul\((\d{1,3}),(\d{1,3})\)"

def process_muls(line):
    resum = 0
    for match in re.finditer(REGEX, line):
        resum += int(match.group(1)) * int(match.group(2))
    return resum

def solve_part1(example = False):
    inpt = get_input(DAY, YEAR, example)
    resum = 0
    inpt = "".join(inpt)
    return process_muls(inpt)

def solve_part2(example = False):
    inpt = get_input(DAY, YEAR, example)
    inpt = "".join(inpt)
    splt = inpt.split("do()")
    splt = [s.split("don't()")[0] for s in splt]
    return sum(process_muls(s) for s in splt)

if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("-e", "--example", action="store_true")
    argparser.add_argument("-p", "--part", type=int, choices=[1, 2], default=1)
    args = argparser.parse_args()

    if args.part == 1:
        print(solve_part1(args.example))
    else:
        print(solve_part2(args.example))
