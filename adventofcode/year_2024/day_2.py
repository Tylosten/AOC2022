""" Day 2 year 2024 """
from argparse import ArgumentParser
import numpy as np
from common import get_input


DAY = 2
YEAR = 2024

def is_safe(arr):
    diff = np.array([arr[0]] + arr) - np.array(arr + [arr[-1]])
    diff = diff[1:-1]
    absdiff = np.abs(diff)
    return  min(absdiff) >= 1 and max(absdiff) <= 3 and (all(diff > 0) or all(diff < 0))

def solve_part1(example = False):
    inpt = get_input(DAY, YEAR, example)
    ressum = 0
    for line in inpt:
        arr = [int(x) for x in line.split()]
        if is_safe(arr):
            ressum += 1
    return ressum

def is_safe_lesser(arr):
    if is_safe(arr):
        return True
    for i in range(len(arr)):
        if is_safe(arr[:i] + arr[i+1:]):
            return True
    return False

def solve_part2(example = False):
    inpt = get_input(DAY, YEAR, example)
    ressum = 0
    for line in inpt:
        arr = [int(x) for x in line.split()]
        if is_safe_lesser(arr):
            ressum += 1
    return ressum


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("-e", "--example", action="store_true")
    argparser.add_argument("-p", "--part", type=int, choices=[1, 2], default=1)
    args = argparser.parse_args()

    if args.part == 1:
        print(solve_part1(args.example))
    else:
        print(solve_part2(args.example))
