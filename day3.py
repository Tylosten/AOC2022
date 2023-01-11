from common import Puzzle


class Puzzle3(Puzzle):
    def __init__(self):
        super().__init__(3)

    def parse_input(self):
        return self.input

    def find_item(self, rucksack):
        l = int(len(rucksack) / 2)
        part1 = rucksack[:l]
        part2 = rucksack[l:]
        item = [i for i in part1 if i in part2]
        item = [*set(item)]
        if len(item) == 1:
            return item[0]
        raise ValueError(f"Invalid rucksack item found : {str(item)} {rucksack}")

    def get_priority(self, item):
        upper = item.isupper()
        item_ord = ord(item)
        return (item_ord - 64 + 26) if upper else (item_ord - 96)

    def run_part1(self):
        s = 0
        for r in self.input:
            if r != "":
                s += self.get_priority(self.find_item(r))
        return s

    def find_group_item(self, r1, r2, r3):
        for i in r1:
            if i in r2 and i in r3:
                return i
        raise ValueError(f"Couldn't find group item for {r1} and {r2} and {r3}")

    def run_part2(self):
        s = 0
        for group in range(0, len(self.input) - 3, 3):
            s += self.get_priority(
                self.find_group_item(
                    self.input[group], self.input[group + 1], self.input[group + 2]
                )
            )
        return s


puzzle = Puzzle3()
puzzle.run()
