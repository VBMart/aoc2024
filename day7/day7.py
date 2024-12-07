import re
from itertools import product
import time


def get_input(debug: bool = False):
    file_name = 'input.txt'
    if debug:
        file_name = 'example.txt'
    with open(file_name, 'r') as f:
        return f.read()


def split_line(line):
    tmp = line.split(': ')
    tmp2 = tmp[1].split(' ')
    return int(tmp[0]), [int(x) for x in tmp2]


def check(num, items, operations):
    if len(items) == 1:
        return items[0] == num
    operation_combinations = product(operations, repeat=len(items) - 1)
    results = []
    for ops in operation_combinations:
        # Create an expression by interleaving items and operations
        # expression = ''.join(str(item) + op for item, op in zip(items, ops)) + str(items[-1])
        sum = items[0]
        i = 1
        for op in ops:
            if op == '+':
                sum += items[i]
            elif op == '*':
                sum *= items[i]
            elif op == '||':
                sum = int(f'{sum}{items[i]}')
            i += 1
        if sum == num:
            # print(expression, sum)
            return True
    return False

def silver(in_txt):
    lines = re.findall(r"([^\n]+)\n?", in_txt)
    sum = 0
    for line in lines:
        num, items = split_line(line)
        if check(num, items, ['+', '*']):
            sum += num
    print(sum)


def golden(in_txt):
    lines = re.findall(r"([^\n]+)\n?", in_txt)
    sum = 0
    i = 0
    for line in lines:
        if i % 100 == 0:
            print(i)
        num, items = split_line(line)
        if check(num, items, ['+', '*', '||']):
            sum += num
        i += 1
    print(sum)


if __name__ == "__main__":
    # in_txt = get_input(debug=True)
    in_txt = get_input(debug=False)
    print('Silver:')
    silver(in_txt)
    print('')
    t1 = time.time()
    print('Golden:')
    golden(in_txt)
    print('Time spent: ', time.time() - t1)
    print('')
    # golden_thr(in_txt)
