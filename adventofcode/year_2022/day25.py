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

    def int_to_snafu(self, nb):
        res = []
        to_process = nb
        while to_process > 0:
            res.append(to_process % 5)
            to_process = to_process // 5
        # pylint: disable=consider-using-enumerate
        for i in range(len(res)):
            if res[i] > 2:
                res[i] -= 5
                res[i] = "-" if res[i] == -1 else "=" if res[i] == -2 else str(res[i])
                if i == len(res) - 1:
                    res.append(1)
                else:
                    res[i + 1] += 1

        return "".join(str(r) for r in reversed(res))

    def run_part1(self):
        sum_int = sum(self.snafu_to_int(snafu) for snafu in self.input)
        return self.int_to_snafu(sum_int)


if __name__ == "__main__":
    Puzzle25().run()
