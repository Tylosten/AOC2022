import re
import pandas as pd
from matplotlib import pyplot as plt
from common import Puzzle


class Puzzle12(Puzzle):
    def __init__(self):
        super().__init__(12)
        self.start = None
        self.end = None
        self.starts = []

    def parsed_input(self):
        res = []
        for i, row in enumerate(self.input):
            startindex = row.find("S")
            endindex = row.find("E")
            self.starts += [[i, _.start()] for _ in re.finditer("a", row)]
            if startindex >= 0:
                self.start = [i, startindex]
            if endindex >= 0:
                self.end = [i, endindex]
            res.append([ord(char) - 97 for char in row if char.isalpha()])
        res = pd.DataFrame(res)
        res.iloc[self.start[0], self.start[1]] = -1
        res.iloc[self.end[0], self.end[1]] = 26
        return res

    def run_part1(self):
        elevations = self.parsed_input()
        print(f"Going from {self.start} to {self.end}")
        dist = pd.DataFrame(
            -1, columns=range(elevations.shape[1]), index=range(elevations.shape[0])
        )
        dist.iloc[self.start[0], self.start[1]] = 0
        todo = [self.start]
        while len(todo) > 0:
            cell = todo.pop(0)
            curr_el = elevations.iloc[cell[0], cell[1]]
            curr_dist = dist.iloc[cell[0], cell[1]]
            neighbors = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            neighbors = [
                [cell[0] + n[0], cell[1] + n[1]]
                for n in neighbors
                if cell[0] + n[0] >= 0
                and cell[0] + n[0] < elevations.shape[0]
                and cell[1] + n[1] >= 0
                and cell[1] + n[1] < elevations.shape[1]
            ]
            for n in neighbors:
                n_el = elevations.iloc[n[0], n[1]]
                n_dist = dist.iloc[n[0], n[1]]
                if curr_el >= n_el - 1 and (n_dist > curr_dist + 1 or n_dist == -1):
                    if n == self.end:
                        return curr_dist + 1
                    dist.iloc[n[0], n[1]] = curr_dist + 1
                    todo.append(n)
        elevations.to_csv("12elevations.csv")

        return dist

    def run_part2(self):
        elevations = self.parsed_input()
        print(elevations.shape)
        dist = pd.DataFrame(
            -1, columns=range(elevations.shape[1]), index=range(elevations.shape[0])
        )
        for s in self.starts:
            dist.iloc[s[0], s[1]] = 0
        todo = self.starts.copy()

        # plt.pcolor(dist)
        # plt.show()
        while len(todo) > 0:
            cell = todo.pop(0)
            curr_el = elevations.iloc[cell[0], cell[1]]
            curr_dist = dist.iloc[cell[0], cell[1]]
            neighbors = [[0, 1], [0, -1], [1, 0], [-1, 0]]
            neighbors = [
                [cell[0] + n[0], cell[1] + n[1]]
                for n in neighbors
                if cell[0] + n[0] >= 0
                and cell[0] + n[0] < elevations.shape[0]
                and cell[1] + n[1] >= 0
                and cell[1] + n[1] < elevations.shape[1]
            ]
            for n in neighbors:
                n_el = elevations.iloc[n[0], n[1]]
                n_dist = dist.iloc[n[0], n[1]]
                if curr_el >= n_el - 1 and (n_dist > curr_dist + 1 or n_dist == -1):
                    dist.iloc[n[0], n[1]] = curr_dist + 1
                    if n == self.end:
                        print(f"Found end dist = {curr_dist + 1}")
                    todo.append(n)

        # plt.pcolor(dist)
        # plt.show()

        return dist.iloc[self.end[0], self.end[1]]


puzzle = Puzzle12()
puzzle.run()
