from copy import deepcopy
import math
from common import Puzzle


class Puzzle20(Puzzle):
    def __init__(self):
        super().__init__(20)

    def parse_input(self):
        return [int(row) for row in self.input]

    def get_in_list(self, list_to_search, index):
        index = index % len(list_to_search)
        return list_to_search[index]

    def get_result(self, mix, key=1):
        init_index0 = self.parsed_input.index(0)
        index0 = [i for i, v in enumerate(mix) if v[0] == init_index0][0]
        original_indexes = [
            self.get_in_list(mix, index0 + num)[0] for num in [1000, 2000, 3000]
        ]
        print([self.parsed_input[index] for index in original_indexes])
        return sum(self.parsed_input[index] for index in original_indexes) * key

    def mix_list(self, original, mix=None, verbose=False, max_nb_process=None):
        if verbose:
            print("Mixing list")
        if mix is None:
            mix = list(enumerate(original))

        len_list = len(original) - 1
        for init_index, num in enumerate(original):
            curr_index = mix.index((init_index, num))
            if verbose:
                print(f"Processing {(init_index, num)}, current index {curr_index}")
            next_index = (curr_index + num + len_list) % len_list
            mix.pop(curr_index)
            mix.insert(next_index, (init_index, num))
            if verbose:
                print(
                    f"    Inserting {num} (initial {init_index}) from {curr_index} to {next_index} of the list"
                )
            # print("    reorder", [self.parsed_input[num[0]] if num != 'start' else "start"  for num in mix])
            if max_nb_process is not None and init_index >= max_nb_process:
                break
        return mix

    def run_part1(self):
        mix = self.mix_list([num for num in self.parsed_input])
        return self.get_result(mix)

    def run_part2(self):
        key = 811589153
        mix = None
        orig = [num * key for num in self.parsed_input]
        for i in range(10):
            mix = self.mix_list(orig, mix)
        return self.get_result(mix, key)


puzzle = Puzzle20()
puzzle.run()
