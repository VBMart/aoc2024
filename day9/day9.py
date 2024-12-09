import re
from itertools import product
import time

def get_input(debug: bool = False):
    file_name = 'input.txt'
    if debug:
        file_name = 'example.txt'
    with open(file_name, 'r') as f:
        return f.read()

class Day9:
    is_golden = False
    input_hdd = ''
    hdd = []
    last_file = 0

    def __init__(self, in_txt, is_golden=False):
        self.is_golden = is_golden
        self.last_file = 0
        self.hdd = []
        self.input_hdd = in_txt

    def prepare_empty_spaces(self):
        i_file = 0
        for i in range(len(self.input_hdd)):
            ch = self.input_hdd[i]
            v = int(ch)
            if i % 2 == 0:
                for iv in range(v):
                    self.hdd.append(f'{i_file}')
                self.last_file = i_file
                i_file += 1
            else:
                for iv in range(v):
                    self.hdd.append('.')
                    
    def defragment_drive(self):
        i_empty = 0
        i_file = len(self.hdd)
        while i_empty < i_file:
            for i in range(len(self.hdd)):
                if self.hdd[i] == '.':
                    i_empty = i
                    break
            for i in reversed(range(len(self.hdd))):
                if self.hdd[i] != '.':
                    i_file = i
                    break
            if i_empty >= i_file:
                break
            # print(f'{i_empty} ({self.hdd[i_empty]}) {i_file} ({self.hdd[i_file]})')
            self.hdd[i_empty] = self.hdd[i_file]
            self.hdd[i_file] = '.'
            # print(f'{''.join(self.hdd)}')

    def defragment_drive_files(self):
        for i_file in reversed(range(self.last_file+1)):
            file_end_pos = 0
            file_start_pos = 0
            is_file_found = False
            for i in reversed(range(len(self.hdd))):
                if self.hdd[i] == str(i_file):
                    if not is_file_found:
                        is_file_found = True
                        file_end_pos = i
                else:
                    if is_file_found:
                        file_start_pos = i+1
                        break

            file_length = file_end_pos - file_start_pos + 1
            # print(f'File {i_file} found at {file_start_pos} - {file_end_pos} with length {file_length}')
            space_start_pos = 0
            space_end_pos = file_start_pos-1
            space_length = space_end_pos - space_start_pos + 1
            is_space_found = False
            for i in range(file_start_pos+1):
                if self.hdd[i] == '.':
                    if not is_space_found:
                        is_space_found = True
                        space_start_pos = i
                else:
                    if is_space_found:
                        space_end_pos = i-1
                        space_length = space_end_pos - space_start_pos + 1
                        if space_length < file_length:
                            # print(f'Space {space_start_pos} - {space_end_pos} is too small')
                            is_space_found = False
                        else:
                            break

            if is_space_found:
                # print(f'File {i_file} will be moved to {space_start_pos} - {space_end_pos}')
                for i in range(file_length):
                    self.hdd[space_start_pos+i] = str(i_file)
                    self.hdd[file_start_pos+i] = '.'
                # print(''.join(self.hdd))
            else:
                # print(f'File {i_file} will not be moved')
                pass


    def get_checksum(self):
        sum = 0
        for i in range(len(self.hdd)):
            if self.hdd[i] != '.':
                sum += i*int(self.hdd[i])
        return sum



def silver(in_txt):
    day9 = Day9(in_txt)
    # print(day9.input_hdd)
    day9.prepare_empty_spaces()
    print('Disk prepared')
    # print(''.join(day9.hdd))
    day9.defragment_drive()
    print('Disk defragmented')
    # print(''.join(day9.hdd))
    print(day9.get_checksum())


def golden(in_txt):
    day9 = Day9(in_txt, is_golden=True)
    day9.prepare_empty_spaces()
    print('Disk prepared')
    # print(''.join(day9.hdd))
    print(f'Max file: {day9.last_file}')
    day9.defragment_drive_files()
    print('Disk defragmented')
    # print(''.join(day9.hdd))
    print(day9.get_checksum())


if __name__ == "__main__":
    # in_txt = get_input(debug=True)
    in_txt = get_input(debug=False)
    # print('Silver:')
    # silver(in_txt)
    print('')
    t1 = time.time()
    print('Golden:')
    golden(in_txt)
    print('Time spent: ', time.time() - t1)
    print('')
