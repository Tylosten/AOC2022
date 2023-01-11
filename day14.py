import os
import sys
import pandas as pd
from common import Puzzle


class Puzzle14(Puzzle):
    def __init__(self):
        super().__init__(14)
        self.init_x = 500

    def parse_input(self):
        rocks = []
        maxy = 0
        for row in self.input:
            coords = [
                [int(coord) for coord in pt.split(",")] for pt in row.split(" -> ")
            ]
            rocks.append(coords)
            ycoords = [c[1] for c in coords]
            maxy = max([*ycoords, maxy])

        map = pd.DataFrame(
            ".",
            index=range(maxy + 1),
            columns=range(self.init_x - 2 - maxy, self.init_x + maxy + 3),
        )
        for rock in rocks:
            for i in range(len(rock) - 1):
                sortx = sorted([rock[i][1], rock[i + 1][1]])
                sorty = sorted([rock[i][0], rock[i + 1][0]])
                map.loc[sortx[0] : sortx[1], sorty[0] : sorty[1]] = "#"
        return map

    def print_map(self, map):
        for row in range(map.shape[0]):
            str_row = ""
            for col in range(map.shape[1]):
                str_row += map.iloc[row, col]
            print(str_row)

    def drop_sand(self, map, x, y):
        new_col = pd.Series(["." for i in range(len(map.index) - 1)] + ["#"])
        column = map.loc[x + 1 :, y]
        ground = column.loc[lambda x: x != "."].index
        if len(ground) == 0:
            return "abyss"
        ground = min(ground)
        if y - 1 < min(map.columns):
            map.loc[:, y - 1] = new_col.copy()
            map.sort_index(axis=1, inplace=True)
        if map.loc[ground, y - 1] == ".":
            return self.drop_sand(map, ground, y - 1)

        if y + 1 > max(map.columns):
            map.loc[:, y + 1] = new_col.copy()
            map.sort_index(axis=1, inplace=True)
        if map.loc[ground, y + 1] == ".":
            return self.drop_sand(map, ground, y + 1)
        return ground - 1, y

    def drop_sand2(self, map, x, y):
        new_col = pd.Series(["." for i in range(len(map.index) - 1)] + ["#"])
        map.loc[x, y] = "o"
        if x + 1 > max(map.index):
            return
        for next_y in [y - 1, y, y + 1]:
            if map.loc[x + 1, next_y] == ".":
                self.drop_sand2(map, x + 1, next_y)

    def to_csv(self, map):
        map.to_csv("14map.csv", sep=" ")

    def run_part1(self):
        map = self.parsed_input
        count = 0
        map.loc[0, 500] = "+"
        while True:
            coords = self.drop_sand(map, 0, 500)
            if coords == "abyss":
                break
            map.loc[coords[0], coords[1]] = "o"
            count += 1
        self.to_csv(map)
        return count

    def run_part2(self):
        grid = self.parsed_input
        max_ind = max(grid.index)
        grid.loc[max_ind + 1] = "."
        grid.loc[max_ind + 2] = "#"
        try:
            self.drop_sand2(grid, 0, 500)
        except Exception:
            self.to_csv(grid)
            raise
        self.to_csv(grid)
        return grid.apply(lambda x: x == "o").sum().sum()


puzzle = Puzzle14()
print(puzzle.run_part2())
