import re
from munch import munchify
from common import Puzzle


class Puzzle16(Puzzle):
    def __init__(self):
        super().__init__(16)

    def parsed_input(self):
        valves = []
        for row in self.input:
            name, flow, neighbors = re.match(
                r"Valve (\w+) has flow rate=(\d+); tunnels lead to valves (.+)^", row
            ).groups()
            valves.append(
                {"name": name, "flow": int(flow), "neighbors": neighbors.split(", ")}
            )
        return munchify(valves)


puzzle = Puzzle16()
