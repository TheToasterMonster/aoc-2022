import pprint

pp = pprint.PrettyPrinter()

class Valve:
    def __init__(self, rate: int, adj: list[str]) -> None:
        self.rate: int = rate
        self.adj: list[str] = adj

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

class Data:
    def __init__(self) -> None:
        self.rate: int = 0
        self.total: int = 0
        self.path: set[str] = set()

rounds: list[dict[str, Data]] = [{s: Data() for s in valves} for _ in range(31)]
