import tkinter as tk
import block as bk


class Window:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title('Chess')
        self.master.geometry('900x900')
        self.blocks = []
        self.labeling = []
        self.__rest_of_init()
        self.temp = 0

    def __rest_of_init(self):
        self.master.bind('<1>', self.some_function)
        for i in range(64):
            if i // 8 % 2 == 0:
                if i % 2 == 0:
                    self.blocks.append(bk.Block(self.master, 'white', i))
                else:
                    self.blocks.append(bk.Block(self.master, 'grey', i))
            else:
                if i % 2 == 0:
                    self.blocks.append(bk.Block(self.master, 'grey', i))
                else:
                    self.blocks.append(bk.Block(self.master, 'white', i))
        for i in range(8):
            self.labeling.append((tk.Label(self.master, text=chr(97 + i)), tk.Label(self.master, text=8 - i)))
            self.labeling[i][0].grid(row=8, column=i)
            self.labeling[i][1].grid(row=i, column=8)
        self.__setup()

    def some_function(self, event=None):
        if event:
            pass
        self.temp += 1
        if self.temp == 2:
            self.__make_move()
            self.temp = 0

    def run(self):
        self.master.mainloop()

    def __setup(self):
        for block in self.blocks:
            block.setup()

    def __make_move(self):
        times = []
        for block in self.blocks:
            if block.return_time():
                times.append(block)
        if len(times) == 2:
            if times[0].return_time() < times[1].return_time():
                if self.__move_checker(times[0], times[1]):
                    times[1].help_setup(times[0].temp)
                    times[0].empty_position()
                else:
                    print('Not a valid Move')
            else:
                if self.__move_checker(times[1], times[0]):
                    times[0].help_setup(times[1].temp)
                    times[1].empty_position()
                else:
                    print('Not a valid Move')
        else:
            print('2 positions not selected')
        for block in times:
            block.reset_time()

    def __move_checker(self, start, end):
        print('{} to {}'.format(start.position, end.position))
        piece_name = start.label[2]
        possible_positions = []
        start_index = 0
        is_king = 'king' in piece_name
        for i in range(len(self.blocks)):
            if start == self.blocks[i]:
                start_index = i
                break
        if ('rook' in piece_name) or is_king:
            if 'h' not in start.position:  # rightwards
                for k in range(start_index + 1, (start_index // 8 + 1) * 8):
                    if self.blocks[k].label[1] == 'empty':
                        possible_positions.append(self.blocks[k].position)
                        if is_king:
                            break
                    elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                            self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                        possible_positions.append(self.blocks[k].position)
                        break
                    else:
                        break
            if 'a' not in start.position:  # leftwards
                for k in range(start_index - 1, 8 * (start_index // 8) - 1, -1):
                    if self.blocks[k].label[1] == 'empty':
                        possible_positions.append(self.blocks[k].position)
                        if is_king:
                            break
                    elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                            self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                        possible_positions.append(self.blocks[k].position)
                        break
                    else:
                        break
            if '8' not in start.position:  # upwards
                for k in range(start_index - 8, -1, -8):
                    if self.blocks[k].label[1] == 'empty':
                        possible_positions.append(self.blocks[k].position)
                        if is_king:
                            break
                    elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                            self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                        possible_positions.append(self.blocks[k].position)
                        break
                    else:
                        break
            if '1' not in start.position:  # downwards
                for k in range(start_index + 8, 64, 8):
                    if self.blocks[k].label[1] == 'empty':
                        possible_positions.append(self.blocks[k].position)
                        if is_king:
                            break
                    elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                            self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                        possible_positions.append(self.blocks[k].position)
                        break
                    else:
                        break
        if ('bishop' in piece_name) or is_king:
            if 'h' not in start.position:
                if '8' not in start.position:  # top rightwards
                    for k in range(start_index - 7, -1, -7):
                        if self.blocks[k].label[1] == 'empty':
                            possible_positions.append(self.blocks[k].position)
                            if is_king:
                                break
                        elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                            possible_positions.append(self.blocks[k].position)
                            break
                        else:
                            break
                        if 'h' in self.blocks[k].position:
                            break
                if '1' not in start.position:  # bottom rightwards
                    for k in range(start_index + 9, 64, 9):
                        if self.blocks[k].label[1] == 'empty':
                            possible_positions.append(self.blocks[k].position)
                            if is_king:
                                break
                        elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                            possible_positions.append(self.blocks[k].position)
                            break
                        else:
                            break
                        if 'h' in self.blocks[k].position:
                            break
            if 'a' not in start.position:
                if '8' not in start.position:  # top leftwards
                    for k in range(start_index - 9, -1, -9):
                        if self.blocks[k].label[1] == 'empty':
                            possible_positions.append(self.blocks[k].position)
                            if is_king:
                                break
                        elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                            possible_positions.append(self.blocks[k].position)
                            break
                        else:
                            break
                        if 'a' in self.blocks[k].position:
                            break
                if '1' not in start.position:  # bottom leftwards
                    for k in range(start_index + 7, 64, 7):
                        if self.blocks[k].label[1] == 'empty':
                            possible_positions.append(self.blocks[k].position)
                            if is_king:
                                break
                        elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                            possible_positions.append(self.blocks[k].position)
                            break
                        else:
                            break
                        if 'a' in self.blocks[k].position:
                            break
        elif piece_name == 'knight':
            if int(start.position[1]) < 7:  # going up
                if 'a' not in start.position:
                    possible_positions.append(
                        '{}{}'.format(chr(ord(start.position[0]) - 1), str(int(start.position[1]) + 2)))
                if 'h' not in start.position:
                    possible_positions.append(
                        '{}{}'.format(chr(ord(start.position[0]) + 1), str(int(start.position[1]) + 2)))
            if int(start.position[1]) > 2:  # going down
                if 'a' not in start.position:
                    possible_positions.append(
                        '{}{}'.format(chr(ord(start.position[0]) - 1), str(int(start.position[1]) - 2)))
                if 'h' not in start.position:
                    possible_positions.append(
                        '{}{}'.format(chr(ord(start.position[0]) + 1), str(int(start.position[1]) - 2)))
            if ord(start.position[0]) < 103:  # going right
                if '8' not in start.position:
                    possible_positions.append(
                        '{}{}'.format(chr(ord(start.position[0]) + 2), str(int(start.position[1]) + 1)))
                if '1' not in start.position:
                    possible_positions.append(
                        '{}{}'.format(chr(ord(start.position[0]) + 2), str(int(start.position[1]) - 1)))
            if ord(start.position[0]) > 98:  # going left
                if '8' not in start.position:
                    possible_positions.append(
                        '{}{}'.format(chr(ord(start.position[0]) - 2), str(int(start.position[1]) + 1)))
                if '1' not in start.position:
                    possible_positions.append(
                        '{}{}'.format(chr(ord(start.position[0]) - 2), str(int(start.position[1]) - 1)))
            for block in self.blocks:
                if block.position in possible_positions and block.label[1] == start.label[1]:
                    possible_positions.remove(block.position)
        elif piece_name == 'pawn':
            if start.label[1] == 'black':
                if '7' in start.position:
                    temp = 17
                else:
                    temp = 9
                for k in range(start_index + 8, start_index + temp, 8):
                    if self.blocks[k].label[1] == 'empty':
                        possible_positions.append(self.blocks[k].position)
                    else:
                        break
                if 'a' not in start.position:  # kills on cross
                    for block in self.blocks:
                        if (block.position == '{}{}'.format(chr(ord(start.position[0]) - 1),
                                                            str(int(start.position[1]) - 1))) and (
                                block.label[1] == 'white'):
                            possible_positions.append(block.position)
                if 'h' not in start.position:  # kills on cross
                    for block in self.blocks:
                        if (block.position == '{}{}'.format(chr(ord(start.position[0]) + 1),
                                                            str(int(start.position[1]) - 1))) and (
                                block.label[1] == 'white'):
                            possible_positions.append(block.position)
            else:
                if '2' in start.position:
                    temp = 17
                else:
                    temp = 9
                for k in range(start_index - 8, start_index - temp, -8):
                    if self.blocks[k].label[1] == 'empty':
                        possible_positions.append(self.blocks[k].position)
                    else:
                        break
                if 'a' not in start.position:  # kills on cross
                    for block in self.blocks:
                        if (block.position == '{}{}'.format(chr(ord(start.position[0]) - 1),
                                                            str(int(start.position[1]) + 1))) and (
                                block.label[1] == 'black'):
                            possible_positions.append(block.position)
                if 'h' not in start.position:  # kills on cross
                    for block in self.blocks:
                        if (block.position == '{}{}'.format(chr(ord(start.position[0]) + 1),
                                                            str(int(start.position[1]) + 1))) and (
                                block.label[1] == 'black'):
                            possible_positions.append(block.position)
        print(possible_positions)
        return end.position in possible_positions
