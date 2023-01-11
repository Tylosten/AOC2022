from common import Puzzle
import re

ROCK = "rock"
PAPER = "paper"
SCISSOR = "scissor"

LOOSE = "loose"
DRAW = "draw"
WIN = "win"

game_scores = {LOOSE: 0, DRAW: 3, WIN: 6}
player1 = {"A": ROCK, "B": PAPER, "C": SCISSOR}
player2 = {"X": LOOSE, "Y": DRAW, "Z": WIN}
scores = {
    ROCK: {"base": 1, ROCK: DRAW, PAPER: LOOSE, SCISSOR: WIN},
    PAPER: {"base": 2, ROCK: WIN, PAPER: DRAW, SCISSOR: LOOSE},
    SCISSOR: {"base": 3, ROCK: LOOSE, PAPER: WIN, SCISSOR: DRAW},
}


class Puzzle2(Puzzle):
    def __init__(self):
        super().__init__(2)

    def parsed_input(self):
        games = []
        for game in self.input:
            if game != "":
                p1, p2 = re.match(r"(\w) (\w)", game).groups()
                games.append([p1, p2])
        return games

    def run_part1(self):
        pass

    def get_player2(self, p1, p2):
        for i, val in scores.items():
            if val[player1[p1]] == player2[p2]:
                return i

    def score2(self, p1, p2):
        play1_game = player1[p1]
        play2_game = self.get_player2(p1, p2)
        base_score = scores[play2_game]["base"]
        game_score = game_scores[scores[play2_game][play1_game]]

        # print(
        #     f"{p1} ({play1_game}) {p2} ({player2[p2]} -> {play2_game}) :  {base_score} + {game_score}"
        # )

        return base_score + game_score

    def run_part2(self):
        score = 0
        for g in self.parsed_input():
            score += self.score2(g[0], g[1])
        return score


puzzle = Puzzle2()
puzzle.run()
