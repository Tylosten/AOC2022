from copy import deepcopy
from common import Puzzle
from day9 import Point

N = Point(-1, 0)
S = Point(1, 0)
W = Point(0, -1)
E = Point(0, 1)
NE = N + E
NW = N + W
SE = S + E
SW = S + W


class Puzzle23(Puzzle):
    def __init__(self):
        super().__init__(23)
        self.moves = [
            {"dir": N, "to_check": [N, NE, NW]},
            {"dir": S, "to_check": [S, SE, SW]},
            {"dir": W, "to_check": [W, NW, SW]},
            {"dir": E, "to_check": [E, NE, SE]},
        ]

    def parse_input(self):
        elfs = []
        for x, row in enumerate(self.input):
            for y, col in enumerate(row):
                if col == "#":
                    elfs.append(Point(x, y))
        return elfs

    def get_limits(self, elfs):
        xmin = min(x.x for x in elfs)
        xmax = max(x.x for x in elfs)
        ymin = min(x.y for x in elfs)
        ymax = max(x.y for x in elfs)
        return xmin, xmax, ymin, ymax

    def get_map(self, elfs):
        xmin, xmax, ymin, ymax = self.get_limits(elfs)
        emap = []
        for x in range(xmin, xmax + 3):
            vals = []
            for y in range(ymin, ymax + 3):
                vals.append(".")
            emap.append(vals)
        for elf in elfs:
            emap[elf.x - xmin + 1][elf.y - ymin + 1] = "#"
        return emap, xmin, xmax, ymin, ymax

    def get_in_map(self, emap, xmin, ymin, point):
        return emap[point.x - xmin + 1][point.y - ymin + 1]

    def proposed_moves(self, elfs):
        moves = []
        already_proposed = []
        emap, xmin, xmax, ymin, ymax = self.get_map(elfs)
        for i, elf in enumerate(elfs):
            # Check if elf has neighbor :
            if all(
                self.get_in_map(emap, xmin, ymin, elf + neighbor) == "."
                for neighbor in [N, S, W, E, NE, NW, SE, SW]
            ):
                continue

            # Propose a move
            for direction in self.moves:
                if any(
                    self.get_in_map(emap, xmin, ymin, elf + neighbor) == "#"
                    for neighbor in direction["to_check"]
                ):
                    continue
                proposed_move = elf + direction["dir"]
                if proposed_move in already_proposed:
                    moves = [x for x in moves if x[1] != proposed_move]
                else:
                    already_proposed.append(proposed_move)
                    moves.append((i, proposed_move))
                break
        first_dir = self.moves.pop(0)
        self.moves.append(first_dir)
        return moves

    def move(self, elfs):
        proposed_moves = self.proposed_moves(elfs)
        for move in proposed_moves:
            elfs[move[0]] = move[1]
        return elfs, len(proposed_moves) == 0

    def get_empty_tiles(self, elfs):
        xmin, xmax, ymin, ymax = self.get_limits(elfs)
        print(f"({xmin}, {ymin}) - ({xmax}, {ymax})")
        return (xmax - xmin + 1) * (ymax - ymin + 1) - len(elfs)

    def print(self, elfs):
        xmin, xmax, ymin, ymax = self.get_limits(elfs)
        for x in range(xmin, xmax + 1):
            print(x, end=" ")
            for y in range(ymin, ymax + 1):
                if Point(x, y) in elfs:
                    print("#", end="")
                else:
                    print(".", end="")
            print("")

    def run_part1(self):
        elfs = deepcopy(self.parsed_input)
        # self.print(elfs)
        for i in range(10):
            print(f"============================== {i} ==============================")
            elfs, ended = self.move(elfs)
            # self.print(elfs)
        return self.get_empty_tiles(elfs)

    def run_part2(self):
        elfs = deepcopy(self.parsed_input)
        ended = False
        i = 0
        while not ended:
            i += 1
            elfs, ended = self.move(elfs)
        return i


if __name__ == "__main__":
    Puzzle23().run(part1=False)
