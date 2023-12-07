from copy import deepcopy
import re
from adventofcode.year_2023.puzzle2023 import Puzzle2023

class Puzzle4(Puzzle2023):
    def __init__(self):
        super().__init__(4)
        
    def parse_input(self):
        res = {}
        for line in self.input:
            match = re.match(r'Card *(\d+):', line)
            if match is None:
                continue
            id = int(match.group(1))
            res[id] = [[int(nbstr) for nbstr in nblist.strip().split(' ') if nbstr != ''] for nblist in line.split(':')[1].split('|') ]
        return res
    
    def run_part1(self):
        points = 0
        for card in self.parsed_input.values():
            win = [nb for nb in card[1] if nb in card[0]]
            if len(win) > 0:
                points += 2**(len(win)-1)
        return points
            
    def what_to_add(self, id, card):
        win_nb = len([nb for nb in card[1] if nb in card[0]])
        return [id + i + 1 for i in range(win_nb)]

    def nb_of_cards(self, id, adding, nb_cards):
        what_to_add = adding[id]
        count = 1
        for to_add in what_to_add:
            if to_add in nb_cards:
                count += nb_cards[to_add]
            else :
                return None
        return count
        

    def run_part2(self):
        adding = {id : self.what_to_add(id, card) for id, card in self.parsed_input.items()}
        
        nb_cards = {}
        while len(nb_cards) < len(self.parsed_input):
            nb_cards = {id: self.nb_of_cards(id, adding, nb_cards) for id in self.parsed_input.keys()}
            nb_cards = {id: nb for id, nb in nb_cards.items() if nb is not None}
            print(nb_cards)
        
        return sum(nb_cards.values())

puzzle = Puzzle4()
puzzle.run()