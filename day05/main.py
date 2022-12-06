from copy import deepcopy

stacks: list[list[str]] = [[] for _ in range(10)]
instructions: list[tuple[int]] = []

INPUT_FILE = "./input.txt"
with open(INPUT_FILE) as f:
    for _ in range(8):
        line = f.readline()
        i = 1
        while i < len(line):
            if crate := line[i].strip():
                stacks[i//4 + 1].insert(0, crate)
            i += 4
    f.readline()
    f.readline()
    while line := f.readline().strip():
        tokens = line.split()
        instructions.append(tuple(map(int, (tokens[1], tokens[3], tokens[5]))))

stacks1 = deepcopy(stacks)

def move1(amount, first, second):
    for i in range(amount):
        stacks1[second].append(stacks1[first].pop())

for instruction in instructions:
    move1(*instruction)

print(f'Part 1: {"".join([s[-1] for s in stacks1[1:]])}')

stacks2 = deepcopy(stacks)

def move2(amount, first, second):
    to_move: list[int] = []  # use like stack
    for _ in range(amount):
        to_move.append(stacks2[first].pop())
    for _ in range(amount):
        stacks2[second].append(to_move.pop())

for instruction in instructions:
    move2(*instruction)

print(f'Part 1: {"".join([s[-1] for s in stacks2[1:]])}')
