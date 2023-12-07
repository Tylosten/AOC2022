from copy import deepcopy
import re
from adventofcode.year_2023.puzzle2023 import Puzzle2023

class Puzzle5(Puzzle2023):
    def __init__(self):
        super().__init__(5)
        
    def parse_input(self):
        res = {"maps" : {}, "seeds" : [], "corres_map" : {}}
        label = None
        for line in self.input:
            if line.startswith('seeds:') :
                res["seeds"] = [int(nb) for nb in line.split(':')[1].strip().split(' ')]
            match = re.match(r'(\w+)-to-(\w+) map:', line)
            
            if match :
                from_label = match.group(1)
                to_label = match.group(2)
                label = f"{from_label}-to-{to_label}"
                res['maps'][label] = []
                res['corres_map'][from_label] = to_label
                
            else :
                match = re.match(r'(\d+) (\d+) (\d+)', line)
                if match :
                    res['maps'][label].append([int(nb) for nb in line.split(' ')])
        return res
    
    def convert(self, from_label, to_label, source):
        maps = self.parsed_input['maps'][f"{from_label}-to-{to_label}"]
        for corres in maps:
            dest_start = corres[0]
            src_start = corres[1]
            length = corres[2]
            if src_start <= source <= (src_start + length):
                return dest_start + source - src_start
        return source
    
    def convert_to_target(self, from_label, target_label, sources):
        label = from_label
        tmp = deepcopy(sources)
        while label != target_label:
            next_label = self.parsed_input['corres_map'][label]
            tmp = [self.convert(label, next_label, source) for source in tmp]
            label = next_label
        return tmp
    
    def run_part1(self):
        print(self.parsed_input["corres_map"])
        locations = self.convert_to_target('seed', 'location', self.parsed_input['seeds'])
        return min(locations)
    
    def build_corres_map(self, from_label, to_label):
        next_label = self.parsed_input['corres_map'][from_label]
        if to_label == next_label:
            return self.parsed_input['maps'][f"{from_label}-to-{to_label}"]
        
        second_next_label = self.parsed_input['corres_map'][next_label]
        if to_label == second_next_label:
            
            map1 = self.parsed_input['maps'][f"{from_label}-to-{next_label}"]
            map2 = self.parsed_input['maps'][f"{next_label}-to-{second_next_label}"]
            
            for starttmp1, startsrc1, len1 in map1:
                for startdest2, starttmp2, len2 in map2:
                    if starttmp2 <= starttmp1 <= (starttmp2 + len2):
                        newstartdest = startdest2 + starttmp1 - starttmp2
                        newlen = min()
                        if start
                        
                    if starttmp1 == starttmp2:
                        return [[startdest2, startsrc1, len1]]
                startdest = self.convert(next_label, to_label, starttmp1)
        
puzzle = Puzzle5()
puzzle.run()