from common import Puzzle

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)


class Blizzard:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def __repr__(self) -> str:
        return f"Blizzard({self.x}, {self.y}, {self.direction})"


class Puzzle24(Puzzle):
    def __init__(self):
        super().__init__(24)

    def parse_input(self):
        blizzards = []
        maxx = len(self.input[0]) - 1
        maxy = len(self.input) - 1
        start = (self.input[0].index("."), 0)
        end = (self.input[-1].index("."), len(self.input) - 1)

        for y, line in enumerate(self.input):
            for x, char in enumerate(line):
                if char == "^":
                    blizzards.append(Blizzard(x, y, UP))
                elif char == "v":
                    blizzards.append(Blizzard(x, y, DOWN))
                elif char == "<":
                    blizzards.append(Blizzard(x, y, LEFT))
                elif char == ">":
                    blizzards.append(Blizzard(x, y, RIGHT))
        return blizzards, start, end, maxx, maxy

    def move_blizzard(self, blizzard, maxx, maxy):
        blizzard.x += blizzard.direction[0]
        blizzard.y += blizzard.direction[1]

        if blizzard.x <= 0:
            blizzard.x = maxx - 1
        elif blizzard.x >= maxx:
            blizzard.x = 1

        if blizzard.y <= 0:
            blizzard.y = maxy - 1
        elif blizzard.y >= maxy:
            blizzard.y = 1

    def moves_to_check(self, position, start, end, maxx, maxy):
        possibles = [
            (position[0] + move[0], position[1] + move[1])
            for move in [(0, 0), UP, DOWN, LEFT, RIGHT]
        ]
        if end in possibles:
            return "END"
        return [
            possible
            for possible in possibles
            if possible == start
            or (
                possible[0] > 0
                and possible[0] < maxx
                and possible[1] > 0
                and possible[1] < maxy
            )
        ]

    def print_state(self, positions, blizzards, start, end, maxx, maxy):
        blizz_pos = list(set((blizzard.x, blizzard.y) for blizzard in blizzards))
        for y in range(maxy + 1):
            for x in range(maxx + 1):
                if (x, y) == start:
                    print("S", end="")
                elif (x, y) == end:
                    print("E", end="")
                elif (x, y) in blizz_pos:
                    print("B", end="")
                elif (x, y) in positions:
                    print("X", end="")
                else:
                    print(".", end="")
            print()

    def crossing_time(self, blizzards, start, end, maxx, maxy):
        positions = [start]
        round_nb = 0
        while True:
            round_nb += 1
            positions_to_check = []
            for pos in positions:
                possibles = self.moves_to_check(pos, start, end, maxx, maxy)
                if possibles == "END":
                    return round_nb, blizzards
                positions_to_check.extend(possibles)
            positions = list(set(positions_to_check))

            for blizzard in blizzards:
                self.move_blizzard(blizzard, maxx, maxy)
                if (blizzard.x, blizzard.y) in positions:
                    positions.remove((blizzard.x, blizzard.y))

            if round_nb % 100 == 0:
                print(f"Round {round_nb} - {len(positions)} positions to check")

    def run_part1(self):
        blizzards, start, end, maxx, maxy = self.parsed_input
        return self.crossing_time(blizzards, start, end, maxx, maxy)[0]

    def run_part2(self):
        blizzards, start, end, maxx, maxy = self.parsed_input
        crossing1, blizzards = self.crossing_time(blizzards, start, end, maxx, maxy)
        print(f"Crossing 1: {crossing1}")
        for blizzard in blizzards:
            self.move_blizzard(blizzard, maxx, maxy)
        crossing2, blizzards = self.crossing_time(
            blizzards, start=end, end=start, maxx=maxx, maxy=maxy
        )
        for blizzard in blizzards:
            self.move_blizzard(blizzard, maxx, maxy)
        print(f"Crossing 2: {crossing2}")
        return (
            crossing1
            + crossing2
            + self.crossing_time(blizzards, start, end, maxx, maxy)[0]
        )


if __name__ == "__main__":
    Puzzle24().run(part1=False)
