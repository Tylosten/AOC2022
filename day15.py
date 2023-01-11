import re
import pandas as pd
from munch import munchify
from common import Puzzle
from time import time

LIM = 4000000
MINLIM = 0


class Puzzle15(Puzzle):
    def __init__(self):
        super().__init__(15)

    def parsed_input(self):
        sensors = []
        for row in self.input:
            sx, sy, bx, by = re.match(
                r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
                row,
            ).groups()
            sens = {"x": int(sx), "y": int(sy), "bx": int(bx), "by": int(by)}
            sens["dist"] = abs(sens["bx"] - sens["x"]) + abs(sens["by"] - sens["y"])
            sensors.append(sens)
        return munchify(sensors)

    def row_limits(self, sensors, y, verbose=False):
        limits = []
        for s in sensors:
            yd = abs(s.y - y)
            if yd <= s.dist:
                xd = s.dist - yd
                lim = [s.x - xd, s.x + xd]
                limits.append(lim)
        return self.simplify_lim(limits, verbose=verbose)

    def simplify_lim(self, lim, verbose=False):
        lim = sorted(lim, key=lambda x: x[0])
        simplify_lim = []
        next_lim = lim[0]
        if verbose:
            print(f"============ simplifying {lim} =============")
        for i in range(1, len(lim)):
            if verbose:
                print(f"i {i}, lim {lim[i]}, next_lim {next_lim}")
            if next_lim[1] < lim[i][0] - 1:
                simplify_lim.append(next_lim)
                if verbose:
                    print(f"{simplify_lim}")
                next_lim = lim[i]
            else:
                next_lim = [next_lim[0], max(lim[i][1], next_lim[1])]
                if verbose:
                    print(f"next_lim {next_lim}")
            if i == len(lim) - 1:
                simplify_lim.append(next_lim)

        if verbose:
            print(f"===> {simplify_lim}")
        return simplify_lim

    def print_grid(self, sensors, lims):
        grid = pd.DataFrame(
            ".", index=range(MINLIM, LIM + 1), columns=range(MINLIM, LIM + 1)
        )
        for l, lim in lims.items():
            if lim == "full":
                grid.loc[l, :] = "#"
            else:
                for pair in lim:
                    grid.loc[l, pair[0] : pair[1]] = "#"
        for s in sensors:
            grid.loc[s.y, s.x] = "S"
            grid.loc[s.by, s.bx] = "B"

        print(grid)

    def run_part1(self):
        limits = self.row_limits(self.parsed_input(), 10, True)
        return sum([lim[1] - lim[0] for lim in limits])

    def run_part2(self):
        sensors = self.parsed_input()
        for l in range(MINLIM, LIM + 1):
            lims = self.row_limits(sensors, l)
            if len(lims) == 2:
                return (lims[0][1] + 1) * LIM + l


time1 = time()
puzzle = Puzzle15()
puzzle.run(part2=False)
time2 = time()
print(f"Time: {time2 - time1}")
# part1 5394423
# part2 11840879211051
