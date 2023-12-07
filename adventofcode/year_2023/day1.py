import re
from copy import deepcopy
from adventofcode.year_2023.puzzle2023 import Puzzle2023

class Puzzle1(Puzzle2023):
    def __init__(self):
        super().__init__(1)
        
    def run_part1(self):
        numbers = [re.sub(r'[a-z]', '', code) for code in self.parsed_input]
        return sum(int(number[0] + number[-1]) for number in numbers)
    
    def search_first_nb(self, string):
        return self.from_str_to_int(re.search(r'(\d|one|two|three|four|five|six|seven|eight|nine)', string).groups()[0])
    
    def search_last_nb(self, string):
        return self.from_str_to_int(re.search(r'(\d|eno|owt|eerht|ruof|evif|xis|neves|thgie|enin)', string[::-1]).groups()[0][::-1])
    
    def from_str_to_int(self, string):
        subs = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
                'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',}
        if string in subs:
            return subs[string]
        return string
    
    def run_part2(self):
        return sum( int(self.search_first_nb(code) + self.search_last_nb(code)) for code in self.parsed_input)
            
        
puzzle = Puzzle1()
puzzle.run()