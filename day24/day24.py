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

class Device:
    def __init__(self, a, op, b, c):
        self.a = a
        self.op = op
        self.b = b
        self.c = c

    def calc(self, a_value, b_value):
        if self.op == 'AND':
            return a_value & b_value
        elif self.op == 'OR':
            return a_value | b_value
        elif self.op == 'XOR':
            return a_value ^ b_value
        else:
            raise ValueError(f'Unknown operation: {self.op}')

    def __repr__(self):
        return f'{self.a} {self.op} {self.b} -> {self.c}'

    def __str__(self):
        return f'{self.a} {self.op} {self.b} -> {self.c}'

    def __eq__(self, other):
        return self.a == other.a and self.op == other.op and self.b == other.b and self.c == other.c

    def __hash__(self):
        return hash((self.a, self.op, self.b, self.c))



class Day24:
    def __init__(self, in_txt):
        self.values = {}
        self.devices_inp = []
        self.devices_tmp = []
        self.parse_input(in_txt)

    def parse_input(self, in_txt):
        self.connections = []
        wires = re.findall(r"([a-z0-9]{3}): (\d)", in_txt)
        for a, b in wires:
            self.values[a] = int(b)

        devices = re.findall(r"([a-z0-9]{3}) (AND|OR|XOR) ([a-z0-9]{3}) -> ([a-z0-9]{3})", in_txt)
        for a, op, b, c in devices:
            self.devices_inp.append(Device(a, op, b, c))
            self.devices_tmp.append(Device(a, op, b, c))

    def step(self):
        for i_device in reversed(range(len(self.devices_tmp))):
            device = self.devices_tmp[i_device]
            a = self.values.get(device.a, None)
            b = self.values.get(device.b, None)
            if a is not None and b is not None:
                self.values[device.c] = device.calc(a, b)
                self.devices_tmp.pop(i_device)

    def run(self):
        while self.devices_tmp:
            self.step()
        print(self.values)


def silver(in_txt, is_debug):
    day = Day24(in_txt)
    day.run()
    z_arr = {}
    for k, v in day.values.items():
        if k.startswith('z'):
            z_arr[k] = v

    z_sorted = sorted(z_arr)
    n = 1
    v = 0
    for i in range(len(z_sorted)):
        if z_arr[z_sorted[i]] != 0:
            v += n
        n *= 2
    print(v)

def golden(in_txt, is_debug):
    day = Day24(in_txt)

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
