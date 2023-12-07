from copy import deepcopy
import re
from adventofcode.year_2023.puzzle2023 import Puzzle2023

class Range:
    def __init__(self, start_dest, start_src, len):
        if len < 0:
            raise ValueError(f"Length must be positive : {start_dest}, {start_src}, {len}")
        self.start_dest = start_dest
        self.start_src = start_src
        self.length = len

    @property
    def end_dest(self):
        return self.start_dest + self.length - 1
    
    @property
    def end_src(self):
        return self.start_src + self.length - 1
    
    def __repr__(self) -> str:
        return f"({self.start_src}, {self.end_src}) => ({self.start_dest}, {self.end_dest})"

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
                    start_dest = int(match.group(1))
                    start_src = int(match.group(2))
                    length = int(match.group(3))
                    res['maps'][label].append(Range(start_dest, start_src, length))
                    
        for label in res['maps']:
            res['maps'][label] = sorted(res['maps'][label], key = lambda range : range.start_src)
        return res
    
    def convert(self, maps, source):
        for corres in maps:
            if corres.start_src <= source <= corres.end_src :
                return corres.start_dest + source - corres.start_src
        return source
    
    def convert_to_target(self, from_label, target_label, sources):
        label = from_label
        tmp = deepcopy(sources)
        while label != target_label:
            next_label = self.parsed_input['corres_map'][label]
            maps = self.parsed_input['maps'][f"{label}-to-{next_label}"]
            tmp = [self.convert(maps, source) for source in tmp]
            label = next_label
        return tmp
    
    def run_part1(self):
        print(self.parsed_input["corres_map"])
        locations = self.convert_to_target('seed', 'location', self.parsed_input['seeds'])
        return min(locations)
    
    
    def convert_range(self, maps, range):
        new_range = None    
        for corres in maps:
            if corres.start_src <= range.start_dest <= corres.end_src :
                # print(f"Found corres {corres} for {range.start_dest}")
                diff = range.start_dest - corres.start_src
                next_start_dest =  corres.start_dest + diff
                remain_len = min(corres.length - diff, range.length)
                new_range = Range(next_start_dest, range.start_src, remain_len)
                break
        if new_range is None:
            # print(f"No corres found for {range.start_dest}")
            try : 
                next_start_dest = min([corres.start_src for corres in maps if corres.start_src > range.start_dest])
                remain_len = next_start_dest - range.start_dest
                if remain_len > range.length:
                    remain_len = range.length
            except ValueError:
                remain_len = range.length
            new_range = Range(range.start_dest, range.start_src, remain_len) 
        
        if new_range.length == range.length:
            # print(f"New range {new_range}")
            return [new_range]

        next_range = Range( 
            range.start_dest + new_range.length, 
            range.start_src + new_range.length, 
            range.length - new_range.length)
        # print(f"New range {new_range} and next range {next_range}")
        return [new_range] + self.convert_range(maps, next_range)
             
        
    def combine_maps(self, maps1, maps2):
        ranges = []
        for range1 in maps1:
            # print(f" ====================== Convert {range1}")
            ranges += self.convert_range(maps2, range1)
            
        return ranges
    
    def combine_maps_to_target(self, from_label, target_label):
        label = from_label
        tmp_maps = None
        while label != target_label:
            next_label = self.parsed_input['corres_map'][label]
            print(f" ====================== Combine {label} to {next_label} ================================ ")
            maps = self.parsed_input['maps'][f"{label}-to-{next_label}"]
            tmp_maps = maps if tmp_maps is None else self.combine_maps(tmp_maps, maps)
            label = next_label
        return tmp_maps

    def run_part2(self):
        seeds = []
        i = 0
        while  i < len(self.parsed_input['seeds']) - 1:
            start_seed = self.parsed_input['seeds'][i]
            len_seed = self.parsed_input['seeds'][i + 1]
            seeds.append(Range(start_seed, start_seed, len_seed))
            i += 2
        seeds = sorted(seeds, key = lambda range : range.start_src)
        maps = self.combine_maps_to_target('seed', 'location')
        maps = self.combine_maps(seeds, maps)
        return min(r.start_dest for r in maps)
        
        
puzzle = Puzzle5()
puzzle.run()