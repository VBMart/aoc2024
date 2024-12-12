import re
from itertools import product
import time

def get_input(debug: bool = False):
    file_name = 'input.txt'
    if debug:
        file_name = 'example_e.txt'
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

deltas = [(0, 1), (1, 0), (0, -1), (-1, 0)]
named_deltas = ['R', 'D', 'L', 'U']

class Region:
    reg_symbol = ''
    points = []
    boundary_points = []

    def __init__(self, reg_symbol):
        self.reg_symbol = reg_symbol
        self.points = []
        self.edges = []
        self.boundary_points = []
        self.visited_boundary = []

    def find_boundary(self):
        self.boundary_points = []
        self.visited_boundary = []
        for point in self.points:
            is_edge = False
            id = 0
            for d in deltas:
                new_row = point[0] + d[0]
                new_col = point[1] + d[1]
                if (new_row, new_col) not in self.points:
                    self.boundary_points.append((point[0], point[1], named_deltas[id]))
                id += 1

    def square(self):
        return len(self.points)

    def perimeter(self):
        perimeter = 0
        for point in self.points:
            for d in deltas:
                new_row = point[0] + d[0]
                new_col = point[1] + d[1]
                if (new_row, new_col) not in self.points:
                    perimeter += 1
        return perimeter

    def find_edges(self, row, col, direction, i_edge):
        self.visited_boundary.append((row, col, direction))
        self.edges[i_edge].append((row, col, direction))
        id = 0
        for d in deltas:
            new_row = row + d[0]
            new_col = col + d[1]
            if (new_row, new_col, direction) in self.visited_boundary:
                continue
            if (new_row, new_col, direction) in self.boundary_points:
                self.find_edges(new_row, new_col, direction, i_edge)
            id += 1

    def get_edges(self):
        if len(self.boundary_points) == 0:
            self.find_boundary()
        self.edges = []
        self.visited_boundary = []
        for i in range(len(self.boundary_points)):
            if self.boundary_points[i] in self.visited_boundary:
                continue
            self.edges.append([])
            self.find_edges(self.boundary_points[i][0], self.boundary_points[i][1], self.boundary_points[i][2], len(self.edges) - 1)
        return len(self.edges)

    def cost(self, is_golden=False):
        if is_golden:
            return self.square() * self.get_edges()
        else:
            return self.square() * self.perimeter()

class Day12:
    is_golden = False
    map = []
    visited = []
    regions = []
    map_height = 0
    map_width = 0

    def __init__(self, in_txt, is_golden=False):
        self.is_golden = is_golden
        lines = re.findall(r"([^\n]+)\n?", in_txt)
        self.map_height = len(lines)
        self.map_width = len(lines[0])
        self.map = []
        self.visited = []
        for i_row in range(self.map_height):
            tmp = []
            for i_col in range(self.map_width):
                tmp.append(lines[i_row][i_col])
            self.map.append(tmp)
            self.visited.append([False] * self.map_width)

    def find_region(self, row, col, reg_ind):
        self.visited[row][col] = True
        self.regions[reg_ind].points.append((row, col))
        reg_symbol = self.map[row][col]
        for d in deltas:
            new_row = row + d[0]
            new_col = col + d[1]
            if new_row < 0 or new_row >= self.map_height or new_col < 0 or new_col >= self.map_width:
                continue
            if self.visited[new_row][new_col]:
                continue
            if self.map[new_row][new_col] != reg_symbol:
                continue
            self.find_region(row + d[0], col + d[1], reg_ind)

    def find_regions(self):
        self.regions = []
        for i_row in range(self.map_height):
            for i_col in range(self.map_width):
                if not self.visited[i_row][i_col]:
                    region = Region(self.map[i_row][i_col])
                    self.regions.append(region)
                    self.find_region(i_row, i_col, len(self.regions) - 1)

def silver(in_txt):
    day = Day12(in_txt)
    print_arr(day.map)
    day.find_regions()

    cost = 0
    print('Regions:')
    for reg in day.regions:
        print(f'Region {reg.reg_symbol}: square {reg.square()}, perimeter {reg.perimeter()}, cost {reg.cost()}')
        print(reg.points)
        cost += reg.cost()
        print('')
    print('Cost: ', cost)

def golden(in_txt):
    day = Day12(in_txt, is_golden=True)
    print_arr(day.map)
    day.find_regions()

    cost = 0
    print('Regions:')
    for reg in day.regions:
        print(f'Region {reg.reg_symbol}: square {reg.square()}, edges {reg.get_edges()}, cost {reg.cost(True)}')
        print(reg.points)
        print(reg.boundary_points)
        print(reg.edges)
        cost += reg.cost(True)
        print('')
    print('Cost: ', cost)


if __name__ == "__main__":
    # in_txt = get_input(debug=True)
    in_txt = get_input(debug=False)
    # print('Silver:')
    # silver(in_txt)
    # print('')
    # t1 = time.time()
    print('Golden:')
    golden(in_txt)
    # print('Time spent: ', time.time() - t1)
    # print('')
