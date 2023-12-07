from copy import deepcopy
import math
from common import Puzzle
import re


class MaterialGroup:
    def __init__(self, ore=0, clay=0, obsidian=0, geode=0):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode

    def __repr__(self):
        return f"({self.ore} ore, {self.clay} clay, {self.obsidian} obsidian, {self.geode} geode)"

    def __add__(self, other):
        return MaterialGroup(
            self.ore + other.ore,
            self.clay + other.clay,
            self.obsidian + other.obsidian,
            self.geode + other.geode,
        )

    def __sub__(self, other):
        return MaterialGroup(
            self.ore - other.ore,
            self.clay - other.clay,
            self.obsidian - other.obsidian,
            self.geode - other.geode,
        )

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return MaterialGroup(
                self.ore * other,
                self.clay * other,
                self.obsidian * other,
                self.geode * other,
            )
        if isinstance(other, MaterialGroup):
            return MaterialGroup(
                self.ore * other.ore,
                self.clay * other.clay,
                self.obsidian * other.obsidian,
                self.geode * other.geode,
            )
        raise TypeError(
            f"unsupported operand type(s) for *: '{type(self)}' and '{type(other)}'"
        )

    def __ge__(self, other):
        return (
            self.ore >= other.ore
            and self.clay >= other.clay
            and self.obsidian >= other.obsidian
            and self.geode >= other.geode
        )

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, MaterialGroup):
            return (
                self.ore == __o.ore
                and self.clay == __o.clay
                and self.obsidian == __o.obsidian
                and self.geode == __o.geode
            )
        return False

    def set(self, rtype, value):
        if rtype == "geode":
            self.geode = value
        elif rtype == "obsidian":
            self.obsidian = value
        elif rtype == "clay":
            self.clay = value
        elif rtype == "ore":
            self.ore = value
        else:
            raise ValueError(f"Unknown type {rtype}")

    def get(self, rtype):
        if rtype == "geode":
            return self.geode
        if rtype == "obsidian":
            return self.obsidian
        if rtype == "clay":
            return self.clay
        if rtype == "ore":
            return self.ore
        raise ValueError(f"Unknown type {rtype}")

    def sum(self):
        return self.ore + self.clay + self.obsidian + self.geode


class Blueprint:
    def __init__(
        self,
        blueprint_id,
        orerobot_ore,
        clayrobot_ore,
        obsrobot_ore,
        obsrobot_clay,
        geodrobot_ore,
        geodrobot_obs,
    ):
        self.id = blueprint_id
        self.ore_robot_cost = MaterialGroup(ore=orerobot_ore)
        self.clay_robot_cost = MaterialGroup(ore=clayrobot_ore)
        self.obs_robot_cost = MaterialGroup(ore=obsrobot_ore, clay=obsrobot_clay)
        self.geod_robot_cost = MaterialGroup(ore=geodrobot_ore, obsidian=geodrobot_obs)
        self.maximums = MaterialGroup(
            ore=self.get_max_robots("ore"),
            clay=self.get_max_robots("clay"),
            obsidian=self.get_max_robots("obsidian"),
            geode=0,
        )

    def __repr__(self):
        return f"Blueprint {self.id}: {self.ore_robot_cost.ore} ore, {self.clay_robot_cost.ore} ore, {self.obs_robot_cost.ore} ore + {self.obs_robot_cost.clay} clay, {self.geod_robot_cost.ore} ore + {self.geod_robot_cost.obsidian} obsidian"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Blueprint):
            return (
                self.id == __o.id
                and self.ore_robot_cost == __o.ore_robot_cost
                and self.clay_robot_cost == __o.clay_robot_cost
                and self.obs_robot_cost == __o.obs_robot_cost
                and self.geod_robot_cost == __o.geod_robot_cost
            )
        return False

    def get_cost(self, rtype):
        if rtype == "geode":
            return self.geod_robot_cost
        if rtype == "obsidian":
            return self.obs_robot_cost
        if rtype == "clay":
            return self.clay_robot_cost
        if rtype == "ore":
            return self.ore_robot_cost
        raise ValueError(f"Unknown robot type {rtype}")

    def get_max_robots(self, rtype):
        return max(
            self.geod_robot_cost.get(rtype),
            self.obs_robot_cost.get(rtype),
            self.clay_robot_cost.get(rtype),
            self.ore_robot_cost.get(rtype),
        )

    def get_max_geodes(self, time_left=24, verbose=False):
        todo = [RobotFactory(self, time_left=time_left)]
        max_geode = 0
        while len(todo) > 0:
            next_todo = []
            for factory in todo:
                possible_next = factory.all_possible_next()
                if len(possible_next) == 0:
                    tmp_max = (
                        factory.stock.geode + factory.robots.geode * factory.time_left
                    )
                    if tmp_max > max_geode:
                        max_geode = tmp_max
                        if verbose:
                            print(f"New max geode: {max_geode} {factory}")
                    continue
                for next_factory in possible_next:
                    if next_factory not in next_todo and next_factory.time_left >= 0:
                        next_todo.append(next_factory)
            next_todo = [
                factory
                for factory in next_todo
                if not any(
                    other.best_than(factory) for other in next_todo if other != factory
                )
            ]
            todo = next_todo
            if verbose:
                print(f"Todo: {len(todo)}")

        print(f"Max geodes for blueprint {self.id} : {max_geode}")
        return max_geode


class RobotFactory:
    def __init__(self, blueprint: Blueprint, time_left=24) -> None:
        self.blueprint = blueprint
        self.robots = MaterialGroup(ore=1)
        self.stock = MaterialGroup()
        self.time_left = time_left

    def __repr__(self) -> str:
        return f"RobotFactory(blueprint {self.blueprint.id}, time left {self.time_left}, robots {self.robots}, stock {self.stock})"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, RobotFactory):
            return (
                self.blueprint == __o.blueprint
                and self.robots == __o.robots
                and self.stock == __o.stock
            )
        return False

    def max_robots_nb(self, rtype):
        if rtype == "geode":
            return False
        return (
            self.robots.get(rtype) * self.time_left + self.stock.get(rtype)
            >= self.blueprint.maximums.get(rtype) * self.time_left
        )

    def can_build(self, rtype):
        return self.stock >= self.blueprint.get_cost(rtype)

    def can_build_in_future(self, rtype):
        if self.max_robots_nb(rtype):
            return False
        cost = self.blueprint.get_cost(rtype)
        required_time = 1
        for cost_type in ["ore", "clay", "obsidian"]:
            if cost.get(cost_type) == 0:
                continue
            if self.robots.get(cost_type) == 0:
                return False
            required_time_for_type = math.ceil(
                (cost.get(cost_type) - self.stock.get(cost_type))
                / self.robots.get(cost_type)
            )
            required_time = max(required_time, required_time_for_type + 1)
        if required_time >= self.time_left:
            return False
        return required_time

    def build_robot(self, rtype):
        if self.can_build(rtype):
            self.stock = self.stock - self.blueprint.get_cost(rtype)
            self.robots.set(rtype, self.robots.get(rtype) + 1)
        else:
            raise ValueError(
                f"Can't build {rtype} robot, not enough resources  : cost {self.blueprint.get_cost(rtype)}, stock {self.stock}"
            )

    def all_possible_next(self):
        harvest = deepcopy(self.robots)
        possible_next = []
        # buiding a robot
        for rtype in ["geode", "obsidian", "clay", "ore"]:
            can_buid_time = self.can_build_in_future(rtype)
            if can_buid_time is not False:
                next_factory = deepcopy(self)
                next_factory.stock = next_factory.stock + harvest * can_buid_time
                next_factory.time_left -= can_buid_time
                next_factory.build_robot(rtype)
                possible_next.append(next_factory)
        return possible_next

    def best_than(self, other):
        if self.time_left < other.time_left:
            return False
        if self.robots.geode > other.robots.geode:
            return True
        return self.stock >= other.stock and self.robots >= other.robots


class Puzzle19(Puzzle):
    def __init__(self):
        super().__init__(19)

    def parse_input(self):
        blueprints = []
        for row in self.input:
            match = re.match(
                r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.",
                row,
            )
            if match:
                args = [int(x) for x in match.groups()]
                blueprints.append(Blueprint(*args))
            else:
                raise Exception(f"Could not parse row {row}")
        return blueprints

    def run_part1(self):
        res = 0
        for blueprint in self.parsed_input:
            res += blueprint.get_max_geodes(time_left=24, verbose=False) * blueprint.id
        return res

    def run_part2(self):
        res = 1
        for blueprint in self.parsed_input[:3]:
            res *= blueprint.get_max_geodes(time_left=32, verbose=False)
        return res


puzzle = Puzzle19()
puzzle.run(part2=False)
