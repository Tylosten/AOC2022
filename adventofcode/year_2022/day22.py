from copy import deepcopy
import re
from common import Puzzle

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)
DIRECTIONS = {"up": UP, "down": DOWN, "left": LEFT, "right": RIGHT}

NEIGHBOR_ORDER = ["up", "right", "down", "left"]
NEIGHBOR_FACES = {
    "front": {"up": "top", "down": "bottom", "left": "left", "right": "right"},
    "back": {"up": "top", "down": "bottom", "left": "right", "right": "left"},
    "left": {"up": "top", "down": "bottom", "left": "back", "right": "front"},
    "right": {"up": "top", "down": "bottom", "left": "front", "right": "back"},
    "top": {"up": "back", "down": "front", "left": "left", "right": "right"},
    "bottom": {"up": "front", "down": "back", "left": "left", "right": "right"},
}
OPPOSITE = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}


class Face:
    def __init__(self, values, coord, face_type):
        self.values = values
        self.coord = coord
        self.type = face_type
        self.neighbor_types = NEIGHBOR_FACES[face_type]

    def rotate(self, face_type, direction):
        print(f"{self.type} : Rotating {face_type} {direction}")
        curr_direction = [k for k, v in self.neighbor_types.items() if v == face_type][
            0
        ]
        curr_index = NEIGHBOR_ORDER.index(curr_direction)
        next_index = NEIGHBOR_ORDER.index(direction)
        transl_index = next_index - curr_index
        print(f"    From {self.neighbor_types}")
        self.neighbor_types = {
            NEIGHBOR_ORDER[(NEIGHBOR_ORDER.index(k) + transl_index + 4) % 4]: v
            for k, v in self.neighbor_types.items()
        }
        print(f"    To {self.neighbor_types}")


class Cube:
    def __init__(
        self, front=None, back=None, left=None, right=None, top=None, bottom=None
    ):
        self.faces = {
            "front": front,
            "back": back,
            "left": left,
            "right": right,
            "top": top,
            "bottom": bottom,
        }

    def is_done(self):
        return (
            self.faces["front"]
            and self.faces["back"]
            and self.faces["left"]
            and self.faces["right"]
            and self.faces["top"]
            and self.faces["bottom"]
        )


class Map:
    def __init__(self, values):
        self.values = values
        self.cube_size = self.get_cube_size()

    def get_first_position(self, line=0, reverse=False):
        iterator = (
            enumerate(self.values[line])
            if not reverse
            else reversed(list(enumerate(self.values[line])))
        )
        for x, col in iterator:
            if col == ".":
                return (x, line)
        raise ValueError("No start position found")

    def is_void(self, position):
        x, y = position
        if x < 0 or y < 0:
            return True
        try:
            return self.values[y][x] == " "
        except IndexError:
            return True

    def get_edge(self, position, direction):
        x, y = position
        dx, dy = direction
        while not self.is_void((x + dx, y + dy)):
            x += dx
            y += dy
        return (x, y)

    def get_cube_size(self):
        print(self.values[-1])
        max_row = max(len(row) for row in self.values)
        max_col = len(self.values)
        size = int(max(max_row, max_col) / 4)
        print(f"Max row : {max_row}, Max col : {max_col}")
        return size

    def get_cube(self):
        cube = Cube()

        for x, val in enumerate(self.values[0]):
            if val != " ":
                break
        cube.faces["front"] = self.get_face((x, 0), "front")
        done = ["front"]
        todo = ["front"]

        while not cube.is_done():
            curr_face_type = todo.pop()
            print(f"Processing face {curr_face_type}")
            curr_face = cube.faces[curr_face_type]
            neighs = self.get_neighbors(curr_face, done)
            neighs = {curr_face.neighbor_types[k]: v for k, v in neighs.items()}
            print(f"  Neighs : {neighs}")

            for n_type, n_face in neighs.items():
                print(f"  Adding {n_type} face")
                cube.faces[n_type] = n_face
                todo.append(n_type)
                done.append(n_type)

        return cube

    def get_face(self, coord, face_type):
        if not self.is_void(coord):
            # print(f'Face([line[{coord[0]}:{coord[0]+self.cube_size}] for line in self.values[{coord[1]}:{coord[1]+self.cube_size}]], {coord}, {self.cube_size})')
            return Face(
                values=[
                    line[coord[0] : coord[0] + self.cube_size]
                    for line in self.values[coord[1] : coord[1] + self.cube_size]
                ],
                coord=coord,
                face_type=face_type,
            )
        return None

    def get_neighbors(self, face, done):
        x, y = face.coord
        neigh_coords = {
            "up": (x, y - self.cube_size),
            "down": (x, y + self.cube_size),
            "left": (x - self.cube_size, y),
            "right": (x + self.cube_size, y),
        }
        neighs = {}
        for direction, neigh_coord in neigh_coords.items():
            neigh_type = face.neighbor_types[direction]
            if neigh_type in done:
                continue
            neigh_face = self.get_face(neigh_coord, neigh_type)
            if neigh_face:
                neigh_face.rotate(face.type, OPPOSITE[direction])
                neighs[direction] = neigh_face
        return neighs


class Puzzle22(Puzzle):
    def __init__(self):
        super().__init__(22)
        self.map = None
        self.path = []
        self.parse_input()

    def parse_input(self):
        values = [row.replace("\n", "") for row in self.input]
        directions = values.pop()
        values.pop()
        self.map = Map(values=values)
        self.path = []
        num_str = ""
        for char in directions:
            if char in ["L", "R"]:
                self.path += [int(num_str), char]
                num_str = ""
            else:
                num_str += char
        self.path += [int(num_str)]

    def run_part1(self):
        direction = RIGHT
        position = self.get_first_position()

        print(f"position : {position}")
        for step in self.path:
            if step == "L":
                direction = (direction[1], -direction[0])
            elif step == "R":
                direction = (-direction[1], direction[0])
            else:
                for i in range(step):
                    new_position = (
                        position[0] + direction[0],
                        position[1] + direction[1],
                    )

                    # check void
                    if self.is_void(new_position):
                        # print(f'Void found at {new_position}')
                        new_position = self.get_edge(
                            position, [dir * -1 for dir in direction]
                        )

                    # check wall
                    if self.map.values[new_position[1]][new_position[0]] == "#":
                        # print(f'Wall found at {new_position}')
                        break

                    # move
                    position = new_position
                    # print(f'position : {position}, direction : {direction}')

        print(f"position : {position}, direction : {direction}")
        return (
            1000 * (position[1] + 1)
            + 4 * (position[0] + 1)
            + [RIGHT, DOWN, LEFT, UP].index(direction)
        )

    def cube_size(self):
        max_row = max(len(row) for row in self.map.values)
        max_col = len(self.map.values)
        print(f"max_row : {max_row}, max_col : {max_col}")
        return max(max_row, max_col) / 4

    def get_new_pos(self, pos_to_keep, new_direction):
        return (
            pos_to_keep
            if new_direction[0] == 0
            else (0 if new_direction[0] == 1 else self.map.cube_size - 1),
            pos_to_keep
            if new_direction[1] == 0
            else (0 if new_direction[1] == 1 else self.map.cube_size - 1),
        )

    def run_part2(self):
        cube = self.map.get_cube()
        face = cube.faces["front"]
        position = (0, face.values[0].index("."))
        direction = RIGHT

        print(f"position : {face.type} {position}")
        for step in self.path:
            if step == "L":
                print(
                    f" Turning left from {direction} to {(direction[1], -direction[0])}"
                )
                direction = (direction[1], -direction[0])
            elif step == "R":
                print(
                    f" Turning right from {direction} to {(-direction[1], direction[0])}"
                )
                direction = (-direction[1], direction[0])
            else:
                for i in range(step):
                    new_face = face
                    new_direction = direction
                    new_position = (
                        position[0] + direction[0],
                        position[1] + direction[1],
                    )

                    # check void
                    pos_to_keep = None
                    if new_position[0] < 0:  # left
                        new_face = cube.faces[face.neighbor_types["left"]]
                        pos_to_keep = new_position[1]
                    elif new_position[0] >= self.map.cube_size:  # right
                        new_face = cube.faces[face.neighbor_types["right"]]
                        pos_to_keep = new_position[1]
                    elif new_position[1] < 0:  # up
                        new_face = cube.faces[face.neighbor_types["up"]]
                        pos_to_keep = new_position[0]
                    elif new_position[1] >= self.map.cube_size:  # down
                        new_face = cube.faces[face.neighbor_types["down"]]
                        pos_to_keep = new_position[0]

                    if pos_to_keep is not None:
                        coming_from = [
                            dir
                            for dir, val in new_face.neighbor_types.items()
                            if val == face.type
                        ][0]
                        new_direction = DIRECTIONS[OPPOSITE[coming_from]]
                        if (direction, new_direction) in [
                            (DOWN, RIGHT),
                            (RIGHT, DOWN),
                            (LEFT, UP),
                            (UP, LEFT),
                            (DOWN, UP),
                            (UP, DOWN),
                            (LEFT, RIGHT),
                            (RIGHT, LEFT),
                        ]:
                            pos_to_keep = self.map.cube_size - pos_to_keep - 1
                        new_position = self.get_new_pos(pos_to_keep, new_direction)

                    # check wall
                    if new_face.values[new_position[1]][new_position[0]] == "#":
                        print(f"Wall found at {new_face.type} {new_position}")
                        break

                    # move
                    position = new_position
                    face = new_face
                    direction = new_direction
                    print(
                        f"face : {face.type}, position : {position}, direction : {direction}"
                    )

        final_position = (position[0] + face.coord[0], position[1] + face.coord[1])
        print(
            f"position : {final_position}, direction : {direction}, { [RIGHT, DOWN, LEFT, UP].index(direction)}"
        )
        return (
            1000 * (final_position[1] + 1)
            + 4 * (final_position[0] + 1)
            + [RIGHT, DOWN, LEFT, UP].index(direction)
        )


puzzle = Puzzle22()

puzzle.run(part1=False)
