import tkinter as tk
import block as bk


class Window:
    def __init__(self):
        self.__master = tk.Tk()
        self.__master.title('Chess')
        self.__master.geometry('680x680')
        self.__blocks = []
        self.__labeling = []
        self.__turn_color = 'white'
        self.__turn_label = None
        self.fen_stuff = []
        self.__rest_of_init()

    def __rest_of_init(self):
        self.__master.bind('<1>', self.__some_function)
        for i in range(64):
            if i // 8 % 2 == 0:
                if i % 2 == 0:
                    self.__blocks.append(bk.Block(self.__master, 'white', i))
                else:
                    self.__blocks.append(bk.Block(self.__master, 'grey', i))
            else:
                if i % 2 == 0:
                    self.__blocks.append(bk.Block(self.__master, 'grey', i))
                else:
                    self.__blocks.append(bk.Block(self.__master, 'white', i))
        for i in range(8):
            self.__labeling.append((tk.Label(self.__master, text=chr(97 + i)), tk.Label(self.__master, text=8 - i)))
            self.__labeling[i][0].grid(row=8, column=i)
            self.__labeling[i][1].grid(row=i, column=8)
        self.__turn_label = tk.Label(self.__master, text='{}\'s Turn'.format(self.__turn_color))
        self.__turn_label.grid(row=9, column=0, columnspan=9)
        self.fen_stuff.append(tk.Entry(self.__master))
        self.fen_stuff[0].grid(row=1, column=10, columnspan=6)
        self.fen_stuff.append(tk.Button(self.__master, text='FEN to Game'))
        self.fen_stuff[1].grid(row=2, column=10, columnspan=3)
        self.fen_stuff.append(tk.Button(self.__master, text='Game to FEN', command=self.__game_to_fen))
        self.fen_stuff[2].grid(row=2, column=13, columnspan=3)
        self.__setup()

    def __some_function(self, event=None):
        if event:
            pass
        if self.__move():
            self.__make_move()

    def run(self):
        self.__master.mainloop()

    def __setup(self):
        for block in self.__blocks:
            block.setup()

    def __move(self):
        temp = []
        for block in self.__blocks:
            if block.return_time():
                temp.append(block)
        return len(temp) == 2

    def __make_move(self):
        times = []
        for block in self.__blocks:
            if block.return_time():
                times.append(block)
        if len(times) == 2:
            if times[0].return_time() < times[1].return_time():
                if times[0].label[1] == self.__turn_color:
                    if self.__move_checker(times[0], times[1]):
                        print()
                        times[1].help_setup(times[0].temp)
                        times[0].empty_position()
                        self.__change_turn_label()
                    else:
                        print('Not a valid Move')
            else:
                if times[1].label[1] == self.__turn_color:
                    if self.__move_checker(times[1], times[0]):
                        times[0].help_setup(times[1].temp)
                        times[1].empty_position()
                        self.__change_turn_label()
                    else:
                        print('Not a valid Move')
        else:
            print('2 positions not selected')
        for block in times:
            block.reset_time()

    def __change_turn_label(self):
        if self.__turn_color == 'white':
            self.__turn_color = 'black'
        else:
            self.__turn_color = 'white'
        self.__turn_label['text'] = '{}\'s turn'.format(self.__turn_color)

    def __move_checker(self, start, end):
        print('{} to {}'.format(start.position, end.position))
        piece_name = start.label[2]
        possible_positions = []
        start_index = 0
        is_king = 'king' in piece_name
        for i in range(len(self.__blocks)):
            if start == self.__blocks[i]:
                start_index = i
                break
        if 'rook' in piece_name or is_king or 'queen' in piece_name:
            if 'h' not in start.position:  # rightwards
                for k in range(start_index + 1, (start_index // 8 + 1) * 8):
                    if self.__blocks[k].label[1] == 'empty':
                        possible_positions.append(self.__blocks[k].position)
                        if is_king:
                            break
                    elif (self.__blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                            self.__blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                        possible_positions.append(self.__blocks[k].position)
                        break
                    else:
                        break
            if 'a' not in start.position:  # leftwards
                for k in range(start_index - 1, 8 * (start_index // 8) - 1, -1):
                    if self.__blocks[k].label[1] == 'empty':
                        possible_positions.append(self.__blocks[k].position)
                        if is_king:
                            break
                    elif (self.__blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                            self.__blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                        possible_positions.append(self.__blocks[k].position)
                        break
                    else:
                        break
            if '8' not in start.position:  # upwards
                for k in range(start_index - 8, -1, -8):
                    if self.__blocks[k].label[1] == 'empty':
                        possible_positions.append(self.__blocks[k].position)
                        if is_king:
                            break
                    elif (self.__blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                            self.__blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                        possible_positions.append(self.__blocks[k].position)
                        break
                    else:
                        break
            if '1' not in start.position:  # downwards
                for k in range(start_index + 8, 64, 8):
                    if self.__blocks[k].label[1] == 'empty':
                        possible_positions.append(self.__blocks[k].position)
                        if is_king:
                            break
                    elif (self.__blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                            self.__blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                        possible_positions.append(self.__blocks[k].position)
                        break
                    else:
                        break
        if 'bishop' in piece_name or is_king or 'queen' in piece_name:
            if 'h' not in start.position:
                if '8' not in start.position:  # top rightwards
                    for k in range(start_index - 7, -1, -7):
                        if self.__blocks[k].label[1] == 'empty':
                            possible_positions.append(self.__blocks[k].position)
                            if is_king:
                                break
                        elif (self.__blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                self.__blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                            possible_positions.append(self.__blocks[k].position)
                            break
                        else:
                            break
                        if 'h' in self.__blocks[k].position:
                            break
                if '1' not in start.position:  # bottom rightwards
                    for k in range(start_index + 9, 64, 9):
                        if self.__blocks[k].label[1] == 'empty':
                            possible_positions.append(self.__blocks[k].position)
                            if is_king:
                                break
                        elif (self.__blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                self.__blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                            possible_positions.append(self.__blocks[k].position)
                            break
                        else:
                            break
                        if 'h' in self.__blocks[k].position:
                            break
            if 'a' not in start.position:
                if '8' not in start.position:  # top leftwards
                    for k in range(start_index - 9, -1, -9):
                        if self.__blocks[k].label[1] == 'empty':
                            possible_positions.append(self.__blocks[k].position)
                            if is_king:
                                break
                        elif (self.__blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                self.__blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                            possible_positions.append(self.__blocks[k].position)
                            break
                        else:
                            break
                        if 'a' in self.__blocks[k].position:
                            break
                if '1' not in start.position:  # bottom leftwards
                    for k in range(start_index + 7, 64, 7):
                        if self.__blocks[k].label[1] == 'empty':
                            possible_positions.append(self.__blocks[k].position)
                            if is_king:
                                break
                        elif (self.__blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                self.__blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                            possible_positions.append(self.__blocks[k].position)
                            break
                        else:
                            break
                        if 'a' in self.__blocks[k].position:
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
            for block in self.__blocks:
                if block.position in possible_positions and block.label[1] == start.label[1]:
                    possible_positions.remove(block.position)
        elif piece_name == 'pawn':
            if start.label[1] == 'black':
                if '7' in start.position:
                    __temp = 17
                else:
                    __temp = 9
                for k in range(start_index + 8, start_index + __temp, 8):
                    if self.__blocks[k].label[1] == 'empty':
                        possible_positions.append(self.__blocks[k].position)
                    else:
                        break
                if 'a' not in start.position:  # kills on cross
                    for block in self.__blocks:
                        if (block.position == '{}{}'.format(chr(ord(start.position[0]) - 1),
                                                            str(int(start.position[1]) - 1))) and (
                                block.label[1] == 'white'):
                            possible_positions.append(block.position)
                if 'h' not in start.position:  # kills on cross
                    for block in self.__blocks:
                        if (block.position == '{}{}'.format(chr(ord(start.position[0]) + 1),
                                                            str(int(start.position[1]) - 1))) and (
                                block.label[1] == 'white'):
                            possible_positions.append(block.position)
            else:
                if '2' in start.position:
                    __temp = 17
                else:
                    __temp = 9
                for k in range(start_index - 8, start_index - __temp, -8):
                    if self.__blocks[k].label[1] == 'empty':
                        possible_positions.append(self.__blocks[k].position)
                    else:
                        break
                if 'a' not in start.position:  # kills on cross
                    for block in self.__blocks:
                        if (block.position == '{}{}'.format(chr(ord(start.position[0]) - 1),
                                                            str(int(start.position[1]) + 1))) and (
                                block.label[1] == 'black'):
                            possible_positions.append(block.position)
                if 'h' not in start.position:  # kills on cross
                    for block in self.__blocks:
                        if (block.position == '{}{}'.format(chr(ord(start.position[0]) + 1),
                                                            str(int(start.position[1]) + 1))) and (
                                block.label[1] == 'black'):
                            possible_positions.append(block.position)
        print(possible_positions)
        return end.position in possible_positions

    def __game_to_fen(self):
        fen = ''
        number = 0
        for block in self.__blocks:
            if self.__blocks.index(block) % 8 == 0 and self.__blocks.index(block) != 0:  # next line
                if number == 0:  # if last is number
                    fen += '/'
                else:  # if last is not number
                    fen += '{}/'.format(number)
                    number = 0
            if block.label[1] == 'empty':  # if block is empty
                number += 1
            elif block.label[1] == 'black':  # if block is black
                if number != 0:  # if empty space before
                    fen += '{}'.format(number)
                    number = 0
                if block.label[2] == 'knight':
                    fen += 'n'
                else:
                    fen += '{}'.format(block.label[2][0])
            else:  # if block is white
                if number != 0:
                    fen += '{}'.format(number)
                    number = 0
                if block.label[2] == 'knight':
                    fen += 'N'
                else:
                    fen += '{}'.format(block.label[2][0].upper())

        self.fen_stuff[0].delete('0', tk.END)
        self.fen_stuff[0].insert('0', fen)
