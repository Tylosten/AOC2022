import re
import munch
from common import Puzzle


class Puzzle4(Puzzle):
    def __init__(self):
        super().__init__(5)

    def parse_input(self):
        cols = {}
        moves = []
        for row in self.input:
            if row.strip().startswith("["):
                for i in range(0, len(row), 4):
                    letter = row[i + 1 : i + 2]
                    col_i = int(i / 4) + 1
                    if letter != " ":
                        cols[col_i] = [] if col_i not in cols else cols[col_i]
                        cols[col_i].insert(0, letter)
            elif row.startswith("move"):
                qty, fromc, toc = re.search(
                    r"move (\d+) from (\d+) to (\d+)", row
                ).groups()
                moves.append(
                    {"qty": int(qty), "col_from": int(fromc), "col_to": int(toc)}
                )
        return munch.munchify({"cols": cols, "moves": moves})

    def make_move(self, move, cols):
        for i in range(move.qty):
            cols[move.col_to].append(cols[move.col_from].pop())
        return cols

    def make_move2(self, move, cols):
        cols[move.col_to].extend(cols[move.col_from][-move.qty :])
        cols[move.col_from] = cols[move.col_from][: -move.qty]
        return cols

    def run_part1(self):
        cols = self.parsed_input.cols
        for move in self.parsed_input.moves:
            cols = self.make_move(move, cols)
        return "".join([cols[i][-1] for i in sorted(cols.keys())])

    def run_part2(self):
        cols = self.parsed_input.cols
        for move in self.parsed_input.moves:
            cols = self.make_move2(move, cols)
        return "".join([cols[i][-1] for i in sorted(cols.keys())])


puzzle = Puzzle4()
puzzle.run()
