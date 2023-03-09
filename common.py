from pathlib import Path
import requests


class Puzzle:
    def __init__(self, day):
        self.day = day
        self.session_file = (
            Path(__file__).parent / "inputs" / "session.txt"
        )  # the path to the session.txt file
        self.input_file = (
            Path(__file__).parent / "inputs" / f"day_{self.day}.txt"
        )  # the path to the input file
        self.input_url = f"https://adventofcode.com/2022/day/{self.day}/input"  # the url to get the input from
        self.input = self.get_input()  # the input
        self.parsed_input = self.parse_input()  # the parsed input

    def get_session(self):
        """Reads the session from a file.

        This function reads the session from the file specified in the
        `session_file` attribute. If the file does not exist, it is created.
        """
        with open(self.session_file, "r") as f:
            return f.read()

    def set_session(self):
        """This function takes the session cookie and writes it to the session file"""
        session = input("Please enter your session cookie: ")
        with open(self.session_file, "w") as f:
            f.write(session)

    def get_input(self):
        if not Path.exists(self.input_file):
            session = self.get_session()
            res = requests.get(self.input_url, cookies={"session": session}, timeout=60)
            inpt = res.text
            with open(self.input_file, "w") as f:
                f.write(inpt)
        with open(self.input_file, "r") as f:
            return [line.strip("\n ") for line in f.readlines()]

    def parse_input(self):
        return self.input

    def run_part1(self):
        """"""
        pass

    def run_part2(self):
        """This function runs the second part of the puzzle"""
        pass

    def run(self, part1=True, part2=True):
        print(f"Puzzle day {self.day}")
        if part1:
            print(f"Part 1 : {self.run_part1()}")
        if part2:
            print(f"Part 2 : {self.run_part2()}")
