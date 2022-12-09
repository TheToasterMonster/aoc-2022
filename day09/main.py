moves: list[tuple[str, int]] = []

INPUT_FILE = "./input.txt"
with open(INPUT_FILE) as f:
    while line := f.readline():
        tokens = line.split()
        moves.append((tokens[0], int(tokens[1])))

class Point():
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def as_tuple(self):
        return (self.x, self.y)

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

head: Point = Point(0, 0)
tail: Point = Point(0, 0)

dirs: dict[str, Point] = {
    'R': Point(1, 0),
    'L': Point(-1, 0),
    'U': Point(0, 1),
    'D': Point(0, -1)
}

def update(head, tail):
    if abs(head.x - tail.x) >= 2 and abs(head.y - tail.y) >= 2:
        tail.x += (head.x - tail.x) // abs(head.x - tail.x)
        tail.y += (head.y - tail.y) // abs(head.y - tail.y)
    elif abs(head.x - tail.x) >= 2:
        tail.y = head.y
        tail.x += (head.x - tail.x) // abs(head.x - tail.x)
    elif abs(head.y - tail.y) >= 2:
        tail.x = head.x
        tail.y += (head.y - tail.y) // abs(head.y - tail.y)

visited: set[tuple[int, int]] = set()
visited.add(tail.as_tuple())

for dir, amount in moves:
    for _ in range(amount):
        head += dirs[dir]
        update(head, tail)
        visited.add(tail.as_tuple())

print(f"Part 1: {len(visited)}")

knots: list[Point] = [Point(0, 0) for _ in range(10)]

visited.clear()
visited.add(knots[-1].as_tuple())

for dir, amount in moves:
    for _ in range(amount):
        knots[0] += dirs[dir]
        for i in range(1, len(knots)):
            update(knots[i-1], knots[i])
        visited.add(knots[-1].as_tuple())

print(f"Part 2: {len(visited)}")
