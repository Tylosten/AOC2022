import pstats
from common import Puzzle
from copy import deepcopy
from PIL import Image, ImageDraw
import cProfile

LINE = "line"
CROSS = "cross"
CORNER = "corner"
COLUMN = "column"
SQUARE = "square"
ROCK_SHAPES = [LINE, CROSS, CORNER, COLUMN, SQUARE]


class Rock:
    def __init__(self, x, y, shape):
        self.left_bottom_x = x
        self.left_bottom_y = y
        self.shape = shape
        if shape not in ROCK_SHAPES:
            raise ValueError("Invalid shape")

    def __repr__(self):
        return f"{self.shape}({self.left_bottom_x}, {self.left_bottom_y})"

    @property
    def top(self):
        if self.shape == LINE:
            return self.left_bottom_y
        if self.shape == CROSS:
            return self.left_bottom_y + 2
        if self.shape == CORNER:
            return self.left_bottom_y + 2
        if self.shape == COLUMN:
            return self.left_bottom_y + 3
        if self.shape == SQUARE:
            return self.left_bottom_y + 1

    @property
    def right(self):
        if self.shape == LINE:
            return self.left_bottom_x + 3
        if self.shape == CROSS:
            return self.left_bottom_x + 2
        if self.shape == CORNER:
            return self.left_bottom_x + 2
        if self.shape == COLUMN:
            return self.left_bottom_x
        if self.shape == SQUARE:
            return self.left_bottom_x + 1

    def get_coords(self):
        if self.shape == LINE:
            return [
                (self.left_bottom_x, self.left_bottom_y),
                (self.left_bottom_x + 1, self.left_bottom_y),
                (self.left_bottom_x + 2, self.left_bottom_y),
                (self.left_bottom_x + 3, self.left_bottom_y),
            ]
        if self.shape == CROSS:
            return [
                (self.left_bottom_x + 1, self.left_bottom_y),
                (self.left_bottom_x, self.left_bottom_y + 1),
                (self.left_bottom_x + 1, self.left_bottom_y + 1),
                (self.left_bottom_x + 2, self.left_bottom_y + 1),
                (self.left_bottom_x + 1, self.left_bottom_y + 2),
            ]
        if self.shape == CORNER:
            return [
                (self.left_bottom_x, self.left_bottom_y),
                (self.left_bottom_x + 1, self.left_bottom_y),
                (self.left_bottom_x + 2, self.left_bottom_y),
                (self.left_bottom_x + 2, self.left_bottom_y + 1),
                (self.left_bottom_x + 2, self.left_bottom_y + 2),
            ]
        if self.shape == COLUMN:
            return [
                (self.left_bottom_x, self.left_bottom_y),
                (self.left_bottom_x, self.left_bottom_y + 1),
                (self.left_bottom_x, self.left_bottom_y + 2),
                (self.left_bottom_x, self.left_bottom_y + 3),
            ]
        if self.shape == SQUARE:
            return [
                (self.left_bottom_x, self.left_bottom_y),
                (self.left_bottom_x + 1, self.left_bottom_y),
                (self.left_bottom_x, self.left_bottom_y + 1),
                (self.left_bottom_x + 1, self.left_bottom_y + 1),
            ]
        raise ValueError("Invalid shape")

    def collision(self, other_rock):
        for coord in self.get_coords():
            for other_coord in other_rock.get_coords():
                if coord[0] == other_coord[0] and coord[1] == other_coord[1]:
                    return True
        return False

    def draw(self, draw, color):
        for coord in self.get_coords():
            draw.rectangle(
                (
                    coord[0] * 100,
                    coord[1] * 100,
                    (coord[0] + 1) * 100,
                    (coord[1] + 1) * 100,
                ),
                fill=color,
            )


class RockPattern:
    def __init__(self, rocks_nb_before, first_top, rocks, height):
        self.rocks_nb_before = rocks_nb_before
        self.rocks = rocks
        self.height = height
        self.first_top = first_top

    def get_top(self, rocks_nb):
        pattern_nb = int((rocks_nb - self.rocks_nb_before) / len(self.rocks))
        rough_estimate = self.first_top + (pattern_nb - 1) * self.height
        missing_rocks_nb = (
            rocks_nb - self.rocks_nb_before - pattern_nb * len(self.rocks)
        )
        if missing_rocks_nb == 0:
            return rough_estimate
        missing_height = (
            max(rock.top for rock in self.rocks[:missing_rocks_nb]) - self.first_top
        )
        return rough_estimate + missing_height + 1

    def __repr__(self) -> str:
        string = f"RockPattern : beginning after {self.rocks_nb_before} rocks, first top : {self.first_top}, height : {self.height}\n"
        string += ", ".join(
            [
                f"{rock.shape}({rock.left_bottom_x}, {rock.left_bottom_y })"
                for rock in self.rocks
            ]
        )
        return string


class Chamber:
    def __init__(self, wind_pattern, width=7):
        self.width = width
        self.rocks = []
        self.falling_rock = None
        self.colors = {
            LINE: "red",
            CROSS: "green",
            CORNER: "blue",
            COLUMN: "yellow",
            SQUARE: "purple",
        }
        self.top = -1
        self.wind_pattern = wind_pattern
        self.wind = []
        self.repeat_wind_nb = 0
        self.repeat_wind_rock_index = []

    def is_falling_rock_collision(self):
        return (
            self.falling_rock.left_bottom_y < 0
            or self.falling_rock.left_bottom_x < 0
            or self.falling_rock.right >= self.width
            or (
                self.falling_rock.left_bottom_y <= self.top
                and any(self.falling_rock.collision(rock) for rock in self.rocks)
            )
        )

    def blow_wind(self, direction):
        if self.falling_rock is None:
            raise ValueError("No rock to blow")
        wind = 1 if direction == ">" else -1
        self.falling_rock.left_bottom_x += wind
        if self.is_falling_rock_collision():
            self.falling_rock.left_bottom_x -= wind

    def move_falling_rock_down(self):
        """Move the falling rock down if possible

        Raises:
            ValueError: If there is no falling rock

        Returns:
            bool: True if the rock has landed, False otherwise
        """
        if self.falling_rock is None:
            raise ValueError("No rock to move down")
        self.falling_rock.left_bottom_y -= 1
        if self.is_falling_rock_collision():
            self.falling_rock.left_bottom_y += 1
            self.rocks.append(self.falling_rock)
            self.top = max(self.falling_rock.top, self.top)
            self.falling_rock = None
            return True
        return False

    def find_pattern(self):
        """Find if there is a pattern in the rocks
        returns :
            bool: If there is a pattern, returns starting rock nb, first occurence and second occurence
        """
        repeat_wind_nb = self.repeat_wind_nb / 3
        if int(repeat_wind_nb) != repeat_wind_nb:
            return False
        repeat_wind_nb = int(repeat_wind_nb)
        index1 = self.repeat_wind_rock_index[repeat_wind_nb - 1]
        index2 = self.repeat_wind_rock_index[repeat_wind_nb * 2 - 1]
        index3 = self.repeat_wind_rock_index[repeat_wind_nb * 3 - 1]
        first = self.rocks[index1:index2]
        second = self.rocks[index2:index3]
        if first[0].shape == second[0].shape and "".join(
            [str(rock.left_bottom_x) for rock in first]
        ) == "".join([str(rock.left_bottom_x) for rock in second]):
            first_top = max(rock.top for rock in first)
            pattern_height = second[0].left_bottom_y - first[0].left_bottom_y
            pattern = RockPattern(
                rocks_nb_before=index1,
                first_top=first_top,
                rocks=second,
                height=pattern_height,
            )
            print(f"pattern found : {pattern}")
            return pattern
        print("no pattern found")
        return False

    def add_rock(self, shape: str) -> bool:
        """Add a rock to the chamber.

        Args:
            shape (str): The shape of the rock to add.

        Returns:
            bool: True if a pattern is found, False otherwise.
        """
        self.falling_rock = Rock(2, self.top + 4, shape)
        collision = False
        while not collision:
            if len(self.wind) == 0:
                self.wind = deepcopy(self.wind_pattern)
                if len(self.rocks) != 0:
                    self.repeat_wind_nb += 1
                    self.repeat_wind_rock_index.append(len(self.rocks))
                    pattern = self.find_pattern()
                    if pattern:
                        return pattern
            self.blow_wind(self.wind.pop(0))
            collision = self.move_falling_rock_down()
        return False

    def get_top(self, rocks_nb: int) -> int:
        """Return the top of the rocks after adding rocks_nb rocks"""
        pattern = False
        for i in range(rocks_nb):
            pattern = self.add_rock(ROCK_SHAPES[i % len(ROCK_SHAPES)])
            if pattern:
                return pattern.get_top(rocks_nb)
        return self.top + 1

    def draw(self):
        """Draw the current state of the chamber"""
        im = Image.new("RGB", (self.width * 100, (self.top + 10) * 100), color="white")
        draw = ImageDraw.Draw(im)
        if self.falling_rock is not None:
            self.falling_rock.draw(draw, self.colors[self.falling_rock.shape])
        for rock in self.rocks:
            rock.draw(draw, self.colors[rock.shape])
        im.transpose(Image.FLIP_TOP_BOTTOM).show()

    def simplify(self):
        """Remove the rocks that are not visible"""
        try:
            bottom = min(
                max(coord[1] for coord in self.rocks if coord[0] == i)
                for i in range(self.width)
            )
            self.rocks = [rock for rock in self.rocks if rock[1] > bottom - 5]
        except ValueError:
            ## chamber can't be simplify, there's at least a column without any rock
            pass


class Puzzle17(Puzzle):
    def __init__(self):
        super().__init__(17)

    def parse_input(self):
        return list(self.input[0][:-1])

    def run_part1(self):
        chamber = Chamber(wind_pattern=self.parsed_input)
        for i in range(2022):
            chamber.add_rock(ROCK_SHAPES[i % len(ROCK_SHAPES)])
        return chamber.top + 1

    def run_part2(self):
        chamber = Chamber(wind_pattern=self.parsed_input)
        return chamber.get_top(1000000000)


puzzle = Puzzle17()
puzzle.run(part2=False)
# cProfile.run('puzzle.run(part1=False)', filename='puzzle17.profile')

# with  open('puzzle17profile.txt', 'w') as file :
#     profile = pstats.Stats('puzzle17.profile', stream=file)
#     profile.sort_stats('cumulative') # Sorts the result according to the supplied criteria
#     profile.print_stats(15) # Prints the first 15 lines of the sorted report
