from math import ceil, floor
from adventofcode.year_2023.puzzle2023 import Puzzle2023
from sympy import symbols, Eq, solve

class Puzzle6(Puzzle2023):
    def __init__(self):
        super().__init__(6)
        
    def parse_input(self):
        for line in self.input:
            if line.startswith('Time:') :
                times = [int(nb) for nb in line.split(':')[1].strip().split(' ') if nb != '']
            elif line.startswith('Distance:') :
                dists = [int(nb) for nb in line.split(':')[1].strip().split(' ') if nb != '']
        return [{"time" : time, "dist" : dists[i]} for i, time in enumerate(times)]

    def get_distance(self, charging_time, total_time):
        return charging_time * (total_time - charging_time)
    
    def get_charging_time(self, total_time, dist):
        t = symbols('t')
        equation = Eq(self.get_distance(t, total_time), dist)
        return solve(equation)
                    
    def run_part1(self):
        solutions = [self.get_charging_time(race['time'], race['dist']) for race in self.parsed_input]
        mult = 1
        for sol in solutions : 
            max_sol = ceil(max(sol)) - 1
            min_sol = floor(min(sol)) + 1
            mult *= max_sol - min_sol + 1
        return mult
    
    def run_part2(self):
        time = int(''.join(str(race['time']) for race in self.parsed_input))
        dist = int(''.join(str(race['dist']) for race in self.parsed_input))
        sol = self.get_charging_time(time, dist)
        max_sol = ceil(max(sol)) - 1
        min_sol = floor(min(sol)) + 1
        return max_sol - min_sol + 1

puzzle = Puzzle6()
puzzle.run()