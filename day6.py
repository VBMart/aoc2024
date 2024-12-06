import re
import math
import functools


in_txt = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


lines = re.findall(r"([^\n]+)\n?", in_txt)

class Step:
    r: int
    c: int
    d: str

    def __init__(self, r, c, d):
        self.r = r
        self.c = c
        self.d = d

    def __repr__(self):
        return f'Step: {self.r}x{self.c} {self.d}'


class Guard:
    r: int
    c: int
    d: str
    world_map: dict
    places: dict
    map_w: int
    map_h: int
    leave: bool
    loop: bool
    history: dict

    def __init__(self, r, c, d):
        self.r = r
        self.c = c
        self.d = d
        self.world_map = []
        self.places = []
        self.history = []
        self.loop = False
        self.leave = False

    def __repr__(self):
        return f'Guard: {self.r}x{self.c} {self.d} leave: {self.leave}, cnt: {self.get_places_count()}'

    def print_arr(self, arr):
        for ih in range(0, self.map_h):
            s = ""
            for iw in range(0, self.map_w):
                s += arr[ih][iw]
            print(s)
        print('')

    def print_map(self):
        self.print_arr(self.world_map)

    def print_places(self):
        self.print_arr(self.places)

    def make_step(self):
        if self.leave:
            return
        if self.loop:
            return
        
        if self.d == '^':
            if self.r == 0:
                self.leave = True
                return
            if self.world_map[self.r-1][self.c] != '#':
                self.r -= 1
                self.places[self.r][self.c] = 'X'
            else:
                self.d = '>'
        elif self.d == '>':
            if self.c == self.map_w-1:
                self.leave = True
                return
            if self.world_map[self.r][self.c+1] != '#':
                self.c += 1
                self.places[self.r][self.c] = 'X'
            else:
                self.d = 'V'
        elif self.d == 'V':
            if self.r == self.map_h-1:
                self.leave = True
                return
            if self.world_map[self.r+1][self.c] != '#':
                self.r += 1
                self.places[self.r][self.c] = 'X'
            else:
                self.d = '<'
        elif self.d == '<':
            if self.c == 0:
                self.leave = True
                return
            if self.world_map[self.r][self.c-1] != '#':
                self.c -= 1
                self.places[self.r][self.c] = 'X'
            else:
                self.d = '^'
                
        for step in self.history:
            if step.c == self.c and step.r == self.r and step.d == self.d:
                self.loop = True
                return
        self.history.append(Step(r=self.r, c=self.c, d=self.d))

    def test_loop(self):
        max_steps = 2 * self.map_w * self.map_h
    
    def get_places_count(self):
        cnt = 0
        for ih in range(0, self.map_h):
            for iw in range(0, self.map_w):
                if self.places[ih][iw] == 'X':
                    cnt += 1
        return cnt

guard = Guard(r=0, c=0, d="^")

def parse_map():
    global guard
    guard = Guard(r=0, c=0, d="^")
    guard.map_h = len(lines)
    guard.map_w = len(lines[0])
    for ih in range(0, guard.map_h):
        m_l = []
        g_l = []
        for iw in range(0, guard.map_w):
            cell = lines[ih][iw]
            m_l.append(cell)
            if cell == "^":
                guard.r = ih
                guard.c = iw
                g_l.append('X')
            else:
                g_l.append('.')
        guard.world_map.append(m_l)
        guard.places.append(g_l)

def silver():
  for i in range(0, 100000):
    guard.make_step()
    if guard.leave:
        break
  print(guard)
  print(guard.history)
  guard.print_places()

def golden():
  parse_map()
  map_w = guard.map_w
  map_h = guard.map_h
  loop_cnt = 0
  print(f'{map_w}x{map_h}')
  for ih in range(0, map_h):
      for iw in range(0, map_w):
          parse_map()
          if guard.world_map[ih][iw] == '#' or guard.world_map[ih][iw] == '^':
              continue
          else:
              guard.world_map[ih][iw] = '#'
          for i in range(0, 100000):
              guard.make_step()
              if guard.leave:
                  break
              if guard.loop:
                  loop_cnt += 1
                  break
  print(loop_cnt)

if __name__ == "__main__":
  silver()
  golden()
