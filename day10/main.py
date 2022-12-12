from collections import deque
instructions: list[list[str | int]] = []

INPUT_FILE = "./input.txt"
with open(INPUT_FILE) as f:
    while line := f.readline():
        instructions.append(line.split())
        if len(instructions[-1]) == 2:
            instructions[-1][1] = int(instructions[-1][1])

reg = 1
cycle = 0
part1 = 0
positions: list[int] = []
for instruction in instructions:
    positions.append(reg)
    cycle += 1
    if (cycle - 20) % 40 == 0 and cycle <= 220:
        part1 += cycle * reg
    if instruction[0] == "addx":
        positions.append(reg)
        cycle += 1
        if (cycle - 20) % 40 == 0 and cycle <= 220:
            part1 += cycle * reg
        reg += instruction[1]
positions.append(reg)
print(f"Part 1: {part1}")

crt: list[str] = ["" for _ in range(6)]
for i in range(6):
    for j in range(40):
        if abs(j - positions[40*i + j]) <= 1:
            crt[i] += '#'
        else:
            crt[i] += '.'
print("Part 2:\n" + '\n'.join(crt))
