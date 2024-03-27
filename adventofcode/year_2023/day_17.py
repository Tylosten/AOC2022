from adventofcode.year_2023.puzzle2023 import Puzzle2023
import pandas as pd
import numpy as np

possible_dir = {'up' : ['up', 'left', 'right'], 'down' : ['down', 'left', 'right'], 'left' : ['up', 'down', 'left'], 'right' : ['up', 'down', 'right']}
class ScoreList : 
    def __init__(self, heats, max_dist = 4, min_dist = 0):
        self.max_dist = max_dist
        self.min_dist = min_dist
        self.scores = [
            [
                {
                   direction : {
                       distance : {'x' : x, 'y' : y, 'direction' : direction, 'dist' : distance, 'score' : np.nan, 'visited' : False, 'heat' : heats[x][y]}  for distance in range(self.max_dist + 1)
                    }
                   for direction in ['up', 'down', 'left', 'right']
                }
                for y in range(len(heats[0]))
            ] 
            for x in range(len(heats))
        ]
        self.maxdist = 3
        self.lines = len(heats)
        self.cols = len(heats[0])
        self.best_score = np.nan
        
    def solve(self):
        self.scores[DIRECTIONS['down'][0]][DIRECTIONS['down'][1]]['down'][1]['score'] = self.scores[DIRECTIONS['down'][0]][DIRECTIONS['down'][1]]['down'][1]['heat']
        self.scores[DIRECTIONS['right'][0]][DIRECTIONS['right'][1]]['right'][1]['score'] = self.scores[DIRECTIONS['right'][0]][DIRECTIONS['right'][1]]['right'][1]['heat'] 
        todo = [
            self.scores[DIRECTIONS['down'][0]][DIRECTIONS['down'][1]]['down'][1], 
            self.scores[DIRECTIONS['right'][0]][DIRECTIONS['right'][1]]['right'][1]
        ]
        self.best_score = 100000
        
        while len(todo) > 0:
            todo = sorted(todo, key=lambda s: -s['score'] )
            curr = todo.pop()
            curr = self.scores[curr['x']][curr['y']][curr['direction']][curr['dist']]
            curr['visited'] = True
            neigh_scores_pts = []
            
            neigh_dirs = possible_dir[curr['direction']] if curr['dist'] >= self.min_dist else [curr['direction']]
            for neigh_dir in neigh_dirs:
                if curr['direction'] == neigh_dir and curr['dist'] >= self.max_dist :
                    continue
                neigh_x = curr['x'] + DIRECTIONS[neigh_dir][0]
                neigh_y = curr['y'] + DIRECTIONS[neigh_dir][1]
                if neigh_x < 0 or neigh_x >= self.lines or neigh_y < 0 or neigh_y >= self.cols:
                    continue
                if curr['direction'] == neigh_dir :
                    neigh_scores_pts += [self.scores[neigh_x][neigh_y][neigh_dir][curr['dist'] + 1]]
                else : 
                    neigh_scores_pts += [self.scores[neigh_x][neigh_y][neigh_dir][1]]

            neigh_scores_pts = [n for n in neigh_scores_pts if not n['visited']]            
            for neigh_score_pt in neigh_scores_pts:
                neigh_score = neigh_score_pt['heat'] + curr['score']
                if neigh_score >  self.best_score:
                    continue
                
                if neigh_score_pt['x'] == self.lines - 1 and neigh_score_pt['y'] == self.cols - 1:
                    if neigh_score_pt['dist'] >= self.min_dist :
                        neigh_score_pt['score'] = neigh_score
                        self.best_score = neigh_score
                        
                elif np.isnan(neigh_score_pt['score']) or neigh_score < neigh_score_pt['score']:
                    neigh_score_pt['score'] = neigh_score
                    if neigh_score_pt not in todo:
                        todo.append(neigh_score_pt)

    def get_best_score(self, x, y, dirs = ['up', 'down', 'right', 'left']):
        sel_score = None
        for dir in dirs :
            for score in self.scores[x][y][dir].values():
                if not np.isnan(score['score']) and (sel_score is None or score['score'] < sel_score['score']) :
                    sel_score = score
        return sel_score

    def print_best_path(self): 
        x = self.lines - 1
        y = self.cols - 1
        score = self.get_best_score(x,y)
        print(score)
        while x > 0 or y > 0 :
            direction = DIRECTIONS[score['direction']]
            x -= direction[0] * score['dist'] 
            y -= direction[1] * score['dist']
            score = self.get_best_score(x,y, dirs = ['up', 'down'] if score['direction'] in ['right', 'left'] else ['right', 'left'])
            print(score)


DIRECTIONS = {
    'up' : [-1, 0],
    'down' : [1, 0],
    'left' : [0, -1],
    'right' : [0, 1]
}

class Puzzle17(Puzzle2023):
    def __init__(self):
        super().__init__(17)
        
    def parse_input(self):
        return [[int(c) for c in l] for l in self.input]
        
    def get_score(self, scores, x, y, direction, dist):
        return scores[x][y][direction][dist]
        
    def run_part1(self):
        heats = self.parsed_input
        scores = ScoreList(heats, max_dist=4, min_dist=0)
        scores.solve()
        return scores.best_score 
    
    def run_part2(self):
        heats = self.parsed_input
        scores = ScoreList(heats, max_dist=10, min_dist=4)
        scores.solve()
        # scores.print_best_path()
        return scores.best_score  
        

puzzle = Puzzle17()
puzzle.run(part1=False)