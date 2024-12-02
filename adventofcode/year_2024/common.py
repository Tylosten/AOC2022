from pathlib import Path
from argparse import ArgumentParser
import requests

def get_input_url(day, year = 2024):
    return f"https://adventofcode.com/{year}/day/{day}/input"

def get_session():
    file_path = Path(__file__).parent / "session.txt"
    if Path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    session = input("Please enter your session cookie: ")
    with open(file_path, "w") as f:
        f.write(session)
    return session
    
def get_input_file_path(day, example = False):
    return (
        Path(__file__).parent / "inputs" / f"day_{day}.txt" 
        if not example else
        Path(__file__).parent / "inputs" / f"day_{day}_example.txt"
    )

def save_input(day, year = 2024, example = False):
    if example :
        print("Please enter the example input. Ctrl-D or Ctrl-Z ( windows ) to save it.")
        inpt = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            inpt.append(line)
        inpt = "\n".join(inpt)
    else :
        url = get_input_url(day, year)
        res = requests.get(url, cookies={"session": get_session()}, timeout=60)
        inpt = res.text
    file_path = get_input_file_path(day, example)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(inpt)

def get_input(day, year = 2024, example = False):
    file_path = get_input_file_path(day, example)
    if not Path.exists(file_path):
        save_input(day, year, example)
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip("\n ") for line in f.readlines()]

def init_day(day, year = 2024):
    save_input(day, year)
    save_input(day, year, example = True)
    with open(Path(__file__).parent / f"day_{day}.py", "w", encoding="utf-8") as f:
        f.write(
f"""\"\"\" Day {day} year {year} \"\"\"
from argparse import ArgumentParser
from common import get_input

DAY = {day}
YEAR = {year}

def solve_part1(example = False):
    inpt = get_input(DAY, YEAR, example)
    print(inpt)

def solve_part2(example = False):
    inpt = get_input(DAY, YEAR, example)
    print(inpt)

if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("-e", "--example", action="store_true")
    argparser.add_argument("-p", "--part", type=int, choices=[1, 2], default=1)
    args = argparser.parse_args()

    if args.part == 1:
        print(solve_part1(args.example))
    else:
        print(solve_part2(args.example))
""")


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("day", type=int, help="The day of the puzzle")
    arg_parser.add_argument("year", type=int, default=2024, help="The year of the puzzle", nargs="?")
    args = arg_parser.parse_args()
    init_day(args.day, args.year)
