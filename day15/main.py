pairs: list[list[tuple[int, int]]] = []

INPUT_FILE = "./input.txt"
with open(INPUT_FILE) as f:
    while line := f.readline().strip():
        left, right = line.split(':')
        lx, ly = left.split(',')
        rx, ry = right.split(',')
        lxeq, lyeq = lx.find('='), ly.find('=')
        rxeq, ryeq = rx.find('='), ry.find('=')
        sensor = (int(lx[lxeq+1:]), int(ly[lyeq+1:]))
        beacon = (int(rx[rxeq+1:]), int(ry[ryeq+1:]))
        pairs.append([sensor, beacon])

occupied = set.union(*map(set, pairs))

def between(x: int, y: int) -> set[int]:
    if x < y:
        return set(range(x, y + 1))
    else:
        return set(range(y, x + 1))

def dist(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def check(row: int) -> int:
    points: set[int] = set()
    for sensor, beacon in pairs:
        x1, y1 = sensor
        x2, y2 = beacon
        beacon_dist = dist(sensor, beacon)
        if row in between(y1 - beacon_dist, y1 + beacon_dist):
            half_width = beacon_dist - abs(row - y1)
            points |= between(x1 - half_width, x1 + half_width)
    return len(points - set(map(lambda p: p[0], filter(lambda p: p[1] == row, occupied))))

# print(f"Sample Part 1: {check(10)}")
print(f"Part 1: {check(2000000)}")

def create_lines(sensor: tuple[int, int], beacon: tuple[int, int]) -> list[tuple[int, int]]:
    radius: int = dist(sensor, beacon)
    top: tuple[int, int] = (sensor[0], sensor[1] - radius)
    bot: tuple[int, int] = (sensor[0], sensor[1] + radius)
    return [(1, top[0]-top[1]), (-1, top[0]+top[1]), (1, bot[0]-bot[1]), (-1, bot[0]+bot[1])]

def intersect_lines(l1: tuple[int, int], l2: tuple[int, int]) -> tuple[int, int]:
    dir1, a = l1
    dir2, b = l2
    if dir1 + dir2 != 0:
        raise Exception("These lines do not intersect")
    return ((a + b) // 2, dir1 * (b - a) // 2)

lines: list[tuple[int, int]] = []
for sensor, beacon in pairs:
    lines += create_lines(sensor, beacon)

ups: set[tuple[int, int]] = set()
downs: set[tuple[int, int]] = set()
for line in lines:
    if line[0] == 1:
        ups.add(line)
    else:
        downs.add(line)

def neighbors(point: tuple[int, int]) -> list[tuple[int, int]]:
    x, y = point
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

possible_points: dict[tuple[int, int], int] = {}
for up in ups:
    for down in downs:
        for neighbor in neighbors(intersect_lines(up, down)):
            if neighbor not in possible_points:
                possible_points[neighbor] = 0
            possible_points[neighbor] += 1

[empty] = [p for p in possible_points if possible_points[p] == 4]
print(f"Part 2: {empty[0] * 4000000 + empty[1]}")
