import re
import itertools
from common import Puzzle


class Valve:
    def __init__(self, name, flow, neighbors) -> None:
        self.name = name
        self.flow = flow
        self.neighbors = neighbors
        self.distances = {}

    def update_distances(self, valves, neigh_name, neigh_dist):
        for val_name, val_dist in valves[neigh_name].neighbors.items():
            new_dist = val_dist + neigh_dist
            if val_name in self.distances and self.distances[val_name] < new_dist:
                continue
            self.distances[val_name] = new_dist
            self.update_distances(valves, val_name, new_dist)

    def compute_distances(self, valves):
        for val_name, val_dist in self.neighbors.items():
            self.distances[val_name] = val_dist
            self.update_distances(valves, val_name, val_dist)

    def __repr__(self) -> str:
        return f"Valve {self.name} with flow {self.flow}"


class Path:
    def __init__(self, visited=None, pressure=0, time=0, max_time=30):
        self.path = visited if visited else ["AA"]
        self.time = time
        self.pressure = pressure
        self.max_time = max_time
        self.best_child_pressure = None

    def get_valve_pressure_release(self, valve_name, valves, time):
        return valves[valve_name].flow * (self.max_time - time)

    def next_possible_valves(self, valves, visited_valves=None):
        visited_valves = visited_valves if visited_valves else self.path
        last_valve_name = self.path[-1]
        last_valve = valves[last_valve_name]
        next_valves = []
        for next_valve_name, dist in last_valve.neighbors.items():
            next_time = self.time + dist + 1
            if next_time > self.max_time or next_valve_name in visited_valves:
                continue
            next_valves.append(next_valve_name)
        return next_valves

    def next_paths(self, valves, visited_valves=None):
        visited_valves = visited_valves if visited_valves else self.path
        next_paths = []
        last_valve_name = self.path[-1]
        last_valve = valves[last_valve_name]
        for next_valve_name in self.next_possible_valves(valves, visited_valves):
            dist = last_valve.neighbors[next_valve_name]
            add_pressure = self.get_valve_pressure_release(
                next_valve_name, valves, self.time + dist + 1
            )
            next_paths.append(
                Path(
                    visited=[*self.path, next_valve_name],
                    pressure=self.pressure + add_pressure,
                    time=self.time + dist + 1,
                    max_time=self.max_time,
                ),
            )
        return next_paths

    def get_all_paths(self, valves, using_max_time=True):
        childs_path = []
        next_paths = self.next_paths(valves)
        if len(next_paths) == 0 or not using_max_time:
            childs_path.append(self)
        for next_p in next_paths:
            childs_path.extend(next_p.get_all_paths(valves, using_max_time))
        return childs_path

    def __repr__(self) -> str:
        return f"Path {self.path} with pressure {self.pressure} and time {self.time}"


class Puzzle16(Puzzle):
    def __init__(self):
        super().__init__(16)

    def parse_input(self):
        valves = {}
        for row in self.input:
            match = re.match(
                r"Valve (\w+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (.*)",
                row,
            )
            if match is None:
                raise ValueError(f"Could not parse {row}")
            name, flow, neighbors = match.groups()
            valves[name] = Valve(
                name, int(flow), {neigh: 1 for neigh in neighbors.split(", ")}
            )
        self.simplify_network(valves)
        for valve in valves.values():
            valve.compute_distances(valves)
        return valves

    def simplify_network(self, valves):
        valves_to_process = list(valves.keys())
        while len(valves_to_process) > 0:
            valve_name = valves_to_process.pop()
            valve = valves[valve_name]
            is_hub = valve_name != "AA" and valve.flow == 0

            if is_hub:
                valves.pop(valve_name)
                neighbors_to_process = list(valve.neighbors.keys())
                while len(neighbors_to_process) > 0:
                    neighbor_name = neighbors_to_process.pop()
                    neighbor = valves[neighbor_name]
                    neighbor.neighbors.pop(valve_name)

                    for other_name in neighbors_to_process:
                        other = valves[other_name]
                        if (
                            other != neighbor
                            and not other_name in neighbor.neighbors.keys()
                        ):
                            dist = (
                                valve.neighbors[other_name]
                                + valve.neighbors[neighbor_name]
                            )
                            neighbor.neighbors[other_name] = dist
                            other.neighbors[neighbor_name] = dist

    def run_part1(self):
        valves = self.parsed_input
        beginning = Path(visited=["AA"], pressure=0, time=0, max_time=30)
        possible_paths = beginning.get_all_paths(valves=valves)
        return max([path.pressure for path in possible_paths])

    def run_part2(self):
        valves = self.parsed_input
        beginning = Path(visited=["AA"], pressure=0, time=0, max_time=26)
        possible_paths = beginning.get_all_paths(valves=valves, using_max_time=False)
        print(f"Found {len(possible_paths)} possible paths")

        possible_pair_pressures = []
        for path in possible_paths:
            for other in possible_paths:
                if path != other:
                    if (
                        len(
                            [
                                valve
                                for valve in [*path.path[1:], *other.path[1:]]
                                if valve in path.path and valve in other.path
                            ]
                        )
                        == 0
                    ):
                        possible_pair_pressures += [
                            {
                                "p1": path,
                                "p2": other,
                                "pressure": path.pressure + other.pressure,
                            }
                        ]
        print(f"Found {len(possible_pair_pressures)} possible pairs")
        return max([pair["pressure"] for pair in possible_pair_pressures])


puzzle = Puzzle16()
puzzle.run()
