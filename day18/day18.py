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
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x

    def __repr__(self):
        return f'p({self.x}, {self.y})'

class Day18:
    map_width: int
    map_height: int
    walls: list
    start: Point
    end: Point
    person: Point
    corrupted: list[Point]
    corrupted_numbers_to_use: int

    def __init__(self, in_txt, corrupted_numbers_to_use=None, is_debug=False):
        self.is_debug = is_debug
        if not self.is_debug:
            self.map_width = 71
            self.map_height = 71
            self.corrupted_numbers_to_use = corrupted_numbers_to_use or 1024
        else:
            self.map_width = 7
            self.map_height = 7
            self.corrupted_numbers_to_use = corrupted_numbers_to_use or 10
        self.parse_input(in_txt)
        self.path = []

    def parse_input(self, in_txt):
        in_map = re.findall(r"(\d+),(\d+)", in_txt)
        self.corrupted = [Point(int(x), int(y)) for x, y in in_map]
        self.walls = []
        for ic in range(self.corrupted_numbers_to_use):
            self.walls.append(self.corrupted[ic])
        self.start = Point(0, 0)
        self.person = Point(0, 0)
        self.end = Point(self.map_width - 1, self.map_height - 1)

    def print_map(self):
        for ih in range(self.map_height):
            for iw in range(self.map_width):
                p = Point(iw, ih)
                if p in self.walls:
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
    day = Day18(in_txt, None, is_debug=is_debug)
    print(day.dijkstra())
    day.print_map()

def golden(in_txt):
    corrupted_numbers_to_use = 1
    while True:
        day = Day18(in_txt, corrupted_numbers_to_use)
        result = day.dijkstra()
        print(f'Checking corrupted_numbers_to_use: {corrupted_numbers_to_use} -> {result}')
        if result == math.inf:
            print(f'corrupted_numbers_to_use: {corrupted_numbers_to_use}')
            break
        corrupted_numbers_to_use += 1

if __name__ == "__main__":
    debug = False
    # debug = True
    in_txt = get_input(debug)
    print('Silver:')
    silver(in_txt, debug)
    print('')
    print('Golden:')
    golden(in_txt)
    print('')
