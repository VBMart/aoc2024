import array
import heapq
import math
import os
import re
from enum import Enum, IntEnum

from colorama import Fore, Back, Style, init
import time


def get_input(debug: bool = False):
    file_name = 'input.txt'
    if debug:
        file_name = 'example1.txt'
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


class Instruction(IntEnum):
    adv = 0, 'adv'
    bxl = 1, 'bxl'
    bst = 2, 'bst'
    jnz = 3, 'jnz'
    bxc = 4, 'bxc'
    out = 5, 'out'
    bdv = 6, 'bdv'
    cdv = 7, 'cdv'

    def __new__(cls, number, name_str):
        obj = int.__new__(cls, number)
        obj._value_ = number
        obj.name_str = name_str
        return obj

    def __repr__(self):
        return f'Instruction({self.value}, {self.name_str})'

    def __str__(self):
        return self.name_str

    @classmethod
    def get_by_number(cls, value):
        for item in cls:
            if item.value == value:
                return item
        return None

class Step:
    def __init__(self, instruction: Instruction, operand):
        self.instruction = instruction
        self.operand = operand

    def __repr__(self):
        return f'[{self.instruction.value},{self.operand}] {self.instruction}, {self.operand}'
        # return f'Step(instruction={self.instruction}, operand={self.operand})'

class Computer:
    def __init__(self, a, b, c, program):
        self.a_init = a
        self.b_init = b
        self.c_init = c
        self.a = a
        self.b = b
        self.c = c
        self.instruction_pointer = 0
        self.i_step = 0
        self.program = program
        self.str_program = ','.join([str(x) for x in self.program])
        self.output = []
        self.str_output = ''
        self.is_failed = False

    def reset(self):
        self.a = self.a_init
        self.b = self.b_init
        self.c = self.c_init
        self.instruction_pointer = 0
        self.i_step = 0
        self.output = []
        self.str_output = ''
        self.is_failed = False

    def __repr__(self):
        return f'Computer(a={self.a}, b={self.b}, c={self.c}) (a={bin(self.a)[2:]} b={bin(self.b % 8)[2:]} c={bin(self.c % 8)[2:]})'

    def combo_operand_value(self, operand):
        if operand <= 3:
            return operand
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        if operand == 7:
            raise Exception('Invalid operand value')

    def do(self, step: Step):
        do_not_move_pointer = False
        if step.instruction == Instruction.adv:
            self.a = self.a // (2 ** self.combo_operand_value(step.operand))
        elif step.instruction == Instruction.bxl:
            self.b = self.b ^ step.operand
        elif step.instruction == Instruction.bst:
            self.b = self.combo_operand_value(step.operand) % 8
        elif step.instruction == Instruction.jnz:
            if self.a == 0:
                pass
            else:
                self.instruction_pointer = step.operand
                do_not_move_pointer = True
        elif step.instruction == Instruction.bxc:
            self.b = self.b ^ self.c
        elif step.instruction == Instruction.out:
            # self.output.append(self.combo_operand_value(step.operand) % 8)
            if self.str_output != '':
                self.str_output += ',' + str(self.combo_operand_value(step.operand) % 8)
            else:
                self.str_output += str(self.combo_operand_value(step.operand) % 8)
            if not self.str_program.startswith(self.str_output):
                self.is_failed = True
        elif step.instruction == Instruction.bdv:
            self.b = self.a // (2 ** self.combo_operand_value(step.operand))
        elif step.instruction == Instruction.cdv:
            self.c = self.a // (2 ** self.combo_operand_value(step.operand))

        if not do_not_move_pointer:
            self.instruction_pointer += 2
        self.i_step += 1

    def do_str(self, step: Step):
        s = ''
        op = step.operand
        combo_op = ''
        if step.operand <= 3:
            combo_op = str(step.operand)
        elif step.operand == 4:
            combo_op = 'a'
        elif step.operand == 5:
            combo_op = 'b'
        elif step.operand == 6:
            combo_op = 'c'

        if step.instruction == Instruction.adv:
            s = f'a = a // (2 ** {combo_op})'
        elif step.instruction == Instruction.bxl:
            s = f'b = b ^ {op}'
        elif step.instruction == Instruction.bst:
            s = f'b = {combo_op} % 8'
        elif step.instruction == Instruction.jnz:
            if self.a == 0:
                s = 'nop'
            else:
                s = f'jmp to {op}'
        elif step.instruction == Instruction.bxc:
            s = 'b = b ^ c'
        elif step.instruction == Instruction.out:
            s = f'out({combo_op} % 8)'
        elif step.instruction == Instruction.bdv:
            s = f'b = a // (2 ** {combo_op})'
        elif step.instruction == Instruction.cdv:
            s = f'c = a // (2 ** {combo_op})'
        return s

    def run(self):
        while self.instruction_pointer < len(self.program)-1:
            instruction_number = self.program[self.instruction_pointer]
            operand = self.program[self.instruction_pointer+1]
            step = Step(Instruction.get_by_number(instruction_number), operand)
            # print(f'{self.i_step}: {step} -> {self.do_str(step)}')
            # s = f'{self}'
            self.do(step)
            # print(f'{s} -> {self}')
            # print('')
            # if self.is_failed:
            #     break
            if self.i_step >= 200:
                print('Too many steps')
                break
        # self.str_output = ','.join([str(x) for x in self.output])

class Day17:
    is_golden = False

    def __init__(self, in_txt, is_golden=False):
        self.computer = None
        self.program = []
        self.s_program = ''
        self.is_golden = is_golden
        self.parse_input(in_txt)

    def parse_input(self, in_txt):
        a = int(re.findall(r"Register A: (\d+)", in_txt)[0])
        b = int(re.findall(r"Register B: (\d+)", in_txt)[0])
        c = int(re.findall(r"Register C: (\d+)", in_txt)[0])

        self.s_program = re.findall(r"Program: (.+)", in_txt)[0]
        numbers = re.findall(r"(\d+)", self.s_program)
        program = [int(x) for x in numbers]

        self.computer = Computer(a, b, c, program)

    def run(self):
        self.computer.run()

def silver(in_txt):
    day = Day17(in_txt)
    print(day.computer)
    print('')
    day.run()
    print(day.computer.str_output)
    print(day.computer.i_step)

def make_num(num):
    res = []
    for b1 in range(8):
        b2 = b1 ^ 1
        pow_b2 = 2 ** b2
        for c in range(8):
            b3 = b2 ^ c
            b4 = b3 ^ 6
            a = c * (2 ** pow_b2) + b1
            if a % 8 != b1:
                continue
            if b4 == num:
                res.append((a, b1, c))
    return res


def golden(in_txt):
    day = Day17(in_txt, is_golden=True)

    for i in range(8):
        print(f'{i}:')
        arr = make_num(i)
        for a, b, c in arr:
            print(f'{a} = {bin(a)[2:]}')

    print(day.s_program)
    print(len(day.computer.program))
    a_len_bin = len(day.computer.program) * 3
    print(f'Bits in a: {a_len_bin}, Bytes: {a_len_bin // 8}')
    print(f'Max(a) = {2 ** a_len_bin - 1}')
    # for a in range(1, 1000):
    #     day.computer.reset()
    #     day.computer.a = a
    #     day.run()
    #     if len(day.computer.str_output) > 1:
    #         print(f'{a} = {bin(a)[2:]} -> {day.computer.str_output}')


    sa = '1000000010'
    a = int(sa, 2)
    print(f'{a} = {bin(a)[2:]}')
    day.computer.reset()
    day.computer.a = a
    day.run()
    print(f'{a} = {bin(a)[2:]} -> {day.computer.str_output}')

    return

    deltas = set()
    t1 = time.time()
    tmp = 100_000_000
    max_len = 0
    for i in range(tmp):
        if i % 10_000_000 == 0:
            print(f'Iteration {i} / {tmp}')
        day.computer.reset()
        day.computer.a = i
        day.run()
        if day.computer.str_program.startswith(day.computer.str_output[0]):
            if max_len < len(day.computer.str_output):
                max_len = len(day.computer.str_output)
                deltas = set()
            deltas.add(i)

    print(f'Time spent for deltas: {time.time() - t1}')
    print(f'Deltas: {len(deltas)}')

    t1 = time.time()
    t2 = time.time()
    a = 0
    is_number_found = False
    i_start = 1
    i_end = i_start + 100
    for i in range(i_start, i_end):
        if i % 1 == 0:
            print(f'Iteration {i} / {i_end} time: ({time.time() - t2})')
            t2 = time.time()
        for j in deltas:
            day.computer.reset()
            a = j + tmp * i
            day.computer.a = a
            day.run()
            if day.computer.str_output == day.computer.str_program:
                print(f'Init a: {a}')
                is_number_found = True
                break
        if is_number_found:
            break

    print(f'Last a: {a}')
    print(f'Time spent: {time.time() - t1}')

    # day.computer.a = 117440
    # day.computer.a = 55
    # print(day.computer)
    # print(','.join([str(x) for x in day.computer.program]))
    # print('')
    # day.run()
    # print(day.computer.str_output)
    # print(day.computer.i_step)

if __name__ == "__main__":
    debug = False
    # debug = True
    in_txt = get_input(debug)
    # print('Silver:')
    # silver(in_txt)
    print('')
    print('Golden:')
    golden(in_txt)
    print('')
