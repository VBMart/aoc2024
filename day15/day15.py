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
                    print(Back.WHITE + Fore.BLACK + ' ', end='')
                else:
                    print('.', end='')
            print('')
        print('')


class Day15Golden:
    robot: Point
    boxes: array
    walls: array
    map_width: int
    map_height: int
    moves: array
    highlited_wall: Point

    def __init__(self, in_txt):
        self.i_move = 0
        self.stack = []
        self.is_stack_movable = False
        self.highlited_wall = None
        self.parse_input(in_txt)

    def parse_input(self, in_txt):
        in_map = re.findall(r"([#.O@\n]+)", in_txt)
        map_lines = in_map[0].split('\n')
        map_lines = [x for x in map_lines if x != '']
        in_moves = re.findall(r"([<>^v])", in_txt)

        self.moves = in_moves
        self.map_width = 2 * len(map_lines[0])
        self.map_height = len(map_lines)

        self.boxes = []
        self.walls = []
        for ih in range(self.map_height):
            for iw in range(len(map_lines[0])):
                p = Point(2*iw, ih)
                if map_lines[ih][iw] == '#':
                    self.walls.append(p)
                    self.walls.append(Point(2*iw+1, ih))
                elif map_lines[ih][iw] == 'O':
                    self.boxes.append(p)
                elif map_lines[ih][iw] == '@':
                    self.robot = p

    def get_check_directions(self, direction, is_robot, find_wall=False):
        deltas_for_check = []
        if direction == '>':
            if is_robot:
                deltas_for_check.append((1, 0))
            else:
                deltas_for_check.append((2, 0))
        elif direction == '<':
            if is_robot:
                deltas_for_check.append((-2, 0))
            else:
                if find_wall:
                    deltas_for_check.append((-1, 0))
                else:
                    deltas_for_check.append((-2, 0))
        elif direction == '^':
            if is_robot:
                deltas_for_check.append((0, -1))
                deltas_for_check.append((-1, -1))
            else:
                deltas_for_check.append((0, -1))
                deltas_for_check.append((1, -1))
                if not find_wall:
                    deltas_for_check.append((-1, -1))
        elif direction == 'v':
            if is_robot:
                deltas_for_check.append((0, 1))
                deltas_for_check.append((-1, 1))
            else:
                deltas_for_check.append((0, 1))
                deltas_for_check.append((1, 1))
                if not find_wall:
                    deltas_for_check.append((-1, 1))
        return deltas_for_check

    def find_boxes_stack(self, p: Point, is_robot, direction):
        deltas_for_check = self.get_check_directions(direction, is_robot, False)
        for d in deltas_for_check:
            new_x = p.x + d[0]
            new_y = p.y + d[1]
            new_p = Point(new_x, new_y)
            if new_p in self.boxes:
                if new_p in self.stack:
                    continue
                self.stack.append(new_p)
                box_deltas = self.get_check_directions(direction, False, True)
                for bd in box_deltas:
                    wall_x = new_p.x + bd[0]
                    wall_y = new_p.y + bd[1]
                    wall_p = Point(wall_x, wall_y)
                    if wall_p in self.walls:
                        self.is_stack_movable = False
                        self.highlited_wall = wall_p
                        return
                self.find_boxes_stack(new_p, False, direction)

    def make_step(self, direction):
        self.stack = []
        self.highlited_wall = None
        new_x = self.robot.x + deltas[direction][0]
        new_y = self.robot.y + deltas[direction][1]
        new_p = Point(new_x, new_y)
        if new_p in self.walls:
            self.highlited_wall = new_p
            return

        self.is_stack_movable = True
        self.find_boxes_stack(self.robot, True, direction)
        if self.i_move == 1391:
            self.print_map()
            print(self.stack)
        if len(self.stack) != 0:
            if self.is_stack_movable:
                for i_box in range(len(self.stack)):
                    self.boxes.remove(self.stack[i_box])
                    self.stack[i_box] = Point(self.stack[i_box].x + deltas[direction][0], self.stack[i_box].y + deltas[direction][1])
                    self.boxes.append(self.stack[i_box])
            else:
                return

        self.robot.x = new_x
        self.robot.y = new_y

    def run(self, show_steps=False):
        self.i_move = 0
        for move in self.moves:
            if show_steps:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f'Step: {move} {self.i_move} / {len(self.moves)}')
            self.make_step(move)
            if show_steps:
                self.print_map()
                time.sleep(0.1)
            self.i_move += 1

    def calc_distances(self):
        sum = 0
        for box in self.boxes:
            distance = 100 * box.y + box.x
            sum += distance
        return sum

    def print_map(self):
        for ih in range(self.map_height):
            iw = 0
            while iw < self.map_width:
                p = Point(iw, ih)
                if p in self.walls:
                    if self.highlited_wall is not None and p == self.highlited_wall:
                        print(Back.RED + Fore.RED + '#', end='')
                    else:
                        print(Fore.RED + '#', end='')
                elif p in self.boxes:
                    if p in self.stack:
                        print(Fore.BLUE + '[]', end='')
                    else:
                        print(Fore.GREEN + '[]', end='')
                    iw += 1
                elif self.robot == p:
                    print(Back.WHITE + Fore.BLACK + ' ', end='')
                else:
                    print('.', end='')
                iw += 1
            print('')
        print('')

def silver(in_txt):
    day = Day15(in_txt)
    day.print_map()
    day.run(True)
    day.print_map()
    print(f'Distances: {day.calc_distances()}')

def golden(in_txt):
    day = Day15Golden(in_txt)
    day.print_map()
    day.run(True)
    day.print_map()
    print(f'Distances: {day.calc_distances()}')

if __name__ == "__main__":
    init(autoreset=True)
    debug = False
    # debug = True
    in_txt = get_input(debug)
    # print('Silver:')
    # silver(in_txt)
    # print('')
    print('Golden:')
    golden(in_txt)
    print('')
