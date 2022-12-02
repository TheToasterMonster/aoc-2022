INPUT_FILE = "./input.txt"
with open(INPUT_FILE) as f:
    input_str = f.read()

moves = {
    'A': 1,
    'X': 1,
    'B': 2,
    'Y': 2,
    'C': 3,
    'Z': 3
}
possible_moves = ['A', 'B', 'C']
outcomes = [
    [ 3, 0, 6 ],
    [ 6, 3, 0 ],
    [ 0, 6, 3 ]
]

def play(round):
    p1, p2 = moves[round[0]], moves[round[1]]
    return outcomes[p2 - 1][p1 - 1] + p2

rounds = list(map(str.split, input_str.splitlines()))
results = list(map(play, rounds))
print(f"Part 1: {sum(results)}")

def figure(round):
    p1, outcome = round[0], round[1]
    diff = moves[outcome] - 1
    return play([p1, possible_moves[((moves[p1] + diff - 1) - 1) % 3]])

new_results = list(map(figure, rounds))
print(f"Part 2: {sum(new_results)}")

