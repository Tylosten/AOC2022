from munch import munchify
from common import Puzzle


class Puzzle10(Puzzle):
    def __init__(self):
        super().__init__(10)

    @property
    def parsed_input(self):
        cycle = 0
        x = 1
        res = []
        for row in self.input:
            if row.startswith("noop"):
                cycle += 1
                res.append({"cycle": cycle, "x": x})
            elif row.startswith("addx"):
                cycle += 1
                res.append({"cycle": cycle, "x": x})
                cycle += 1
                res.append({"cycle": cycle, "x": x})
                x += int(row.split(" ")[1])
        return munchify(res)

    def run_part1(self):
        sum = 0
        for index in range(19, len(self.parsed_input), 40):
            print(index, self.parsed_input[index])
            sum += self.parsed_input[index].x * self.parsed_input[index].cycle
        return sum

    def run_part2(self):
        row_str = "\n"
        for i, row in enumerate(self.parsed_input):
            if row.cycle % 40 in range(row.x, row.x + 3):
                row_str += "#"
            else:
                row_str += "."
            if i % 40 == 39:
                row_str += "\n"
        return row_str


puzzle = Puzzle10()
puzzle.run()
