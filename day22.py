from copy import deepcopy
import re
from common import Puzzle

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)


class Puzzle22(Puzzle):
    def __init__(self):
        super().__init__(22)
        self.map = None
        self.path = []
        self.parse_input()

    def parse_input(self):
        self.map = [row.replace("\n", "") for row in self.input]
        directions = self.map.pop()

        self.path = []
        num_str = ""
        for char in directions:
            if char in ["L", "R"]:
                self.path += [int(num_str), char]
                num_str = ""
            else:
                num_str += char
        self.path += [int(num_str)]

    def get_first_position(self, line=0, reverse=False):
        iterator = (
            enumerate(self.map[line])
            if not reverse
            else reversed(list(enumerate(self.map[line])))
        )
        for x, col in iterator:
            if col == ".":
                return (x, line)
        raise ValueError("No start position found")

    def is_void(self, position):
        x, y = position
        if x < 0 or y < 0:
            return True
        try:
            return self.map[y][x] == " "
        except IndexError:
            return True

    def get_edge(self, position, direction):
        x, y = position
        dx, dy = direction
        while not self.is_void((x + dx, y + dy)):
            x += dx
            y += dy
        return (x, y)

    def run_part1(self):
        direction = RIGHT
        position = self.get_first_position()

        print(f"position : {position}")
        for step in self.path:
            if step == "L":
                direction = (direction[1], -direction[0])
            elif step == "R":
                direction = (-direction[1], direction[0])
            else:
                for i in range(step):
                    new_position = (
                        position[0] + direction[0],
                        position[1] + direction[1],
                    )

                    # check void
                    if self.is_void(new_position):
                        # print(f'Void found at {new_position}')
                        new_position = self.get_edge(
                            position, [dir * -1 for dir in direction]
                        )

                    # check wall
                    if self.map[new_position[1]][new_position[0]] == "#":
                        # print(f'Wall found at {new_position}')
                        break

                    # move
                    position = new_position
                    # print(f'position : {position}, direction : {direction}')

        print(f"position : {position}, direction : {direction}")
        return (
            1000 * (position[1] + 1)
            + 4 * (position[0] + 1)
            + [RIGHT, DOWN, LEFT, UP].index(direction)
        )


puzzle = Puzzle22()

puzzle.run()
