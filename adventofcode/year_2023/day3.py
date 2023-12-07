import re
from adventofcode.year_2023.puzzle2023 import Puzzle2023

class Puzzle3(Puzzle2023):
    def __init__(self):
        super().__init__(3)
        
        
    def run_part1(self):
        res = 0
        for i, line in enumerate(self.parsed_input):
            for match in re.finditer(r'(\d+)', line) :
                jstart = max(match.start() - 1, 0)
                jend = min(match.end() + 1 , len(line))
                for ineigh in range(i-1, i+2):
                    if ineigh < 0 or ineigh >= len(self.parsed_input):
                        continue
                    if re.search(r'[^\d\.]', self.parsed_input[ineigh][jstart:jend]) :
                        res += int(match.groups()[0])
                        break
        return res

    def run_part2(self):
        gears = {}
        for i, line in enumerate(self.parsed_input):
            for match in re.finditer(r'(\d+)', line) :
                jstart = max(match.start() - 1, 0)
                jend = min(match.end() + 1 , len(line))
                for ineigh in range(i-1, i+2):
                    if ineigh < 0 or ineigh >= len(self.parsed_input):
                        continue
                    gear_match = re.search(r'\*', self.parsed_input[ineigh][jstart:jend]) 
                    if gear_match :
                        gear_coords = (ineigh, gear_match.start() + jstart)
                        if gear_coords not in gears:
                            gears[gear_coords] = []
                        gears[gear_coords].append(int(match.groups()[0]))
        return sum(gear[0] * gear[1] for gear in gears.values() if len(gear) == 2)
        

puzzle = Puzzle3()
puzzle.run()