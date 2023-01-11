import math
from common import Puzzle


class Monkey:
    def __init__(self, id, worries, count, operation, test, true, false):
        self.id = id
        self.count = count
        self.operation = operation
        self.test = test
        self.true = true
        self.false = false
        self.worries = worries

    def process(self, relief=None, modulo=False):
        item = self.worries.pop(0)
        ope = self.operation.replace("old", str(item))
        val = eval(ope)
        if relief is not None:
            if modulo:
                val = val % relief
            else:
                val = math.floor(val / relief)

        give_to = self.false if val % self.test else self.true
        self.count += 1
        return give_to, val


class Puzzle11(Puzzle):
    def __init__(self):
        super().__init__(11)

    def parsed_input(self):
        monkeys = []
        worries_str = "  Starting items: "
        operation_str = "  Operation: new = "
        test_str = "  Test: divisible by "
        true_str = "    If true: throw to monkey "
        false_str = "    If false: throw to monkey "
        for row in self.input:
            if row.startswith("Monkey"):
                monkey = {"id": int(row.split(" ")[1][:-2]), "count": 0}
            elif row.startswith(worries_str):
                monkey["worries"] = [
                    int(w) for w in row[len(worries_str) :].split(", ")
                ]
            elif row.startswith(operation_str):
                monkey["operation"] = row[len(operation_str) :]
            elif row.startswith(test_str):
                monkey["test"] = int(row[len(test_str) :])
            elif row.startswith(true_str):
                monkey["true"] = int(row[len(true_str) :])
            elif row.startswith(false_str):
                monkey["false"] = int(row[len(false_str) :])
            if row == "\n":
                monkeys.append(Monkey(**monkey))
        monkeys.append(Monkey(**monkey))
        return monkeys

    def run_part1(self, niter=20):
        monkeys = self.parsed_input()
        for i in range(niter):
            for monkey in monkeys:
                while len(monkey.worries) > 0:
                    give_to, val = monkey.process(relief=3)
                    monkeys[give_to].worries.append(val)

        counts = sorted([monkey.count for monkey in monkeys], reverse=True)
        return counts[0] * counts[1]

    def run_part2(self, niter=1000):
        monkeys = self.parsed_input()
        relief = math.prod([m.test for m in monkeys])
        for i in range(niter):
            for monkey in monkeys:
                while len(monkey.worries) > 0:
                    give_to, val = monkey.process(relief=relief, modulo=True)
                    monkeys[give_to].worries.append(val)

        counts = sorted([monkey.count for monkey in monkeys], reverse=True)
        return counts[0] * counts[1]

    def run(self, niter=100):
        print("Part 1: ", self.run_part1(20))
        print("Part 2: ", self.run_part2(10000))


puzzle = Puzzle11()
puzzle.run(10000)
