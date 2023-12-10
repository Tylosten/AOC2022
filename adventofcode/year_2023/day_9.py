from adventofcode.year_2023.puzzle2023 import Puzzle2023

class Puzzle9(Puzzle2023):
    def __init__(self):
        super().__init__(9)
        
    def parse_input(self):
        return([[int(nb) for nb in line.split(' ')] for line in self.input])

    def get_diff_seq(self, seq):
        return [seq[i] - seq[i-1] for i in range(1, len(seq))]
    
    def get_prediction(self, seq, backward = True):
        seq_diff = self.get_diff_seq(seq)
        if all(nb == 0 for nb in seq_diff):
            return seq[0] if backward else seq[-1]
        if backward:
            return seq[0] - self.get_prediction(seq_diff, backward=backward)
        else :
            return seq[-1] + self.get_prediction(seq_diff, backward=backward)
    
    
    
    def run_part1(self):
        return sum(self.get_prediction(data, backward = False) for data in self.parsed_input)
    
    def run_part2(self):
        return sum(self.get_prediction(data, backward = True) for data in self.parsed_input)
    
puzzle = Puzzle9()
puzzle.run()