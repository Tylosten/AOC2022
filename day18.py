from common import Puzzle
from copy import deepcopy


class Puzzle18(Puzzle):
    def __init__(self):
        super().__init__(18)

    def parse_input(self):
        cubes = []
        for row in self.input:
            cubes.append([int(c) for c in row.split(",")])
        return cubes

    def run_part1(self):
        surface = 0
        for cube in self.parsed_input:
            for i in range(3):
                for j in [-1, 1]:
                    neighbor = deepcopy(cube)
                    neighbor[i] += j

                    if neighbor not in self.parsed_input:
                        surface += 1
        return surface

    def run_part2(self):
        left_bottom = [min(c[i] for c in self.parsed_input) - 1 for i in range(3)]
        right_top = [max(c[i] for c in self.parsed_input) + 1 for i in range(3)]
        print(f"left_bottom = {left_bottom}, right_top = {right_top}")

        todo = [left_bottom]
        done = []
        surface = 0

        while len(todo) > 0:
            air_cube = todo.pop()
            for i in range(3):
                for j in [-1, 1]:
                    neighbor = deepcopy(air_cube)
                    neighbor[i] += j
                    is_lava = neighbor in self.parsed_input
                    if is_lava:
                        surface += 1
                    elif (
                        neighbor not in done
                        and neighbor not in todo
                        and all(
                            neighbor[i] >= left_bottom[i]
                            and neighbor[i] <= right_top[i]
                            for i in range(3)
                        )
                    ):
                        todo.append(neighbor)
            done.append(air_cube)

        return surface


puzzle = Puzzle18()
puzzle.run(part1=False)
