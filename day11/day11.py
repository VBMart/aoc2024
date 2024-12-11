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
            print(''.join([str(x) for x in row]))
        else:
            print(row)
    print('')


class Day11:
    is_golden = False
    stones = []

    def __init__(self, in_txt, is_golden=False):
        self.is_golden = is_golden
        items = re.findall(r"(\d+)", in_txt)
        self.stones = [int(a) for a in items]

    def fill_from_int(self, n):
        self.stones = [n]

    def blink(self):
        new_stones = []
        for i in range(len(self.stones)):
            stone = self.stones[i]
            s_stone = f'{stone}'
            len_stones = len(s_stone)
            if stone == 0:
                new_stones.append(1)
            elif len_stones % 2 == 0:
                l_stone = s_stone[:len_stones // 2]
                r_stone = s_stone[len_stones // 2:]
                new_stones.append(int(l_stone))
                new_stones.append(int(r_stone))
            else:
                new_stones.append(2024 * stone)
        self.stones = new_stones
        # print(self.stones)

def silver(in_txt):
    day11 = Day11(in_txt)
    for i in range(25):
        day11.blink()
    print(len(day11.stones))

def golden(in_txt):
    day11 = Day11(in_txt, is_golden=True)
    cnt = []
    # p1 = 40
    # p2 = 75
    p1 = 40
    p2 = 75
    t = time.time()
    for i in range(p1):
        day11.blink()
    print(f'Iteration {i} passed (time: {time.time() - t}) (n={len(day11.stones)})')

    i = 0
    t = time.time()
    cache = {}
    d = Day11('0', is_golden=True)
    for stone in day11.stones:
        if i % 1000000 == 0:
            print(f'Iteration {i // 1000000} / {len(day11.stones) // 1000000 } (cache: {len(cache)}) (time: {time.time() - t})')
            t = time.time()
        n = cache.get(stone, None)
        if n:
            cnt.append(n)
        else:
            d.fill_from_int(stone)
            for i in range(p1, p2):
                d.blink()
            cache[stone] = len(d.stones)
            cnt.append(len(d.stones))
        i += 1

    sum = 0
    for c in cnt:
        sum += c
    print(sum)


if __name__ == "__main__":
    # in_txt = get_input(debug=True)
    in_txt = get_input(debug=False)
    print('Silver:')
    silver(in_txt)
    print('')
    t1 = time.time()
    print('Golden:')
    golden(in_txt)
    print('Time spent: ', time.time() - t1)
    print('')
