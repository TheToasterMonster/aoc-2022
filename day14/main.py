from copy import deepcopy

paths: list[list[tuple[int, int]]] = []

INPUT_FILE = "./input.txt"
with open(INPUT_FILE) as f:
    while line := f.readline().strip():
        tokens = line.split(' -> ')
        paths.append(list(map(lambda s: tuple(map(int, s.split(','))), tokens)))

minX: int = 1000
maxX: int = -1
maxY: int = -1
for path in paths:
    for x, y in path:
        minX = min(minX, x)
        maxX = max(maxX, x)
        maxY = max(maxY, y)

def expand_path(path: list[tuple[int, int]]) -> set[tuple[int, int]]:
    points: set[tuple[int, int]] = set()
    for i in range(1, len(path)):
        startX, startY = path[i - 1]
        endX, endY = path[i]
        if startX == endX:
            minY = min(startY, endY)
            maxY = max(startY, endY)
            points |= set((startX, y) for y in range(minY, maxY + 1))
        else:
            minX = min(startX, endX)
            maxX = max(startX, endX)
            points |= set((x, startY) for x in range(minX, maxX + 1))
    return points

orig_sand_map: set[tuple[int, int]] = set.union(*map(expand_path, paths))
sand_map: set[tuple[int, int]] = deepcopy(orig_sand_map)

def options(sand: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = sand
    return [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]

def drop(sand: tuple[int, int]) -> bool:
    if sand[0] < minX or sand[1] > maxX:
        return False
    for option in options(sand):
        if option not in sand_map:
            return drop(option)
    sand_map.add(sand)
    return True

start: tuple[int, int] = (500, 0)
count: int = 0
while drop(start):
    count += 1
print(f"Part 1: {count}")

sand_map = deepcopy(orig_sand_map)
floor = maxY + 2

def drop_with_floor(sand: tuple[int, int]):
    if sand[1] + 1 < floor:
        for option in options(sand):
            if option not in sand_map:
                return drop_with_floor(option)
    sand_map.add(sand)

count = 0
while start not in sand_map:
    drop_with_floor(start)
    count += 1
print(f"Part 2: {count}")
