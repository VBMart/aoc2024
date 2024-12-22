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

class Generator:
    def __init__(self, initial):
        self.value = initial
        self.step = 0
        self.secret = initial
        self.secrets = []
        self.sequences = []
        self.deltas = []
        self.add_to_sequence(initial)
        self.deltas_cache = {}

    def mix(self, v1, v2):
        return v1 ^ v2

    def prune(self, value):
        return value % 16777216

    def add_to_sequence(self, value):
        self.secrets.append(value)
        value = value % 10
        self.sequences.append(value)
        if len(self.sequences) == 1:
            self.deltas.append(None)
        else:
            self.deltas.append(self.sequences[-1] - self.sequences[-2])

        if len(self.deltas) >= 5:
            deltas = self.deltas[-4:]
            deltas_s = ','.join([str(x) for x in deltas])
            if deltas_s not in self.deltas_cache:
                self.deltas_cache[deltas_s] = self.get_price(deltas)

    def next(self):
        self.step += 1

        secret = self.secret
        a = 64 * secret
        secret = self.mix(secret, a)
        secret = self.prune(secret)

        a = secret // 32
        secret = self.mix(secret, a)
        secret = self.prune(secret)

        a = 2048 * secret
        secret = self.mix(secret, a)
        secret = self.prune(secret)

        self.secret = secret
        self.add_to_sequence(secret)

        return secret

    def get_price(self, deltas):
        last_ind = None
        for i_self in reversed(range(len(self.deltas) - len(deltas) + 1)):
            s = 0
            for i in range(len(deltas)):
                if self.deltas[i_self + i] == deltas[i]:
                    s += 1
            if s == len(deltas):
                last_ind = i_self + len(deltas) - 1
                break

        if last_ind is None:
            return None

        return self.sequences[last_ind]

    def get_cached_price(self, deltas):
        deltas_s = ','.join([str(x) for x in deltas])
        if deltas_s in self.deltas_cache:
            return self.deltas_cache[deltas_s]
        return None

class Day22:
    def __init__(self, in_txt):
        self.init_secrets = []
        self.last_secrets = []
        self.gens = []
        self.parse_input(in_txt)

    def parse_input(self, in_txt):
        self.init_secrets = []
        self.last_secrets = []
        self.gens = []
        inputs = re.findall(r"(\d+)", in_txt)
        self.init_secrets = [int(x) for x in inputs]

    def run_gens(self, iters):
        for secret in self.init_secrets:
            gen = Generator(secret)
            for i in range(iters):
                gen.next()
            self.last_secrets.append(gen.secret)
            self.gens.append(gen)

    def solve_silver(self):
        self.run_gens(2000)
        sum = 0
        for secret in self.last_secrets:
            sum += secret
        return sum

    def calc_sum_by_deltas(self, deltas):
        sum = 0
        for gen in self.gens:
            v = gen.get_cached_price(deltas)
            if v is not None:
                sum += v
        return sum

    def solve_golden(self):
        self.run_gens(2000)

        max_deltas = self.gens[0].deltas[1:5]
        max_sum = self.calc_sum_by_deltas(max_deltas)
        cache = {}

        t1 = time.time()
        for ig in range(len(self.gens)):
            print(f'gen {ig} / {len(self.gens)}. Time: {time.time() - t1}')
            t1 = time.time()
            for id in range(1, len(self.gens[ig].deltas) - 4):
                deltas = self.gens[ig].deltas[id:id+4]
                deltas_s = ','.join([str(x) for x in deltas])
                if deltas_s not in cache:
                    sum = self.calc_sum_by_deltas(deltas)
                    cache[deltas_s] = sum
                    if sum > max_sum:
                        max_sum = sum
                        max_deltas = deltas

        return max_deltas, max_sum



def silver(in_txt, is_debug):
    day = Day22(in_txt)
    print(day.solve_silver())


def golden(in_txt, is_debug):
    day = Day22(in_txt)
    print(day.solve_golden())

if __name__ == "__main__":
    debug = False
    # debug = True
    in_txt = get_input(debug)
    print('Silver:')
    silver(in_txt, debug)
    print('')
    print('Golden:')
    golden(in_txt, debug)
    print('')
