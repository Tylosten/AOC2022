from common import Puzzle


class Packet:
    def __init__(self, data):
        self.data = data

    def check_order(self, elt1, elt2):
        if isinstance(elt1, int) and isinstance(elt2, int):
            if elt1 == elt2:
                return "tie"
            return elt1 < elt2

        if isinstance(elt1, int) and isinstance(elt2, list):
            return self.check_order([elt1], elt2)

        if isinstance(elt1, list) and isinstance(elt2, int):
            return self.check_order(elt1, [elt2])

        if isinstance(elt1, list) and isinstance(elt2, list):
            for i in range(min(len(elt1), len(elt2))):
                check = self.check_order(elt1[i], elt2[i])
                if check != "tie":
                    return check
            return self.check_order(len(elt1), len(elt2))

        raise ValueError("Invalid input types")

    def __eq__(self, other):
        if isinstance(other, Packet):
            return self.check_order(self.data, other.data) == "tie"
        return False

    def __lt__(self, other):
        if isinstance(other, Packet):
            return self.check_order(self.data, other.data) == True
        return False

    def __gt__(self, other):
        if isinstance(other, Packet):
            return self.check_order(self.data, other.data) == False
        return False

    def __repr__(self):
        return str(self.data)


class Puzzle13(Puzzle):
    def __init__(self):
        super().__init__(13)

    def parsed_input(self):
        pairs = []
        for i in range(0, len(self.input), 3):
            pairs.append(
                [
                    Packet(eval(self.input[i])),
                    Packet(eval(self.input[i + 1])),
                ]
            )
        return pairs

    def run_part1(self):
        s = 0
        for i, pair in enumerate(self.parsed_input()):
            if pair[0] < pair[1]:
                s += i + 1
        return s

    def run_part2(self):
        pairs = self.parsed_input()
        packets = [pair[0] for pair in pairs] + [pair[1] for pair in pairs]
        divider1 = Packet([[2]])
        divider2 = Packet([[6]])
        packets += [divider1, divider2]
        ordered = sorted(packets)
        index1 = ordered.index(divider1) + 1
        index2 = ordered.index(divider2) + 1
        return ordered, index1, index2, index1 * index2


puzzle = Puzzle13()
puzzle.run()
