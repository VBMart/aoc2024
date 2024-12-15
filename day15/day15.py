import array
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

deltas = {
    '^': (0, -1),
    'v': (0, 1),
    '<': (-1, 0),
    '>': (1, 0)
}

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'p({self.x}, {self.y})'

class Day15:
    is_golden = False
    robot: Point
    boxes: array
    walls: array
    map_width: int
    map_height: int
    moves: array

    def __init__(self, in_txt, is_golden=False):
        self.is_golden = is_golden
        self.parse_input(in_txt)

    def parse_input(self, in_txt):
        in_map = re.findall(r"([#.O@\n]+)", in_txt)
        map_lines = in_map[0].split('\n')
        map_lines = [x for x in map_lines if x != '']
        in_moves = re.findall(r"([<>^v])", in_txt)

        self.moves = in_moves
        self.map_width = len(map_lines[0])
        self.map_height = len(map_lines)

        self.boxes = []
        self.walls = []
        for ih in range(self.map_height):
            for iw in range(self.map_width):
                if map_lines[ih][iw] == '#':
                    self.walls.append(Point(iw, ih))
                elif map_lines[ih][iw] == 'O':
                    self.boxes.append(Point(iw, ih))
                elif map_lines[ih][iw] == '@':
                    self.robot = Point(iw, ih)

    def make_step(self, direction):
        new_x = self.robot.x + deltas[direction][0]
        new_y = self.robot.y + deltas[direction][1]
        new_p = Point(new_x, new_y)
        if new_p in self.walls:
            # print('wall')
            return
        if new_p in self.boxes:
            # print('box')
            boxes_stack = []
            is_stack_found = False
            i = 1
            s_p = None
            while not is_stack_found:
                s_x = self.robot.x + deltas[direction][0] * i
                s_y = self.robot.y + deltas[direction][1] * i
                s_p = Point(s_x, s_y)
                if s_p in self.boxes:
                    boxes_stack.append(s_p)
                else:
                    is_stack_found = True
                    if s_p in self.walls:
                        # print('wall after stack')
                        return
                i += 1
            # print(boxes_stack)
            self.boxes.remove(boxes_stack[0])
            self.boxes.append(s_p)
        self.robot.x = new_x
        self.robot.y = new_y

    def run(self, show_steps=False):
        i_move = 0
        for move in self.moves:
            if show_steps:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f'Step: {move} {i_move} / {len(self.moves)}')
            self.make_step(move)
            if show_steps:
                self.print_map()
                time.sleep(0.01)
            i_move += 1

    def calc_distances(self):
        sum = 0
        for box in self.boxes:
            distance = 100 * box.y + box.x
            sum += distance
        return sum

    def print_map(self):
        for ih in range(self.map_height):
            for iw in range(self.map_width):
                p = Point(iw, ih)
                if p in self.walls:
                    print(Fore.RED + '#', end='')
                elif p in self.boxes:
                    print(Fore.GREEN + 'O', end='')
                elif self.robot == p:
                    print(Back.WHITE + Fore.BLACK + '@', end='')
                else:
                    print('.', end='')
            print('')
        print('')


def silver(in_txt):
    day = Day15(in_txt)
    day.print_map()
    day.run(True)
    day.print_map()
    print(f'Distances: {day.calc_distances()}')

def golden(in_txt):
    day = Day15(in_txt, is_golden=True)

if __name__ == "__main__":
    init(autoreset=True)
    debug = False
    # debug = True
    in_txt = get_input(debug)
    print('Silver:')
    silver(in_txt)
    print('')
    # print('Golden:')
    # golden(in_txt)
    # print('')
