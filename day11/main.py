from typing import List
from collections import deque
from copy import deepcopy
import pprint

pp = pprint.PrettyPrinter()

class Monkey:
    def __init__(self, items: List[int], op, test_int, test, t, f):
        self.items = deque(items)
        self.op = op
        self.test_int = test_int
        self.test = test
        self.t = t
        self.f = f

    def __repr__(self) -> str:
        return f"Monkey(items={self.items})"

def parse_op(s: str):
    _, op = s.split(' = ')
    return lambda old: eval(op)

def parse_monkey(f) -> Monkey:
    line = f.readline()
    if not line.startswith("Monkey"):
        return None
    
    _, items = f.readline().strip().split(': ')
    items = list(map(int, items.split(', ')))
    _, op = f.readline().strip().split(': ')
    op = parse_op(op)
    test_line = f.readline().strip().split()
    test_int = int(test_line[-1])
    test = lambda x: x % test_int == 0
    true_line = f.readline().strip().split()
    t = int(true_line[-1])
    false_line = f.readline().strip().split()
    f = int(false_line[-1])
    return Monkey(items, op, test_int, test, t, f)

input_monkeys = []
INPUT_FILE = "./input.txt"
with open(INPUT_FILE) as f:
    while monkey := parse_monkey(f):
        input_monkeys.append(monkey)
        f.readline()

# pp.pprint(input_monkeys)

def prod(arr: List[int]) -> int:
    x: int = 1
    for i in arr:
        x *= i
    return x

monkeys = deepcopy(input_monkeys)
inspections: List[int] = [0 for _ in range(len(monkeys))]
for _ in range(20):
    for i in range(len(monkeys)):
        while len(monkeys[i].items) > 0:
            inspections[i] += 1
            item = monkeys[i].items.popleft()
            item = monkeys[i].op(item)
            item //= 3
            if monkeys[i].test(item):
                monkeys[monkeys[i].t].items.append(item)
            else:
                monkeys[monkeys[i].f].items.append(item)
print(f"Part 1: {prod(sorted(inspections, reverse=True)[:2])}")

test_prod: int = prod([monkey.test_int for monkey in input_monkeys])

monkeys = deepcopy(input_monkeys)
inspections = [0 for _ in range(len(monkeys))]
for _ in range(10_000):
    for i in range(len(monkeys)):
        while len(monkeys[i].items) > 0:
            inspections[i] += 1
            item = monkeys[i].items.popleft()
            item = monkeys[i].op(item)
            item %= test_prod
            if monkeys[i].test(item):
                monkeys[monkeys[i].t].items.append(item)
            else:
                monkeys[monkeys[i].f].items.append(item)
print(f"Part 2: {prod(sorted(inspections, reverse=True)[:2])}")
