import re
from itertools import product
import time

from setuptools.command.bdist_egg import safety_flags


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


class Robot:
    is_golden = False
    map_width: int
    map_height: int
    x: int
    y: int
    vx: int
    vy: int

    def __init__(self, x, y, vx, vy, map_width, map_height, is_golden=False):
        self.is_golden = is_golden
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.map_width = map_width
        self.map_height = map_height

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0:
            self.x += self.map_width
        if self.x >= self.map_width:
            self.x -= self.map_width
        if self.y < 0:
            self.y += self.map_height
        if self.y >= self.map_height:
            self.y -= self.map_height

    def __str__(self):
        return f"[{self.x}, {self.y}] -> [{self.vx}, {self.vy}]"

class Day14:
    is_golden = False
    robots = []

    def __init__(self, in_txt, map_width, map_height, is_golden=False):
        self.is_golden = is_golden
        self.map_width = map_width
        self.map_height = map_height
        items = re.findall(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)", in_txt)
        self.robots = []
        for item in items:
            self.robots.append(Robot(int(item[0]), int(item[1]), int(item[2]), int(item[3]), self.map_width, self.map_height, is_golden))

    def move(self):
        for robot in self.robots:
            robot.move()

    def is_tree(self):
        arr = self.make_map()
        for ih in range(self.map_height):
            s = ''
            for iw in range(self.map_width):
                if arr[ih][iw] > 0:
                    s += '#'
                else:
                    s += '.'
            if s.find('#' * 10) >= 0:
                return True
        return False

    def make_map(self):
        arr = [[0 for _ in range(self.map_width)] for _ in range(self.map_height)]
        for robot in self.robots:
            arr[robot.y][robot.x] += 1
        return arr

    def print_map(self):
        arr = self.make_map()
        for ih in range(self.map_height):
            for iw in range(self.map_width):
                if arr[ih][iw] > 0:
                    print('#', end='')
                else:
                    print('.', end='')
            print('')
        print('')

    def calc_safety_factor(self):
        safety_factor = 1
        quadrants = [0, 0, 0, 0]
        w_2 = self.map_width // 2
        h_2 = self.map_height // 2
        for robot in self.robots:
            if robot.x < w_2:
                if robot.y < h_2:
                    quadrants[0] += 1
                elif robot.y > h_2:
                    quadrants[1] += 1
            elif robot.x > w_2:
                if robot.y < h_2:
                    quadrants[2] += 1
                elif robot.y > h_2:
                    quadrants[3] += 1
        for q in quadrants:
            safety_factor *= q
        return safety_factor

def silver(in_txt, map_width, map_height):
    day = Day14(in_txt, map_width, map_height)
    day.print_map()
    for i in range(100):
        day.move()
    print(day.calc_safety_factor())

def golden(in_txt, map_width, map_height):
    day = Day14(in_txt, map_width, map_height, is_golden=True)
    for i in range(10000):
        day.move()
        if day.is_tree():
            print(f'Found tree at {i+1}')
            break
    day.print_map()

if __name__ == "__main__":
    debug = False
    # debug = True
    if debug:
        map_width = 11
        map_height = 7
    else:
        map_width = 101
        map_height = 103
    in_txt = get_input(debug)
    print('Silver:')
    silver(in_txt, map_width, map_height)
    print('')
    print('Golden:')
    golden(in_txt, map_width, map_height)
    print('')
