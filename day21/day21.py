import array
import heapq
import math
import os
import re
from colorama import Fore, Back, Style, init
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


directions = ['>', 'v', '<', '^']
direction_vectors = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Point:
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def __eq__(self, other):
        return self.r == other.r and self.c == other.c

    def __lt__(self, other):
        if self.r == other.r:
            return self.c < other.c
        return self.r < other.r

    def __repr__(self):
        return f'p({self.r}, {self.c})'

class Pad:
    def __init__(self, keypad, start):
        self.keypad = keypad
        self.width = len(keypad[0])
        self.height = len(keypad)
        self.height = 4
        self.position = start

    def get_current_button(self):
        return self.keypad[self.position.x][self.position.y]

    def get_target_position(self, button):
        for r in range(self.height):
            for c in range(self.width):
                if self.keypad[r][c] == button:
                    return Point(r, c)
        return None

    def get_moves(self, password):
        moves = ''
        for btn in password:
            if btn == self.get_current_button():
                moves += 'A'
            else:
                pass

class NumPad(Pad):
    def __init__(self):
        keypad = [
            [ '7', '8', '9'],
            [ '4', '5', '6'],
            [ '1', '2', '3'],
            [None, '0', 'A'],
        ]
        super().__init__(keypad, Point(3, 2))

class DirPad(Pad):
    def __init__(self):
        keypad = [
            [None, '^', 'A'],
            [ '<', 'v', '>'],
        ]
        super().__init__(keypad, Point(0, 2))

class Day21:


    def __init__(self, in_txt):
        self.start = None
        self.end = None
        self.person = None
        self.map_width = 0
        self.map_height = 0
        self.path = []
        self.cheats = []
        self.parse_input(in_txt)

    def parse_input(self, in_txt):
        self.path = []
        map_lines = in_txt.split('\n')
        self.map_height = len(map_lines)
        self.map_width = len(map_lines[0])
        self.walls = []
        for ih in range(self.map_height):
            for iw in range(self.map_width):
                if map_lines[ih][iw] == '#':
                    self.walls.append(Point(iw, ih))
                elif map_lines[ih][iw] == 'E':
                    self.end = Point(iw, ih)
                elif map_lines[ih][iw] == 'S':
                    self.start = Point(iw, ih)
                    self.person = Point(iw, ih)

    def print_map(self):
        for ih in range(self.map_height):
            for iw in range(self.map_width):
                p = Point(iw, ih)
                if p in self.walls:
                    if p in self.cheats:
                        print(Fore.YELLOW + 'C', end='')
                    else:
                        print(Fore.RED + '#', end='')
                elif p in self.path:
                    if self.start == p:
                        print(Fore.GREEN + 'S', end='')
                    elif self.end == p:
                        print(Fore.GREEN + 'E', end='')
                    else:
                        print(Fore.BLUE + 'O', end='')
                elif self.person == p:
                    print(Fore.GREEN + '🙂', end='')
                elif self.start == p:
                    print(Fore.GREEN + 'S', end='')
                elif self.end == p:
                    print(Fore.GREEN + 'E', end='')
                else:
                    print(Fore.RESET + '.', end='')
            print('')
        print(Fore.RESET + '')

    def is_hall(self, point):
        """Check if the point is within bounds and not a wall."""
        if point.x < 0 or point.x >= self.map_width:
            return False
        if point.y < 0 or point.y >= self.map_height:
            return False
        if point in self.walls:
            return False
        return True

    def dijkstra(self):
        start = self.start
        end = self.end

        # Priority queue (min-heap)
        queue = []
        heapq.heappush(queue, (0, start))  # (cost, point, direction)

        visited = set()
        parents = {}

        while queue:
            cost, current = heapq.heappop(queue)

            state = (current.x, current.y)
            if state in visited:
                continue
            visited.add(state)

            if current == end:
                self.path = []
                current = state
                while current in parents:
                    self.path.append(Point(current[0], current[1]))
                    current = parents[current]
                self.path.append(Point(current[0], current[1]))
                self.path.reverse()
                return cost

            for direction in directions:
                dir_idx = directions.index(direction)
                dx, dy = direction_vectors[dir_idx]
                new_point = Point(current.x + dx, current.y + dy)

                new_state = (new_point.x, new_point.y)
                if self.is_hall(new_point) and new_state not in visited:
                    heapq.heappush(queue, (cost + 1, new_point))
                    parents[new_state] = state

        return math.inf

def silver(in_txt, is_debug):
    day = Day20(in_txt)
    print(f'Start: {day.start}')
    print(f'End: {day.end}')
    cheat_limit = 100
    if is_debug:
        cheat_limit = 1
    initial_path_time = day.dijkstra()
    initial_path = day.path
    cheat_times = {}
    walls = []
    for wall in day.walls:
        if wall.x < 0 or wall.x >= day.map_width:
            continue
        if wall.y < 0 or wall.y >= day.map_height:
            continue
        walls.append(wall)
    for i_wall in range(len(walls)):
        wall = walls[i_wall]

        ip_start = len(initial_path)
        ip_end = -1

        for dir_idx in range(len(directions)):
            dx, dy = direction_vectors[dir_idx]
            new_point = Point(wall.x + dx, wall.y + dy)
            if new_point in initial_path:
                ip = initial_path.index(new_point)
                if ip_end < ip:
                    ip_end = ip
                if ip_start > ip:
                    ip_start = ip

        if ip_start >= ip_end:
            continue

        ip_delta = ip_end - ip_start - 2
        if ip_delta < cheat_limit:
            continue

        if ip_delta not in cheat_times:
            cheat_times[ip_delta] = 0
        cheat_times[ip_delta] += 1
        day.cheats.append(wall)

    day.print_map()
    cheat_times = {k: v for k, v in sorted(cheat_times.items(), key=lambda item: item[0])}
    cheat_numbers = 0
    for k, v in cheat_times.items():
        print(f'Cheats: {v} times for {k} steps')
        cheat_numbers += v
    print(f'Cheats: {cheat_numbers} times')


def golden(in_txt, is_debug):
    day = Day20(in_txt)
    print(f'Start: {day.start}')
    print(f'End: {day.end}')
    cheat_limit = 100
    if is_debug:
        cheat_limit = 50
    initial_path_time = day.dijkstra()
    initial_path = day.path
    cheat_times = {}

    for i_path in range(len(initial_path)):
        for j_path in range(i_path + cheat_limit, len(initial_path)):
            ip_start = i_path
            ip_end = j_path
            ip_delta = ip_end - ip_start

            p_start = initial_path[ip_start]
            p_end = initial_path[ip_end]
            dx = p_end.x - p_start.x
            dy = p_end.y - p_start.y
            l = abs(dx) + abs(dy)
            if l > 20 or l == 1:
                continue
            if l + cheat_limit <= ip_delta:
                new_delta = ip_delta - l
                if new_delta not in cheat_times:
                    cheat_times[new_delta] = 0
                cheat_times[new_delta] += 1

    cheat_times = {k: v for k, v in sorted(cheat_times.items(), key=lambda item: item[0])}
    cheat_numbers = 0
    for k, v in cheat_times.items():
        print(f'Cheats: {v} times for {k} steps')
        cheat_numbers += v
    print(f'Cheats: {cheat_numbers} times')

if __name__ == "__main__":
    debug = False
    # debug = True
    in_txt = get_input(debug)
    # print('Silver:')
    # silver(in_txt, debug)
    # print('')
    print('Golden:')
    golden(in_txt, debug)
    print('')
