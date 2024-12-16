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

class Person:
    def __init__(self, x, y, direction):
        self.position = Point(x, y)
        self.direction = direction

class Day16:
    is_golden = False
    map_width: int
    map_height: int
    walls: list
    start: Point
    end: Point
    person: Person

    def __init__(self, in_txt, is_golden=False):
        self.is_golden = is_golden
        self.parse_input(in_txt)

    def parse_input(self, in_txt):
        in_map = re.findall(r"([#.ES\n]+)", in_txt)
        map_lines = in_map[0].split('\n')
        map_lines = [x for x in map_lines if x != '']

        self.map_width = len(map_lines[0])
        self.map_height = len(map_lines)

        self.walls = []
        for ih in range(self.map_height):
            for iw in range(self.map_width):
                if map_lines[ih][iw] == '#':
                    self.walls.append(Point(iw, ih))
                elif map_lines[ih][iw] == 'E':
                    self.end = Point(iw, ih)
                elif map_lines[ih][iw] == 'S':
                    self.start = Point(iw, ih)
                    self.person = Person(iw, ih, '>')

    def print_map(self):
        for ih in range(self.map_height):
            for iw in range(self.map_width):
                p = Point(iw, ih)
                if p in self.walls:
                    print(Fore.RED + '#', end='')
                elif self.person.position == p:
                    print(Fore.GREEN + self.person.direction, end='')
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
        initial_direction = self.person.direction

        # Priority queue (min-heap)
        queue = []
        heapq.heappush(queue, (0, start, initial_direction))  # (cost, point, direction)

        visited = set()

        while queue:
            cost, current, direction = heapq.heappop(queue)

            state = (current.x, current.y, direction)
            if state in visited:
                continue
            visited.add(state)

            if current == end:
                return cost

            # Rotate (90 degrees left or right)
            current_dir_idx = directions.index(direction)
            for rotation in [-1, 1]:  # Left or right
                new_dir_idx = (current_dir_idx + rotation) % 4
                new_direction = directions[new_dir_idx]
                heapq.heappush(queue, (cost + 1000, current, new_direction))

            # Move forward
            dir_idx = directions.index(direction)
            dx, dy = direction_vectors[dir_idx]
            new_point = Point(current.x + dx, current.y + dy)

            if self.is_hall(new_point):
                heapq.heappush(queue, (cost + 1, new_point, direction))

        return math.inf

def silver(in_txt):
    day = Day16(in_txt)
    # day.print_map()
    print(day.dijkstra())

def golden(in_txt):
    day = Day16(in_txt, is_golden=True)

if __name__ == "__main__":
    # debug = False
    debug = True
    in_txt = get_input(debug)
    print('Silver:')
    silver(in_txt)
    print('')
    # print('Golden:')
    # golden(in_txt)
    # print('')
