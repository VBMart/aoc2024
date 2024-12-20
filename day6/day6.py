import re
import math
import functools
import concurrent.futures
import time
from multiprocessing import Pool


debug_in_txt = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""

def get_input(debug: bool = False):
    if debug:
        return debug_in_txt
    with open('day6.txt', 'r') as f:
        return f.read()

direction_map = {
    '^': (-1, 0, '>'),
    '>': (0, 1, 'V'),
    'V': (1, 0, '<'),
    '<': (0, -1, '^'),
}

class Step:
    r: int
    c: int
    d: str

    def __init__(self, r, c, d):
        self.r = r
        self.c = c
        self.d = d

    def __repr__(self):
        return f'Step: {self.r}x{self.c} {self.d}'

    def __eq__(self, other):
        return self.r == other.r and self.c == other.c and self.d == other.d

    def __hash__(self):
        return hash((self.r, self.c, self.d))


class Guard:
    r: int
    c: int
    d: str
    world_map: dict
    places: dict
    map_w: int
    map_h: int
    leave: bool
    loop: bool
    history: set

    def __init__(self, r, c, d):
        self.r = r
        self.c = c
        self.d = d
        self.map_h = 0
        self.map_w = 0
        self.world_map = []
        self.places = []
        self.history = set()
        self.loop = False
        self.leave = False

    def __repr__(self):
        return f'Guard: {self.r}x{self.c} {self.d} leave: {self.leave}, cnt: {self.get_places_count()}'

    def print_arr(self, arr):
        for ih in range(0, self.map_h):
            s = ""
            for iw in range(0, self.map_w):
                s += arr[ih][iw]
            print(s)
        print('')

    def print_map(self):
        self.print_arr(self.world_map)

    def print_places(self):
        self.print_arr(self.places)


    def make_step(self):
        if self.leave or self.loop:
            return

        dr, dc, next_d = direction_map[self.d]
        new_r, new_c = self.r + dr, self.c + dc

        if new_r < 0 or new_r >= self.map_h or new_c < 0 or new_c >= self.map_w:
            self.leave = True
            return

        if self.world_map[new_r][new_c] != '#':
            self.r, self.c = new_r, new_c
            self.places[self.r][self.c] = 'X'
        else:
            self.d = next_d

        # key = f'{self.r}x{self.c}'
        # if key in self.history:
        #     if self.history[key][2] == self.d:
        #         self.loop = True
        #         return
        # else:
        #     self.history[key] = (self.r, self.c, self.d)
        current_step = Step(r=self.r, c=self.c, d=self.d)
        # current_step = (self.r, self.c, self.d)
        if current_step in self.history:
            self.loop = True
        else:
            self.history.add(current_step)

    def get_places_count(self):
        cnt = 0
        for ih in range(0, self.map_h):
            for iw in range(0, self.map_w):
                if self.places[ih][iw] == 'X':
                    cnt += 1
        return cnt

    def go(self):
        for i in range(0, self.map_w * self.map_h):
            self.make_step()
            if self.leave:
                return 0
            if self.loop:
                return 1

    def parse_map(self, lines):
        self.world_map = []
        self.places = []
        self.history = set()
        self.loop = False
        self.leave = False
        self.map_h = len(lines)
        self.map_w = len(lines[0])
        for ih in range(0, self.map_h):
            m_l = []
            g_l = []
            for iw in range(0, self.map_w):
                cell = lines[ih][iw]
                m_l.append(cell)
                if cell == '^':
                    self.r = ih
                    self.c = iw
                    self.d = '^'
                    g_l.append('X')
                else:
                    g_l.append('.')
            self.world_map.append(m_l)
            self.places.append(g_l)


def silver(in_txt):
    lines = re.findall(r"([^\n]+)\n?", in_txt)
    guard = Guard(0, 0, '^')
    guard.parse_map(lines)
    guard.go()
    print(guard)


def golden(in_txt = None):
    lines = re.findall(r"([^\n]+)\n?", in_txt)
    guard = Guard(0, 0, '^')
    guard.parse_map(lines)
    guard.go()
    loop_cnt = 0
    print(f'{guard.map_w}x{guard.map_h}')
    tasks = []
    for step in guard.history:
        # tasks.append((guard.history[step][0], guard.history[step][1]))
        tasks.append((step.r, step.c))
        # tasks.append((step[0], step[1]))
    tasks = set(tasks)
    print(f'Tasks: {len(tasks)}')

    t1 = time.time()
    i = 0
    for task in tasks:
        i += 1
        if i % 1000 == 0:
            print(f'Processed: {i} / {len(tasks)} time: {time.time() - t1}')
        # if i >= 100:
        #     break
        ih, iw = task
        guard = Guard(0, 0, '^')
        guard.parse_map(lines)
        guard.world_map[ih][iw] = '#'
        guard.go()
        if guard.loop:
            loop_cnt += 1
        # print(f'Time spent: {time.time() - start_time}')
    print(f'Total time spent: {time.time() - t1}')

    print(loop_cnt)

def check_loop(inpt):
    ih, iw, lines = inpt
    guard = Guard(0, 0, '^')
    guard.parse_map(lines)
    guard.world_map[ih][iw] = '#'
    guard.go()
    if guard.loop:
        return 1
    return 0

def golden_thr(int_txt):
    lines = re.findall(r"([^\n]+)\n?", in_txt)
    guard = Guard(0, 0, '^')
    guard.parse_map(lines)
    guard.go()
    map_w = guard.map_w
    map_h = guard.map_h
    print(f'{map_w}x{map_h}')
    tasks = []
    for step in guard.history:
        tasks.append((step.r, step.c, tuple(lines)))
    tasks = set(tasks)
    print(f'Tasks: {len(tasks)}')

    start_time = time.time()
    with Pool(12) as p:
        results = p.map(check_loop, tasks)
        print(sum(results))
    # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #     results = list(executor.map(check_loop, tasks))
    #     # print(results)
    #     print(sum(results))
    print(f'Time spent: {time.time() - start_time}')

if __name__ == "__main__":
    # in_txt = get_input(debug=True)
    in_txt = get_input(debug=False)
    print('Silver:')
    silver(in_txt)
    print('')
    print('Golden:')
    golden(in_txt)
    print('')
    golden_thr(in_txt)
