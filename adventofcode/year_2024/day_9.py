""" Day 9 year 2024 """
from argparse import ArgumentParser
from common import get_input

DAY = 9
YEAR = 2024


def solve_part1(example = False):
    inpt = get_input(DAY, YEAR, example)
    disk = inpt[0]
    files = {}
    for i, space_len in enumerate(disk):
        if i % 2 == 0:
            files[i//2] = int(space_len)
    
    # print(files)
    compact_disk = []
    for i, space_len in enumerate(disk):
        space_len = int(space_len)
        if i % 2 == 0: # file
            file_id = i//2
            if file_id in files:
                compact_disk += [file_id] * files[file_id]
                del files[file_id]
        else: # free space
            while space_len > 0:
                if len(files) == 0:
                    break
                last_file_id = max(files.keys())
                last_file_len = files[last_file_id]
                if last_file_len > space_len:
                    files[last_file_id] -= space_len
                    compact_disk += [last_file_id] * space_len
                    space_len = 0
                else:
                    space_len -= last_file_len
                    del files[last_file_id]
                    compact_disk += [last_file_id] * last_file_len
        if len(files) == 0:
            break
        # print(compact_disk)
        # print(files)
    # print(compact_disk)
    return sum(file_id*index for index, file_id in enumerate(compact_disk))
        
def disk_arr(files):
    disk_arr = []
    for file in files :
        disk_arr += [file["id"]] * file["file"]
        disk_arr += [0] * file["freespace"]
    return disk_arr  

def solve_part2(example = False):
    inpt = get_input(DAY, YEAR, example)
    disk = inpt[0]
    
    files = []
    for i, space_len in enumerate(disk):
        if i % 2 == 0:
            files.append({
                "file" : int(space_len),
                "id" : i//2,
                "freespace" : int(disk[i + 1]) if i + 1 < len(disk) else 0
            })
            
    for file_id in reversed(range(len(files))):
        # print(f" ===== File {file_id}")
        file_pos, file_len = [(pos, f['file']) for pos, f in enumerate(files) if f["id"] == file_id][0]
        # print(f"   len {file_len}, pos {file_pos}")
        possible_freespaces = [free_pos for free_pos, f in enumerate(files[:file_pos]) if f["freespace"] >= file_len]
        # print(possible_freespaces)
        if len(possible_freespaces) == 0:
            continue
        fsp_pos = possible_freespaces[0]
        # warning : order of the following lines is important
        files[file_pos - 1]["freespace"] += file_len + files[file_pos]["freespace"]
        files.remove(files[file_pos])
        files.insert(fsp_pos + 1, {
            "file" : file_len,
            "id" : file_id,
            "freespace" : files[fsp_pos]["freespace"] - file_len
        })
        files[fsp_pos]["freespace"] = 0
        # print(disk_arr(files))

    arr = disk_arr(files)
    return sum(file_id*index for index, file_id in enumerate(arr))
        

if __name__ == "__main__":
    argparser = ArgumentParser()
    argparser.add_argument("-e", "--example", action="store_true")
    argparser.add_argument("-p", "--part", type=int, choices=[1, 2], default=1)
    args = argparser.parse_args()

    if args.part == 1:
        print(solve_part1(args.example))
    else:
        print(solve_part2(args.example))
