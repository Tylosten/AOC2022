from adventofcode.year_2023.puzzle2023 import Puzzle2023
import re
import math

class Puzzle8(Puzzle2023):
    def __init__(self):
        super().__init__(8)

    def parse_input(self):
        res = {}
        instructions = self.input[0].strip()
        for line in self.input:
            match = re.match(r'([A-Z1-9]*) = \(([A-Z1-9]*), ([A-Z1-9]*)\)', line)
            if match :
                res[match.group(1)] = (match.group(2), match.group(3))
                
        return instructions, res
    
    
    def get_count(self, start, instructions, data) : 
        counter = 0
        choice = data[start]
        while True : 
            for inst in instructions :
                counter += 1
                next = choice[0 if inst == 'L' else 1]
                if next[-1] == 'Z' :
                    return counter
                choice = data[next]
    
    def run_part1(self,):
        instructions, data = self.parsed_input
        return self.get_count('AAA', instructions, data)
                
    def run_part2(self):
        instructions, data = self.parsed_input
        starts = [k for k in data.keys() if k[-1] == 'A']
        counts = [self.get_count(start, instructions, data) for start in starts]
        print(counts)
        return math.lcm(*counts)
            

puzzle = Puzzle8()
puzzle.run()