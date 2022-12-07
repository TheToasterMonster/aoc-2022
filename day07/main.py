from copy import deepcopy
import pprint

pp = pprint.PrettyPrinter()

curr_path: list[str] = []
file_tree = {}

def get(path: list[str], tree: dict[str, any]) -> dict[str, any]:
    if path[0] not in tree or tree[path[0]] == "dir":
        tree[path[0]] = {}
    if len(path) == 1:
        return tree[path[0]]
    return get(path[1:], tree[path[0]])

INPUT_FILE = "./input.txt"
with open(INPUT_FILE) as f:
    while line := f.readline().strip():
        tokens: list[str] = line.split()
        if tokens[0] == "$":
            if tokens[1] == "cd":
                if tokens[2] == "..":
                    curr_path.pop()
                else:
                    curr_path.append(tokens[2])
        else:
            get(curr_path, file_tree)[tokens[1]] = int(tokens[0]) if tokens[0].isnumeric() else tokens[0]

#  pp.pprint(file_tree)

sizes = []
def dfs(dir: dict[str, any] | int, track=True) -> int:
    if type(dir) is int:
        return dir
    else:
        total_size = 0
        for subdir in dir:
            total_size += dfs(dir[subdir], track)
        if track:
            sizes.append(total_size)
        return total_size

dfs(file_tree)
print(f"Part 1: {sum(filter(lambda x: x <= int(1e5), sizes))}")

size = lambda d: dfs(d, track=False)
needed: int = int(3e7) - (int(7e7) - size(file_tree))
print(f"Part 2: {min(filter(lambda x: x >= needed, sizes))}")
