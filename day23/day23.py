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


class Connection:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return f'{self.a} <-> {self.b}'

    def __str__(self):
        return f'{self.a} <-> {self.b}'

    def __eq__(self, other):
        return (self.a == other.a and self.b == other.b) or (self.a == other.b and self.b == other.a)

    def __hash__(self):
        return hash(self.__str__())

    def is_connected(self, other):
        if self == other:
            return False
        return self.a == other.a or self.a == other.b or self.b == other.a or self.b == other.b


class Day23:
    def __init__(self, in_txt):
        self.connections = []
        self.parse_input(in_txt)

    def parse_input(self, in_txt):
        self.connections = []
        inputs = re.findall(r"([a-z]{2})-([a-z]{2})", in_txt)
        for inp in inputs:
            self.connections.append(Connection(inp[0], inp[1]))

    def make3(self):
        connections3 = []
        str_connections = []
        for c1 in self.connections:
            next2_connections = [x for x in self.connections if c1.is_connected(x)]
            for c2 in next2_connections:
                next3_connections = [x for x in self.connections if c2.is_connected(x)]
                for c3 in next3_connections:
                    if c1.is_connected(c3):
                        connections3.append([c1, c2, c3])
                        tmp = set()
                        is_starts_from_t = False
                        for c in [c1, c2, c3]:
                            tmp.add(c.a)
                            tmp.add(c.b)
                            if c.a.startswith('t') or c.b.startswith('t'):
                                is_starts_from_t = True
                        if is_starts_from_t:
                            if len(tmp) == 3:
                                s_tmp = ','.join(sorted(list(tmp)))
                                if s_tmp not in str_connections:

                                    str_connections.append(s_tmp)

        # for c in str_connections:
        #     print(c)
        return len(str_connections)

def silver(in_txt, is_debug):
    day = Day23(in_txt)
    cnt = day.make3()
    print(f'Answer: {cnt}')


def golden(in_txt, is_debug):
    day = Day23(in_txt)


if __name__ == "__main__":
    debug = False
    # debug = True
    in_txt = get_input(debug)
    print('Silver:')
    silver(in_txt, debug)
    # print('')
    # print('Golden:')
    # golden(in_txt, debug)
    # print('')
