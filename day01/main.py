elves: list[list[int]] = []

FILE_PATH = "./input.txt"
with open(FILE_PATH) as f:
    input_str: list[str] = list(map(str.strip, f.read().splitlines()))

elf: list[int] = []
for line in input_str:
    if line:
        elf.append(int(line))
    else:
        elves.append(elf)
        elf = []
if elf:
    elves.append(elf)

sums: list[int] = sorted(list(map(sum, elves)), reverse=True)
print(f"Part 1: {sums[0]}")
print(f"Part 2: {sum(sums[0:3])}")
