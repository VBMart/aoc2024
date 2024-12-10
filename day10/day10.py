import re
from itertools import product
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
            print(''.join([str(x) for x in row]))
        else:
            print(row)
    print('')

deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]

class Day10:
    is_golden = False
    map_height = 0
    map_width = 0
    map = []
    start_positions = []
    end_positions = []
    routes = []

    def __init__(self, in_txt, is_golden=False):
        self.is_golden = is_golden
        lines = re.findall(r"([^\n]+)\n?", in_txt)
        self.parse_map(lines)
        self.find_all_starts()
        self.find_all_ends()

    def parse_map(self, lines):
        self.map_width = len(lines[0])
        self.map_height = len(lines)
        self.map = []
        for i_row in range(self.map_height):
            tmp = []
            for i_col in range(self.map_width):
                tmp.append(int(lines[i_row][i_col]))
            self.map.append(tmp)

    def find_all_starts(self):
        self.start_positions = []
        for i_row in range(self.map_height):
            for i_col in range(self.map_width):
                if self.map[i_row][i_col] == 0:
                    self.start_positions.append((i_row, i_col))

    def find_all_ends(self):
        self.end_positions = []
        for i_row in range(self.map_height):
            for i_col in range(self.map_width):
                if self.map[i_row][i_col] == 9:
                    self.end_positions.append((i_row, i_col))

    def find_routes(self, i_row, i_col, path, current_step):
        if current_step == 9:
            self.routes.append(path)
        for delta in deltas:
            new_row = i_row + delta[0]
            new_col = i_col + delta[1]
            if 0 <= new_row < self.map_height and 0 <= new_col < self.map_width:
                if self.map[new_row][new_col] == (current_step + 1):
                    new_path = path.copy()
                    new_path.append((new_row, new_col))
                    self.find_routes(new_row, new_col, new_path, current_step + 1)
        return None

    def find_ways_to_nines(self):
        sum_ends = 0
        sum_routes = 0
        for start in self.start_positions:
            self.routes = []
            self.find_routes(start[0], start[1], [start], 0)
            ends = set([r[-1] for r in self.routes])
            sum_ends += len(ends)
            sum_routes += len(self.routes)
        return sum_ends, sum_routes


def silver(in_txt):
    day10 = Day10(in_txt)
    print(day10.find_ways_to_nines()[0])

def golden(in_txt):
    day10 = Day10(in_txt)
    day10.find_all_starts()
    print(day10.find_ways_to_nines()[1])


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
