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

colors = {
    'r': Back.RED,
    'g': Back.GREEN,
    'b': Back.BLACK,
    'u': Back.BLUE,
    'w': Back.WHITE,
}

class Day19:

    def __init__(self, in_txt):
        self.patterns = set()
        self.designs = []
        self.parse_input(in_txt)

    def parse_input(self, in_txt):
        self.patterns = set()
        self.designs = []

        lines = in_txt.split('\n')

        patterns_line = lines[0]
        patterns = re.findall(r"([rgbuw]+)", patterns_line)
        for pattern in patterns:
            self.patterns.add(pattern)

        self.designs = []
        for i in range(2, len(lines)):
            line = lines[i]
            self.designs.append(line)

        self.clean_up_patterns()

    def clean_up_patterns(self):
        print(f'Patterns in input: {len(self.patterns)}')
        new_patterns = set()
        for pattern in self.patterns:
            is_useful = False
            for design in self.designs:
                if design.find(pattern) != -1:
                    is_useful = True
                    break
            if is_useful:
                new_patterns.add(pattern)
            else:
                print(f'{pattern} is not useful')
        self.patterns = new_patterns
        print(f'Filtered patterns: {len(self.patterns)}')

    def print_pattern(self, pattern):
        for letter in pattern:
            print(colors[letter] + letter, end='')
        print(Back.RESET + Fore.RESET + '')

    def make_design(self, design, current):
        for pattern in self.patterns:
            new_current = current + pattern
            # print(f'{design}: {current} + {pattern} = {new_current} -> {design.startswith(new_current)}')
            if design.startswith(new_current):
                if design == new_current:
                    return True
                res = self.make_design(design, new_current)
                if res:
                    return True

        return False

    def can_combine_design(self, design):
        return self.make_design(design, '')

    def check_designs(self):
        cnt = 0
        for design in self.designs:
            if self.can_combine_design(design):
                cnt += 1
                print(f'{design} YES')
            else:
                print(f'{design} NO')
        return cnt


class Day19Golden(Day19):

    def __init__(self, in_txt):
        super().__init__(in_txt)
        self.design_variants = {}

    def combine_variants(self, design):
        pass

def silver(in_txt, is_debug):
    day = Day19(in_txt)
    # for pattern in day.patterns:
    #     day.print_pattern(pattern)
    # print(day.can_combine_design('bwurrg'))

    print(f'Silver: {day.check_designs()}')

def golden(in_txt):
    day = Day19(in_txt)
    print(day.patterns)


if __name__ == "__main__":
    # debug = False
    debug = True
    in_txt = get_input(debug)
    print('Silver:')
    silver(in_txt, debug)
    print('')
    # print('Golden:')
    # golden(in_txt)
    # print('')
