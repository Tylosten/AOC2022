import math
from munch import munchify
from common import Puzzle


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Point):
            return self.x == __o.x and self.y == __o.y
        if isinstance(__o, list):
            return self.x == __o[0] and self.y == __o[1]
        return False

    def __add__(self, __o: object) -> object:
        if isinstance(__o, Point):
            return Point(self.x + __o.x, self.y + __o.y)
        if isinstance(__o, list):
            return Point(self.x + __o[0], self.y + __o[1])
        if isinstance(__o, int):
            return Point(self.x + __o, self.y + __o)
        return None

    def __sub__(self, __o: object) -> object:
        if isinstance(__o, Point):
            return Point(self.x - __o.x, self.y - __o.y)
        if isinstance(__o, list):
            return Point(self.x - __o[0], self.y - __o[1])
        if isinstance(__o, int):
            return Point(self.x - __o, self.y - __o)
        return None

    def __str__(self) -> str:
        return f"({self.x},{self.y})"

    def size(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def unit_move(self):
        return Point(
            0 if self.x == 0 else self.x / abs(self.x),
            0 if self.y == 0 else self.y / abs(self.y),
        )


class Puzzle9(Puzzle):
    def __init__(self):
        super().__init__(9)

    def get_dir_move(self, direction):
        if direction == "D":
            move = Point(0, -1)
        elif direction == "U":
            move = Point(0, 1)
        elif direction == "L":
            move = Point(-1, 0)
        elif direction == "R":
            move = Point(1, 0)
        return move

    def parse_input(self):
        res = [row.split(" ") for row in self.input]
        res = [{"move": self.get_dir_move(row[0]), "nb": int(row[1])} for row in res]

        return munchify(res)

    def move_head(self, head, move):
        return head + move

    def move_tail(self, head, tail):
        dist = head - tail
        if dist.size() >= 2:
            tail += dist.unit_move()
        return tail

    def run_part1(self):
        visited = [Point(0, 0)]
        head = Point(0, 0)
        tail = Point(0, 0)

        for move_seq in self.parsed_input:
            for i in range(move_seq.nb):
                head = self.move_head(head, move_seq.move)
                tail = self.move_tail(head, tail)
                if tail not in visited:
                    visited.append(tail)
                # print(head, tail, (head-tail).size(), len(visited))
                # import pdb; pdb.set_trace()

        return len(visited)

    def run_part2(self):
        visited = [Point(0, 0)]
        knots_nb = 10
        knots = []
        for i in range(knots_nb):
            knots.append(Point(0, 0))
        for move_seq in self.parsed_input:
            for i in range(move_seq.nb):
                knots[0] = self.move_head(knots[0], move_seq.move)
                for j in range(1, knots_nb):
                    knots[j] = self.move_tail(knots[j - 1], knots[j])
                if knots[knots_nb - 1] not in visited:
                    visited.append(knots[knots_nb - 1])
        return len(visited)


print(Puzzle9().run_part2())
