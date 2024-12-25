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


class Day25:
    def __init__(self, in_txt):
        self.keys = []
        self.keys_calc = []
        self.locks = []
        self.locks_calc = []
        self.in_txt = in_txt
        self.parse_input(in_txt)

    def parse_input(self, in_txt):
        self.keys = []
        self.locks = []

        self.locks = re.findall(r'#####\n(?:[.#]{5}\n?){6}', in_txt)
        self.keys = re.findall(r'(?:[.#]{5}\n){6}#####\n?', in_txt)

    def silver(self):
        fit_numbers = 0
        for lock in self.locks:
            key_mask = lock.replace('#', '*').replace('.', '[#.]').replace('*', '\.')
            fit_numbers += len(re.findall(key_mask, self.in_txt))
            #
            # for key in self.keys:
            #     if re.match(key_mask, key):
            #         fit_numbers += 1
        print(f'Fit numbers: {fit_numbers}')


def silver(in_txt, is_debug):
    day = Day25(in_txt)
    day.silver()



def golden(in_txt, is_debug):
    day = Day25(in_txt)


if __name__ == "__main__":
    debug = False
    # debug = True
    in_txt = get_input(debug)
    print('Silver:')
    silver(in_txt, debug)
    print('')
    # print('Golden:')
    # golden(in_txt, debug)
    # print('')
