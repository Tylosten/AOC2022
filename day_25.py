from common import Puzzle


class Puzzle25(Puzzle):
    def __init__(self):
        super().__init__(25)

    def snafu_to_int(self, snafu):
        res = 0
        for i, char in enumerate(reversed(snafu)):
            val = -1 if char == "-" else -2 if char == "=" else int(char)
            res += val * (5**i)
        return res

    # def int_to_snafu(self, nb):

    def run_part1(self):
        sum = sum(self.snafu_to_int(snafu) for snafu in self.input)
        return sum


if __name__ == "__main__":
    Puzzle25().run()
