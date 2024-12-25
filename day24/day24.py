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
        tmp = a
        if a > b:
            a = b
            b = tmp
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

    def get_expression(self):
        return f'({self.a} {self.op} {self.b})'



class Day24:
    def __init__(self, in_txt):
        self.values = {}
        self.devices_inp = []
        self.devices_tmp = []
        self.formulas = {}
        self.parse_input(in_txt)

    def parse_input(self, in_txt):
        self.connections = []
        wires = re.findall(r"([a-z0-9]{3}): (\d)", in_txt)
        for a, b in wires:
            self.values[a] = int(b)

        devices = re.findall(r"([a-z0-9]{3}) (AND|OR|XOR) ([a-z0-9]{3}) -> ([a-z0-9]{3})", in_txt)
        for a, op, b, c in devices:
            dev = Device(a, op, b, c)
            self.devices_inp.append(dev)
            self.devices_tmp.append(Device(a, op, b, c))
            self.formulas[c] = dev.get_expression()

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

    def resolve_step(self):
        cnt = 0
        for device in self.devices_inp:
            for k, v in self.formulas.items():
                if device.c == k:
                    continue
                if v.find(device.c) != -1:
                    cnt += 1
                    self.formulas[k] = v.replace(device.c, device.get_expression())

        return cnt

    def resolve(self):
        while self.resolve_step() > 0:
            pass

        z_min = 99
        z_max = 0
        for k, v in self.formulas.items():
            if k.startswith('z'):
                n = int(k[1:])
                if n < z_min:
                    z_min = n
                if n > z_max:
                    z_max = n

        for z in range(z_min, z_max + 1):
            z_str = f'z{z:02}'
            print(f'{z_str} = {self.formulas[z_str]}')
            print('')

        print('')
        return z_min, z_max

def silver(in_txt, is_debug):
    day = Day24(in_txt)
    day.run()

    z_arr = {}
    for k, v in day.formulas.items():
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
    z_min, z_max = day.resolve()

    z_arr = {}
    invalid_operands = set()
    z_with_invalid_operands = set()
    for k, v in day.formulas.items():
        if k.startswith('z'):
            z_arr[k] = v
            ops = re.findall(r"([a-z]{3})", v)
            for op in ops:
                invalid_operands.add(op)
                z_with_invalid_operands.add(k)

    z_sorted = sorted(z_with_invalid_operands)
    for z in z_sorted:
        print(f'{z} = {z_arr[z]}')
        print('')


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
