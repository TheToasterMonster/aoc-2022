INPUT_FILE = "./input.txt"
with open(INPUT_FILE) as f:
    input_lst = list(filter(id, map(str.strip, f.readlines())))

pairs = list(map(lambda s: s.split(','), input_lst))
pairs = list(map(lambda pair: (pair[0].split('-'), pair[1].split('-')), pairs))
pairs = [(list(map(int, x)), list(map(int, y))) for x, y in pairs]

def check1(pair):
    (a, b), (x, y) = pair
    if (a <= x and b >= y) or (x <= a and y >= b):
        return 1
    else:
        return 0

print(f"Part 1: {sum(map(check1, pairs))}")

def check2(pair):
    (a, b), (x, y) = sorted(pair)
    if b >= x or (a == x and y >= b):
        return 1
    else:
        return 0

print(f"Part 2: {sum(map(check2, pairs))}")
