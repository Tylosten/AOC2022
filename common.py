from pathlib import Path
import requests


class Puzzle:
    def __init__(self, day):
        self.day = day
        self.session_file = Path(__file__).parent / "inputs" / "session.txt"
        self.input_file = Path(__file__).parent / "inputs" / f"day_{self.day}.txt"
        self.input_url = f"https://adventofcode.com/2022/day/{self.day}/input"
        self.input = self.get_input()

    def get_session(self):
        with open(self.session_file, "r") as f:
            return f.read()

    def set_session(self):
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
            return f.readlines()

    @property
    def parsed_input(self):
        return self.input

    def run_part1(self):
        pass

    def run_part2(self):
        pass

    def run(self, part1=True, part2=True):
        print(f"Puzzle day {self.day}")
        if part1:
            print(f"Part 1 : {self.run_part1()}")
        if part2:
            print(f"Part 2 : {self.run_part2()}")
