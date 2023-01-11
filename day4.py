from common import Puzzle


def is_between(a, b, c):
    return b <= a and a <= c


class Puzzle4(Puzzle):
    def __init__(self):
        super().__init__(4)

    @property
    def parsed_input(self):
        res = []
        for row in self.input:
            pair = row.split(",")
            elf1 = [int(i) for i in pair[0].split("-")]
            elf2 = [int(i) for i in pair[1].split("-")]

            res.append({"elf1": elf1, "elf2": elf2})
        return res

    def run_part1(self):
        count = 0
        for pair in self.parsed_input:
            if (
                pair["elf1"][0] <= pair["elf2"][0]
                and pair["elf1"][1] >= pair["elf2"][1]
            ):
                count += 1
            elif (
                pair["elf1"][0] >= pair["elf2"][0]
                and pair["elf1"][1] <= pair["elf2"][1]
            ):
                count += 1
        return count

    def run_part2(self):
        count = 0
        for pair in self.parsed_input:
            if (
                is_between(pair["elf1"][0], pair["elf2"][0], pair["elf2"][1])
                or is_between(pair["elf1"][1], pair["elf2"][0], pair["elf2"][1])
                or is_between(pair["elf2"][0], pair["elf1"][0], pair["elf1"][1])
                or is_between(pair["elf2"][1], pair["elf1"][0], pair["elf1"][1])
            ):
                count += 1

        return count


puzzle = Puzzle4()
puzzle.run()
