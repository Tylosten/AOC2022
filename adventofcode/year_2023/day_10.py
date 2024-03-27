from adventofcode.year_2023.puzzle2023 import Puzzle2023
import pandas as pd
import numpy as np


    
class Pipe : 
    def __init__(self, line, col, value, dist):
        self.value = value
        self.line = line
        self.col = col
        self.neigh = {}   
        self.dist = dist 
    
    @property
    def right(self):
        return self(self.line, self.col + 1)
    
    @property
    def left(self):
        return self(self.line, self.col - 1)
    
    @property
    def up(self):
        return self(self.line - 1, self.col)
    
    @property
    def down(self):
        return self(self.line + 1, self.col)
    
    def __repr__(self) -> str:
        return f"({self.line}, {self.col})"


class Puzzle10(Puzzle2023):
    def __init__(self):
        super().__init__(10)
        
        
    def parse_input(self):
        return(pd.DataFrame([[{ "shape" : char, "dist" :None} for char in line] for line in self.input]))
    
    def print_dist(self):
        strres = ''
        for i, line in enumerate(self.input) : 
            for j, char in enumerate(line) :
                dist = self.parsed_input.at[i,j]['dist']
                strres += str(f"[{self.parsed_input.at[i,j]['shape']}{dist if dist else '/'}]")
            strres += "\n"
        return strres
    
    def get_neigh_pipe(self, line, col, shape) :
        shape = self.parsed_input.at[line, col]["shape"]
        if shape == "S" : 
            if col + 1 < len(self.input[0]) and  self.parsed_input.at[line, col + 1]["shape"] in ["J", "-", "7"]: # RIGHT
                yield (line, col + 1)
            if col - 1 >= 0 and self.parsed_input.at[line, col - 1]["shape"] in ["F", "-", "L"]: # LEFT
                yield (line, col - 1)
            if line + 1 < len(self.input) and self.parsed_input.at[line + 1, col]["shape"] in ["J", "|", "L"]: # DOWN
                yield (line + 1, col)
            if line - 1 >= 0 and self.parsed_input.at[line - 1, col]["shape"] in ["F", "|", "7"]: # UP
                yield (line - 1, col)
        elif shape == "-" :
            yield (line, col + 1) # RIGHT
            yield (line, col - 1) # LEFT
        elif shape == "|" :
            yield (line + 1, col) # DOWN
            yield (line - 1, col) # UP
        elif shape == "L" :
            yield (line, col + 1) # RIGHT
            yield (line - 1, col) # UP
        elif shape == "7" :
            yield (line +1, col) # DOWN
            yield (line, col - 1) # LEFT
        elif shape == "J" :
            yield (line - 1, col) # UP
            yield (line, col - 1) # LEFT
        elif shape == "F" :
            yield (line, col + 1) 
            yield (line + 1 , col)
    
    def run_part1(self):
        for i, line  in enumerate(self.input):
            try :
                j = line.index('S')
                spipe = (i, j)
                self.parsed_input.at[i, j]["dist"] = 0
                print("S", spipe)
                break
            except ValueError:
                pass
        todo =  [(i, j)]
        while len(todo) > 0 :
            todo_lin, todo_col = todo.pop(0)
            todo_shape = self.parsed_input.at[todo_lin, todo_col]["shape"]
            todo_dist = self.parsed_input.at[todo_lin, todo_col]["dist"]
            for lin, col in self.get_neigh_pipe(todo_lin, todo_col, todo_shape) :
                if self.parsed_input.at[lin, col]["dist"] is None or self.parsed_input.at[lin, col]["dist"] > todo_dist + 1:
                    self.parsed_input.at[lin, col]["dist"] = todo_dist + 1
                    todo.append((lin, col))
        print(self.print_dist())

    
puzzle = Puzzle10()
puzzle.run()