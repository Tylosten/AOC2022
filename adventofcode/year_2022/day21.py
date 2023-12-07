import re
from common import Puzzle


class Monkey:
    def __init__(self, name, number=None, monkey1=None, monkey2=None, operation=None):
        self.name = name
        self.number = number
        self.monkey1 = monkey1
        self.monkey2 = monkey2
        self.operation = operation


class Puzzle21(Puzzle):
    def __init__(self):
        super().__init__(21)

    def parse_input(self):
        monkeys = {}
        for monkey in self.input:
            match = re.match(r"(\w+): (.+)", monkey)
            if match:
                name, nb_or_op = match.groups()
                if nb_or_op.isdigit():
                    monkeys[name] = Monkey(name, number=int(nb_or_op))
                else:
                    monkey1, op, monkey2 = re.match(
                        r"(\w+) ([\+-/*]) (\w+)", nb_or_op
                    ).groups()
                    monkeys[name] = Monkey(
                        name, monkey1=monkey1, monkey2=monkey2, operation=op
                    )
            else:
                raise ValueError(f"Can't parse {monkey}")
        return monkeys

    # pylint: disable=eval-used
    def get_monkey_nb(self, monkey_name, exclude_humn=False):
        monkey = self.parsed_input[monkey_name]
        if exclude_humn:
            if monkey.monkey1 == "humn":
                return (
                    monkey.operation,
                    True,
                    self.get_monkey_nb(monkey.monkey2, exclude_humn=exclude_humn),
                )
            if monkey.monkey2 == "humn":
                return (
                    monkey.operation,
                    False,
                    self.get_monkey_nb(monkey.monkey1, exclude_humn=exclude_humn),
                )

        if monkey.number is not None:
            return monkey.number

        monkey1_nb = self.get_monkey_nb(monkey.monkey1, exclude_humn=exclude_humn)
        monkey2_nb = self.get_monkey_nb(monkey.monkey2, exclude_humn=exclude_humn)
        return eval(f"{monkey1_nb} {monkey.operation} {monkey2_nb}")

    def run_part1(self):
        return self.get_monkey_nb("root")

    def run_part2(self):
        root = self.parsed_input["root"]
        max_search = 10000000000000
        min_search = 1000000000000

        self.parsed_input["humn"].number = 0
        res_0 = [
            self.get_monkey_nb(monkey_name)
            for monkey_name in [root.monkey1, root.monkey2]
        ]
        self.parsed_input["humn"].number = 1
        res_1 = [
            self.get_monkey_nb(monkey_name)
            for monkey_name in [root.monkey1, root.monkey2]
        ]
        humn_pos = 1 if res_0[0] == res_0[1] else 0
        going_up = res_1[humn_pos] - res_0[humn_pos] > 0

        old_dist = None
        while max_search - min_search > 1:
            i = (max_search + min_search) // 2
            print(f"Testing {i}")
            self.parsed_input["humn"].number = i
            test = [
                self.get_monkey_nb(monkey_name)
                for monkey_name in [root.monkey1, root.monkey2]
            ]
            if test[0] == test[1]:
                return i
            too_high = test[humn_pos] - test[1 - humn_pos] > 0

            if (too_high and going_up) or (not too_high and not going_up):
                max_search = i
            elif too_high and not going_up or (not too_high and going_up):
                min_search = i

            new_dist = test[humn_pos] - test[1 - humn_pos]
            if old_dist:
                print(
                    f'    dist to {test[1-humn_pos]} {"too high" if too_high else "too low"} {new_dist} : {old_dist - new_dist} diff'
                )
            old_dist = new_dist


puzzle = Puzzle21()
puzzle.run()
