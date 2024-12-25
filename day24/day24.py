import array
import heapq
import math
import os
import re
from colorama import Fore, Back, Style, init
import time
import graphviz


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

    def get_min_max_z(self):
        z_min = 99
        z_max = 0
        for dev in self.devices_inp:
            if dev.c.startswith('z'):
                n = int(dev.c[1:])
                if n < z_min:
                    z_min = n
                if n > z_max:
                    z_max = n

        return z_min, z_max

    def get_device_by_c(self, c):
        for dev in self.devices_inp:
            if dev.c == c:
                return dev
        return None

    def draw(self):
        dot = graphviz.Digraph(comment='The Round Table')
        for device in self.devices_inp:
            if device.a.startswith('x') or device.a.startswith('y') or device.b.startswith('x') or device.b.startswith('y'):
                dot.node(device.a, shape='circle')

            shapes = ['circle', 'square', 'triangle', 'diamond', 'parallelogram', 'trapezium', 'invtrapezium', 'invhouse', 'house']
            shapes_op = {
                'AND': 'diamond',
                'OR': 'square',
                'XOR': 'triangle',
            }
            shape = shapes_op.get(device.op, 'house')
            if device.c.startswith('z'):
                dot.node(
                    device.c,
                    label=f'{device.c}\n{device.op}',
                    shape=shape,
                    style='filled',
                    color='lightgrey'
                )
            else:
                dot.node(device.c, label=f'{device.c}\n{device.op}', shape=shape)

        for device in self.devices_inp:
            dot.edge(device.a, device.c)
            dot.edge(device.b, device.c)
        dot.render('graph', format='png', cleanup=True)

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
    # day.draw()
    z_min, z_max = day.get_min_max_z()
    problem_nodes = set()

    for z in range(z_min, z_max + 1):
        ind_str = f'{z:02}'
        z_str = f'z{ind_str}'
        is_z_valid = True
        reason = ''

        dev_z = day.get_device_by_c(z_str)
        if z == 0:
            if dev_z.get_expression() != '(x00 XOR y00)':
                reason = '\tz=0'
                problem_nodes.add(z_str)
                is_z_valid = False
        elif z == 1:
            pass
        elif z == z_max:
            if dev_z.op != 'OR':
                reason = '\tz_max must be OR'
                problem_nodes.add(z_str)
                is_z_valid = False
        else:
            if dev_z.op != 'XOR':
                reason = '\tmust be XOR'
                problem_nodes.add(z_str)
                is_z_valid = False
            if is_z_valid:
                dev_p1 = day.get_device_by_c(dev_z.a)
                dev_p2 = day.get_device_by_c(dev_z.b)
                if dev_p1 is None:
                    reason = f'\tPrev not found ({dev_z.a})'
                    problem_nodes.add(z_str)
                    is_z_valid = False
                if dev_p2 is None:
                    reason = f'\tPrev not found ({dev_z.b})'
                    problem_nodes.add(z_str)
                    is_z_valid = False
                if is_z_valid:
                    dev_or = None
                    dev_xor = None
                    if dev_p1.op == 'OR':
                        dev_or = dev_p1
                    if dev_p1.op == 'XOR':
                        dev_xor = dev_p1
                    if dev_p2.op == 'OR':
                        dev_or = dev_p2
                    if dev_p2.op == 'XOR':
                        dev_xor = dev_p2
                    if dev_or is None:
                        if dev_p1.op != 'XOR':
                            reason = f'\tFirst must be OR ({dev_p1}) ({dev_p2})'
                            problem_nodes.add(dev_p1.c)
                        elif dev_p2.op != 'XOR':
                            reason = f'\tSecond must be OR ({dev_p1}) ({dev_p2})'
                            problem_nodes.add(dev_p2.c)
                        else:
                            if not (dev_p1.a.startswith('x') and dev_p1.b.startswith('y')):
                                reason = f'\tNo XOR(OR+XOR) ({dev_p1}), ({dev_p2}) XOR must be from x, y: ({dev_p1})'
                                problem_nodes.add(dev_p1.c)
                            else:
                                reason = f'\tNo XOR(OR+XOR) ({dev_p1}), ({dev_p2}) XOR must be from x, y: ({dev_p2})'
                                problem_nodes.add(dev_p2.c)
                        is_z_valid = False
                    if dev_xor is None:
                        if dev_p1.op != 'OR':
                            reason = f'\tFirst must be XOR ({dev_p1}) ({dev_p2})'
                            problem_nodes.add(dev_p1.c)
                        elif dev_p2.op != 'OR':
                            reason = f'\tSecond must be XOR ({dev_p1}) ({dev_p2})'
                            problem_nodes.add(dev_p2.c)
                        else:
                            reason = f'No XOR(OR+XOR) ({dev_p1}), ({dev_p2})'
                        is_z_valid = False
                    if is_z_valid:
                        if not (dev_xor.a.startswith('x') and dev_xor.b.startswith('y')):
                            reason = 'XOR must be x XOR y'
                            is_z_valid = False
                        dev_or_p1 = day.get_device_by_c(dev_or.a)
                        dev_or_p2 = day.get_device_by_c(dev_or.b)
                        if dev_or_p1 is None:
                            reason = f'Prev not found ({dev_or.a})'
                            is_z_valid = False
                        if dev_or_p2 is None:
                            reason = f'Prev not found ({dev_or.b})'
                            is_z_valid = False
                        if is_z_valid:
                            if dev_or_p1.op != 'AND':
                                reason = f'\tmust be AND ({dev_or_p1}) [{dev_or}]'
                                problem_nodes.add(dev_or_p1.c)
                                is_z_valid = False
                            if dev_or_p2.op != 'AND':
                                reason = f'\tmust be AND ({dev_or_p2}) [{dev_or}]'
                                problem_nodes.add(dev_or_p2.c)
                                is_z_valid = False


        if not is_z_valid:
            print(f'{reason}: {dev_z}')

    problems = ','.join(sorted(problem_nodes))
    print(problems)

    return

    for z in range(z_min, z_max + 1):
    # for z in range(z_min, 5):
        ind_str = f'{z:02}'
        z_str = f'z{ind_str}'
        is_z_valid = True
        z_must_contain = set()
        if z == 0:
            z_must_contain.add('x00 XOR y00')
        else:
            z_must_contain.add(f'x{ind_str} XOR y{ind_str}')
        for zmc in z_must_contain:
            if day.formulas[z_str].find(zmc) == -1:
                is_z_valid = False

        for dev in day.devices_inp:
            if dev.c == z_str:
                if z != z_max:
                    if dev.op != 'XOR':
                        is_z_valid = False
                else:
                    if dev.op != 'OR':
                        is_z_valid = False

        if not is_z_valid:
            for dev in day.devices_inp:
                if dev.c == z_str:
                    print(dev)
            print(f'{z_str} = {day.formulas[z_str]}')
            print('')
        # print(f'{z_str} = {day.formulas[z_str]}')
        # print('')

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
