import pprint

pp = pprint.PrettyPrinter()

class Valve:
    def __init__(self, rate: int, adj: list[str]):
        self.rate = rate
        self.adj = adj

    def __repr__(self) -> str:
        return f"Valve(rate={self.rate}, adj={self.adj})"

valves: dict[str, Valve] = {}

INPUT_FILE = "./input.txt"
with open(INPUT_FILE) as f:
    while line := f.readline().strip():
        left, right = line.split(';')
        i = len('Valve ')
        name = left[i:i+2]
        rate = int(left[left.find('=')+1:])
        i = right.find('valves ')
        n = len('valves ')
        if i == -1:
            i = right.find('valve ')
            n = len('valve ')
        xs = right[i+n:]
        xs = list(xs.split(', '))
        valves[name] = Valve(rate, xs)

# pp.pprint(valves)

def explore(valve: str, time: int, curr_pres: int=0, total_pres: int=0) -> int:
    if time == 0:
        return total_pres
    total_pres += curr_pres
    leave = max(map(lambda v: explore(v, time-1, curr_pres, total_pres), valves[valve].adj))
    take = 0
    if valves[valve].rate == 0:
        take = max(
                map(
                    lambda v: explore(v, time-2, curr_pres+valves[valve].rate, total_pres),
                    valves[valve].adj))
    return max(take, leave)

print(f"Part 1: {explore('AA', 30)}")
