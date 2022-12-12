from typing import List, Set, Tuple
from collections import deque
import string

grid: List[str] = []

INPUT_FILE = "./input.txt"
with open(INPUT_FILE) as f:
    while line := f.readline().strip():
        grid.append(line)

heights = dict(zip(string.ascii_lowercase, range(26)))
heights['S'] = heights['a']
heights['E'] = heights['z']

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.y, self.y - other.y)

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def as_tuple(self) -> Tuple[int]:
        return (self.x, self.y)

    def __hash__(self) -> int:
        return hash(self.as_tuple())

    def valid(self, x_max: int, y_max: int) -> bool:
        return self.x >= 0 and self.x < x_max and self.y >= 0 and self.y < y_max
    
    def neighbors(self, x_max: int, y_max: int):
        points: List[Point] = (
            self + Point(0, 1),
            self + Point(0, -1),
            self + Point(1, 0),
            self + Point(-1, 0)
        )
        return set(filter(lambda point: point.valid(x_max, y_max), points))

start: Point = None
end: Point = None
for x, row in enumerate(grid):
    for y, c in enumerate(row):
        if c == 'S':
            start = Point(x, y)
        if c == 'E':
            end = Point(x, y)

height_map: List[List[int]] = [[heights[c] for c in row] for row in grid]
visited: Set[Point] = set()
def bfs(start: Point, end: Point) -> int:
    frontier = deque()
    frontier.append((start, 0))
    visited.add(start)
    while len(frontier) > 0:
        curr, level = frontier.popleft()
        if curr == end:
            return level

        curr_height = height_map[curr.x][curr.y]
        for neighbor in curr.neighbors(len(height_map), len(height_map[0])):
            if neighbor in visited:
                continue
            if height_map[neighbor.x][neighbor.y] - curr_height > 1:
                continue
            frontier.append((neighbor, level + 1))
            visited.add(neighbor)
    return -1

print(f"Part 1: {bfs(start, end)}")

visited = set()
def bfs_height(start: Point, target_height: int) -> int:
    frontier = deque()
    frontier.append((start, 0))
    visited.add(start)
    while len(frontier) > 0:
        curr, level = frontier.popleft()
        curr_height = height_map[curr.x][curr.y]
        if curr_height == target_height:
            return level

        for neighbor in curr.neighbors(len(height_map), len(height_map[0])):
            if neighbor in visited:
                continue
            if curr_height - height_map[neighbor.x][neighbor.y] > 1:
                continue
            frontier.append((neighbor, level + 1))
            visited.add(neighbor)
    return -1

print(f"Part 2: {bfs_height(end, heights['a'])}")
