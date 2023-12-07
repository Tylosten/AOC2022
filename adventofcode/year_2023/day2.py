import re
from adventofcode.year_2023.puzzle2023 import Puzzle2023

class Puzzle2(Puzzle2023):
    def __init__(self):
        super().__init__(2)
        
    def parse_input(self):
        games = []        
        for game_str in self.input:
            if not game_str.startswith('Game'):
                continue
            game = {}
            game['id'] = int(re.match(r'Game (\d+)', game_str).groups()[0])
            sets = game_str.split(':')[1].split(';')
            game['sets'] = []
            for set_str in sets:
                set_obj = {}
                for color in ['red', 'green', 'blue']:
                    match = re.search(r'(\d+) '+ color, set_str)
                    set_obj[color] = int(match.groups()[0]) if match else 0
                game['sets'].append(set_obj)
            games.append(game)
            print(game)  
        return games
    
    def is_set_possible(self, setobj, max_blue, max_green, max_red):
        return setobj['blue'] <= max_blue and setobj['green'] <= max_green and setobj['red'] <= max_red
    
    def run_part1(self):
        max_red = 12
        max_green = 13
        max_blue = 14
        return sum(game['id'] for game in self.parsed_input if all(self.is_set_possible(setobj, max_blue, max_green, max_red) for setobj in game['sets']))
    
    def run_part2(self):
        power = 0
        for game in self.parsed_input:
            max_set = game['sets'][0]
            for setobj in game['sets'][1:]:
                for color in ['blue', 'green', 'red']:
                    max_set[color] = max(max_set[color], setobj[color])
            power += max_set['blue'] * max_set['green'] * max_set['red']
        return power
                
    
puzzle = Puzzle2()
puzzle.run()