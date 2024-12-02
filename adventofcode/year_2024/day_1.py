""" Day 1 year 2024 """
from argparse import ArgumentParser
from common import get_input
import re
import numpy as np

DAY = 1
YEAR = 2024

def get_lists(inpt):
    regex = re.compile(r"(\d+)   (\d+)")
    arr1 = []
    arr2 = []
    for line in inpt:
        match = regex.match(line)
        if match:
            arr1.append(int(match.group(1)))
            arr2.append(int(match.group(2)))
    return arr1, arr2

def solve_part1(example = False):
    inpt = get_input(DAY, YEAR, example)
    arr1, arr2 = get_lists(inpt)
    arr1 = sorted(arr1)
    arr2 = sorted(arr2)
    diff = [abs(arr1[i] - arr2[i]) for i in range(len(arr1))]
    return sum(diff)

def solve_part2(example = False):
    inpt = get_input(DAY, YEAR, example)
    arr1, arr2 = get_lists(inpt)
    
    res = 0
    for item in arr1 : 
        res += sum(item2 == item for item2 in arr2) * item
    
    return res


if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("-e", "--example", action="store_true")
    argparser.add_argument("-p", "--part", type=int, choices=[1, 2], default=1)
    args = argparser.parse_args()
    
    if args.part == 1:
        print(solve_part1(args.example))
    else:
        print(solve_part2(args.example))