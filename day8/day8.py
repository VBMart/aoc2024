import re
from itertools import product
import time

def print_arr(arr):
    for row in arr:
        if type(row) == list:
            print(''.join(row))
        else:
            print(row)
    print('')

class Day8:
    map_height = 0
    map_width = 0
    map = []
    antinodes = []
    lines = []
    antennas = {}
    is_golden = False

    def __init__(self, in_txt, is_golden=False):
        lines = re.findall(r"([^\n]+)\n?", in_txt)
        self.is_golden = is_golden
        self.parse_map(lines)

    def parse_map(self, lines):
        self.antennas = {}
        self.map = lines
        self.antinodes = []
        self.map_width = len(lines[0])
        self.map_height = len(lines)
        for i_row in range(self.map_height):
            self.antinodes.append(list('.' * self.map_width))
            for i_col in range(self.map_width):
                ant = lines[i_row][i_col]
                if ant != '.':
                    if ant not in self.antennas:
                        self.antennas[ant] = []
                    self.antennas[ant].append((i_row, i_col))

    def set_antinodes(self, row, col, delta_row, delta_col):
        if not self.is_golden:
            r = row - delta_row
            c = col - delta_col
            if 0 <= r < self.map_height and 0 <= c < self.map_width:
                self.antinodes[r][c] = 'X'
        else:
            points = []
            r = row
            c = col
            dr = delta_row
            dc = delta_col
            while 0 <= r < self.map_height and 0 <= c < self.map_width:
                points.append((r, c))
                r -= dr
                c -= dc
            for point in points:
                r = point[0]
                c = point[1]
                if 0 <= r < self.map_height and 0 <= c < self.map_width:
                    self.antinodes[r][c] = 'X'

    def get_antinodes_number(self):
        return sum([row.count('X') for row in self.antinodes])

    def process_antennas(self):
        for ant in self.antennas:
            elem_number = len(self.antennas[ant])
            for i in range(elem_number):
                for j in range(i + 1, elem_number):
                    ant1 = self.antennas[ant][i]
                    ant2 = self.antennas[ant][j]
                    delta_col = ant2[1] - ant1[1]
                    delta_row = ant2[0] - ant1[0]
                    # print(f'Antenna {ant} at {ant1} and {ant2} has delta {delta_row}, {delta_col}')
                    self.set_antinodes(ant1[0], ant1[1], delta_row, delta_col)
                    self.set_antinodes(ant2[0], ant2[1], -delta_row, -delta_col)


def get_input(debug: bool = False):
    file_name = 'input.txt'
    if debug:
        file_name = 'example.txt'
    with open(file_name, 'r') as f:
        return f.read()


def silver(in_txt):
    day8 = Day8(in_txt)
    # print_arr(day8.map)
    # print(day8.antennas)
    day8.process_antennas()
    # print_arr(day8.antinodes)
    print(day8.get_antinodes_number())


def golden(in_txt):
    day8 = Day8(in_txt, is_golden=True)
    print_arr(day8.map)
    print(day8.antennas)
    day8.process_antennas()
    print_arr(day8.antinodes)
    print(day8.get_antinodes_number())


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
