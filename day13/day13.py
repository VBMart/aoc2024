import re
from itertools import product
import time

def get_input(debug: bool = False):
    file_name = 'input.txt'
    if debug:
        file_name = 'example.txt'
    with open(file_name, 'r') as f:
        return f.read()

def print_arr(arr):
    for row in arr:
        if type(row) == list:
            if type(row[0]) == int:
                print(''.join([str(x) for x in row]))
            elif type(row[0]) == bool:
                print(''.join(['#' if x else '.' for x in row]))
            else:
                print(''.join([s for s in row]))
        else:
            print(row)
    print('')


class Machine:
    is_golden = False
    dxa: int
    dya: int
    dxb: int
    dyb: int
    px: int
    py: int

    def __init__(self, dxa, dya, dxb, dyb, px, py, is_golden=False):
        self.is_golden = is_golden
        self.dxa = dxa
        self.dya = dya
        self.dxb = dxb
        self.dyb = dyb
        self.px = px
        self.py = py
        if self.is_golden:
            self.px += 10000000000000
            self.py += 10000000000000

    def get_n(self):
        x = self.px
        y = self.py
        t = x * self.dya - y * self.dxa
        b = self.dxb * self.dya - self.dyb * self.dxa
        nb = t // b
        na = (x - nb * self.dxb) // self.dxa
        if na * self.dxa + nb * self.dxb == x and na * self.dya + nb * self.dyb == y:
            return na, nb
        return None, None

    def __str__(self):
        return f"[A({self.dxa}, {self.dya}) B({self.dxb}, {self.dyb}), P({self.px}, {self.py})]"

class Day13:
    is_golden = False
    machines = []

    def __init__(self, in_txt, is_golden=False):
        self.is_golden = is_golden
        items = re.findall(r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)", in_txt)
        self.machines = []
        for item in items:
            self.machines.append(Machine(int(item[0]), int(item[1]), int(item[2]), int(item[3]), int(item[4]), int(item[5]), is_golden))

    def find_machines(self):
        sum_tokens = 0
        for machine in self.machines:
            na, nb = machine.get_n()
            if na is not None:
                tokens = 3 * na + nb
                sum_tokens += tokens
                # print(f"Machine {machine} gives {tokens} tokens")
        return sum_tokens

def silver(in_txt):
    day = Day13(in_txt)
    print(day.find_machines())

def golden(in_txt):
    day = Day13(in_txt, is_golden=True)
    print(day.find_machines())


if __name__ == "__main__":
    # in_txt = get_input(debug=True)
    in_txt = get_input(debug=False)
    print('Silver:')
    silver(in_txt)
    print('')
    print('Golden:')
    golden(in_txt)
    print('')
