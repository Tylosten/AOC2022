""" Day 5 year 2024 """
from argparse import ArgumentParser
from common import get_input
import re 

DAY = 5
YEAR = 2024


def parse_input(inpt): 
    regex = r'(\d+)\|(\d+)'
    rules = []
    updates = []
    for line in inpt : 
        if line == "":
            continue
        match = re.match(regex, line)
        if match : 
            rules.append((int(match.group(1)), int(match.group(2))))
        else : 
            updates.append([int(nb) for nb in line.split(',')])
    return rules, updates

def is_order_ok(update, rules):
    currules = [r for r in rules if r[0] in update and r[1] in update]
    for rule in currules:
        if update.index(rule[0]) > update.index(rule[1]):
            return False
    return True

def middle_nb(update):
    if len(update) % 2 == 1:
        return update[len(update) // 2]
    raise ValueError("Update length is not odd")

def solve_part1(example = False):
    inpt = get_input(DAY, YEAR, example)
    rules, updates = parse_input(inpt)
    resum = 0
    for upd in updates :
        if is_order_ok(upd, rules) : 
            resum += middle_nb(upd)
    return resum

def get_possible_order(update, rules) : 
    currules = {p : [] for p in update} 
    for r in rules : 
        if r[0] in update and r[1] in update :
            currules[r[0]].append(r[1])
    new_order = []
    while len(new_order) != len(update) :
        free_pages = [page for page in update if len(currules.get(page)) == 0 and page not in new_order]
        if len(free_pages) == 0 :
            break
        new_order = free_pages + new_order
        # print("update", update, 'free_pages', free_pages, ", currules ", currules, "new_order", new_order)
        currules = {k: [v for v in currules[k] if v not in new_order] for k in currules}
    if len(new_order) != len(update) :
        raise ValueError("Can't find a possible order")
    return new_order
            

def solve_part2(example = False):
    inpt = get_input(DAY, YEAR, example)
    rules, updates = parse_input(inpt)
    resum = 0
    for upd in updates :
        if not is_order_ok(upd, rules) : 
            resum += middle_nb(get_possible_order(upd, rules))
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
