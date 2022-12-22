INPUT_FILE = "./input.txt"
with open(INPUT_FILE) as f:
    winds: str = f.readline().strip()

Rock = set[tuple[int, int]]

rock1 = set((x, 4) for x in range(2, 6))
rock2 = set((x, 5) for x in range(2, 5)) | set((3, y) for y in range(4, 7))
rock3 = set((x, 4) for x in range(2, 5)) | set((4, y) for y in range(4, 7))
rock4 = set((2, y) for y in range(4, 8))
rock5 = set([(2, 4), (3, 4), (2, 5), (3, 5)])

rocks: list[Rock] = [rock1, rock2, rock3, rock4, rock5]

CHAMBER_WIDTH = 7
height = 0
curr: set[Rock] = set((x, 0) for x in range(0, CHAMBER_WIDTH))

def spawn_rock(i) -> Rock:
    rock = set(map(lambda p: (p[0], p[1] + height), rocks[i]))
    return rock

def is_valid(rock: Rock) -> bool:
    for point in rock:
        if point in curr or point[0] < 0 or point[0] >= CHAMBER_WIDTH:
            return False
    return True

def move_rock(rock: Rock, down: int=0, right: int=0) -> tuple[bool, Rock]:
    new_rock = set(map(lambda p: (p[0] + right, p[1] - down), rock))
    return (is_valid(new_rock), new_rock)

def print_curr() -> None:
    for y in reversed(range(1, height + 1)):
        for x in range(7):
            if (x, y) in curr:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print('-' * 7)
    print()

def simulate(total_rock_count) -> int:
    global curr, height
    curr = set((x, 0) for x in range(0, CHAMBER_WIDTH))
    height = 0
    moves_i = 0
    for i in range(total_rock_count):
        rock = spawn_rock(i % len(rocks))
        valid = True
        while valid:
            inside = valid = True
            if moves_i % 2 == 0:
                dir = 1 if winds[(moves_i//2) % len(winds)] == '>' else -1
                inside, next_rock = move_rock(rock, right=dir)
            else:
                valid, next_rock = move_rock(rock, down=1)
            moves_i += 1
            if inside and valid:
                rock = next_rock
        height = max(height, *(p[1] for p in rock))
        curr |= rock
    return height

print(f"Part 1: {simulate(2022)}")
#  print(f"Part 2: {simulate(1000000000000)}")
