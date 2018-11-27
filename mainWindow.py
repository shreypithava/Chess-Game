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
        self.__turn_label = self.__check_label = self.__move_label = None
        self.__white_checked = False
        self.__black_checked = False
        self.__fen_stuff = []
        self.__king_position = ['e8', 'e1']  # 0 is black, 1 is white
        self.__white_all_positions = []
        self.__black_all_positions = []
        self.__piece_blocks = []
        self.__check_blocks = []
        self.__move_list = []
        self.__checkmate_checker_var = False
        self.__rest_of_init()

    def __checkmate_checker(self):
        for id1 in range(len(self.__blocks)):
            if self.__blocks[id1].label[1] == self.__turn_color:
                if self.__blocks[id1].label[2] == 'king':
                    continue
                self.__blocks[id1].print_content()
                pos = self.__move_checker(self.__blocks[id1])
                print(pos)
                for p in pos:
                    for id2 in range(len(self.__blocks)):
                        if p == self.__blocks[id2].position:
                            if self.__move_made(True, id1, id2):
                                print('Move Found')
                                self.__previous_move()
                                self.__checkmate_checker_var = False
                                return False
                            break
        return True

    def __move_made(self, next_move=False, bl_no=None, bl1_no=None):  # it starts here
        if next_move:  # this for checkmate checker
            temp = [True, [self.__blocks[bl_no], self.__blocks[bl1_no]]]
        else:
            temp = self.__move()
        if temp[0] or next_move:
            if self.__black_checked:
                self.__make_move(temp[1], check_checker=next_move)
                if self.__black_checked:
                    self.__previous_move()
                    return False
            elif self.__white_checked:
                self.__make_move(temp[1], check_checker=next_move)
                if self.__white_checked:
                    self.__previous_move()
                    return False
            else:
                self.__make_move(temp[1], check_checker=next_move)
                if (self.__white_checked and self.__turn_color == 'black') or (
                        self.__black_checked and self.__turn_color == 'white'):
                    self.__previous_move()
                    return False
            return True
        return False

    def __make_move(self, times, for_prev=False, check_checker=None):
        if not for_prev:
            if check_checker:
                self.__make_move2(times[0], times[1])
            else:
                if times[0].return_time() < times[1].return_time():
                    self.__make_move2(times[0], times[1])
                else:
                    self.__make_move2(times[1], times[0])
                for block in times:
                    block.reset_time()
        else:
            self.__make_move2(times[1], times[0], times[1].label[2] == 'pawn', times[2])

    def __make_move2(self, zero, one, pawn_prev=None, for_prev=None):
        print(self.__king_position)
        if zero.label[1] == self.__turn_color:
            if one.position in self.__move_checker(zero, one) or pawn_prev:
                if zero.label[2] == 'king':
                    if zero.label[1] == 'white':
                        self.__king_position[1] = one.position
                    else:
                        self.__king_position[0] = one.position
                if type(for_prev) is not int:
                    self.__move_list.append([zero, one, one.temp])
                    one.help_setup(zero.temp)
                    zero.empty_position()
                    self.__change_turn_label()
                else:
                    one.help_setup(zero.temp)
                    zero.help_setup(for_prev)
                self.__store_all_moves()
                self.__check_checker()

    def __check_checker(self):
        for block in self.__blocks:
            if block.label[1] != 'empty':
                if block.label[1] == 'white' and self.__king_position[0] in self.__move_checker(block):
                    self.__check_label['text'] = 'Black Checked'
                    self.__black_checked = True
                    if not self.__checkmate_checker_var:
                        self.__checkmate_checker_var = True
                        if self.__checkmate_checker():
                            self.__turn_color = ''
                            print('Game over')
                    return
                elif block.label[1] == 'black' and self.__king_position[1] in self.__move_checker(block):
                    self.__check_label['text'] = 'White Checked'
                    self.__white_checked = True
                    if not self.__checkmate_checker_var:
                        self.__checkmate_checker_var = True
                        if self.__checkmate_checker():
                            print('Game over')
                    return
        self.__black_checked = self.__white_checked = False
        self.__check_label['text'] = ''

    def __previous_move(self):
        # print(self.__move_list)
        temp = self.__move_list[len(self.__move_list) - 1]
        self.__move_list.remove(self.__move_list[len(self.__move_list) - 1])
        # print(self.__move_list)
        self.__change_turn_label()
        self.__make_move(temp, for_prev=True)

    def __move_checker(self, start, end=None, next_move=None):
        if end:
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
                    if self.__rook_and_bishop_helper(possible_positions, k, start, is_king, None, next_move):
                        break
            if 'a' not in start.position:  # leftwards
                for k in range(start_index - 1, 8 * (start_index // 8) - 1, -1):
                    if self.__rook_and_bishop_helper(possible_positions, k, start, is_king, None, next_move):
                        break
            if '8' not in start.position:  # upwards
                for k in range(start_index - 8, -1, -8):
                    if self.__rook_and_bishop_helper(possible_positions, k, start, is_king, None, next_move):
                        break
            if '1' not in start.position:  # downwards
                for k in range(start_index + 8, 64, 8):
                    if self.__rook_and_bishop_helper(possible_positions, k, start, is_king, None, next_move):
                        break
        if 'bishop' in piece_name or is_king or 'queen' in piece_name:
            if 'h' not in start.position:
                if '8' not in start.position:  # top rightwards
                    for k in range(start_index - 7, -1, -7):
                        if self.__rook_and_bishop_helper(possible_positions, k, start, is_king, 'h', next_move):
                            break
                if '1' not in start.position:  # bottom rightwards
                    for k in range(start_index + 9, 64, 9):
                        if self.__rook_and_bishop_helper(possible_positions, k, start, is_king, 'h', next_move):
                            break
            if 'a' not in start.position:
                if '8' not in start.position:  # top leftwards
                    for k in range(start_index - 9, -1, -9):
                        if self.__rook_and_bishop_helper(possible_positions, k, start, is_king, 'a', next_move):
                            break
                if '1' not in start.position:  # bottom leftwards
                    for k in range(start_index + 7, 64, 7):
                        if self.__rook_and_bishop_helper(possible_positions, k, start, is_king, 'a', next_move):
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
            if not next_move:
                for block in self.__blocks:
                    if block.position in possible_positions and block.label[1] == start.label[1]:
                        possible_positions.remove(block.position)
        elif piece_name == 'pawn':
            if start.label[1] == 'black':
                if '7' in start.position:
                    pawn_temp = 17
                else:
                    pawn_temp = 9
                if not next_move:
                    for k in range(start_index + 8, start_index + pawn_temp, 8):
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
                    pawn_temp = 17
                else:
                    pawn_temp = 9
                if not next_move:
                    for k in range(start_index - 8, start_index - pawn_temp, -8):
                        if self.__blocks[k].label[1] == 'empty':
                            possible_positions.append(self.__blocks[k].position)
                        else:
                            break
                if 'a' not in start.position:  # kills on cross
                    for block in self.__blocks:
                        if (block.position == '{}{}'.format(chr(ord(start.position[0]) - 1),
                                                            str(int(start.position[1]) + 1))) and (
                                block.label[1] == 'black' or next_move):
                            possible_positions.append(block.position)
                if 'h' not in start.position:  # kills on cross
                    for block in self.__blocks:
                        if (block.position == '{}{}'.format(chr(ord(start.position[0]) + 1),
                                                            str(int(start.position[1]) + 1))) and (
                                block.label[1] == 'black' or next_move):
                            possible_positions.append(block.position)
        if is_king and end:
            for pos in possible_positions:
                if start.label[1] == 'white':
                    if pos in self.__black_all_positions:
                        possible_positions.remove(pos)
                else:
                    if pos in self.__white_all_positions:
                        possible_positions.remove(pos)
        if end:
            print('Positions are {}'.format(possible_positions))
        return possible_positions

    def __rook_and_bishop_helper(self, possible_positions, k, start, is_king, letter=None, next_move=None):
        if self.__blocks[k].label[1] == 'empty':
            possible_positions.append(self.__blocks[k].position)
            if is_king or (letter and letter in self.__blocks[k].position):
                return True
        elif self.__blocks[k].label[1] != start.label[1] or next_move:
            possible_positions.append(self.__blocks[k].position)
            return True
        else:
            return True
        return False

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
        self.__fen_stuff[0].delete('0', tk.END)
        self.__fen_stuff[0].insert('0', fen)

    def __store_all_moves(self):
        self.__black_all_positions = []
        self.__white_all_positions = []
        for block in self.__blocks:
            if block.label[1] == 'white':
                for pos in self.__move_checker(block, next_move=True):
                    if pos not in self.__white_all_positions:
                        self.__white_all_positions.append(pos)
            elif block.label[1] == 'black':
                for pos in self.__move_checker(block, next_move=True):
                    if pos not in self.__black_all_positions:
                        self.__black_all_positions.append(pos)

    def __change_turn_label(self):
        if self.__turn_color == 'white':
            self.__turn_color = 'black'
        elif self.__turn_color == 'black':
            self.__turn_color = 'white'
        self.__turn_label['text'] = '{}{}\'s Turn'.format(self.__turn_color[0].upper(), self.__turn_color[1:])

    def run(self):
        self.__master.mainloop()

    def __setup(self):
        for block in self.__blocks:
            block.setup()

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
        self.__turn_label = tk.Label(self.__master,
                                     text='{}{}\'s Turn'.format(self.__turn_color[0].upper(), self.__turn_color[1:]))
        self.__turn_label.grid(row=9, column=0, columnspan=9)
        self.__move_label = tk.Label(self.__master)
        self.__move_label.grid(row=10, column=0, columnspan=9)
        self.__check_label = tk.Label(self.__master)
        self.__check_label.grid(row=11, column=0, columnspan=9)
        self.__fen_stuff.append(tk.Entry(self.__master))
        self.__previous_button = tk.Button(self.__master, text='Previous', command=self.__previous_move)
        self.__previous_button.grid(row=12, column=0, columnspan=9)
        self.__fen_stuff[0].grid(row=1, column=10, columnspan=6)
        self.__fen_stuff.append(tk.Button(self.__master, text='FEN to Game'))
        self.__fen_stuff[1].grid(row=2, column=10, columnspan=3)
        self.__fen_stuff.append(tk.Button(self.__master, text='Game to FEN', command=self.__game_to_fen))
        self.__fen_stuff[2].grid(row=2, column=13, columnspan=3)
        self.__setup()
        self.__store_all_moves()

    def __some_function(self, event=None):  # when 2 positions selected
        if event:
            pass
        if self.__move_made():
            print('-' * 50)

    def __move(self):
        temp = []
        for block in self.__blocks:
            if block.return_time():
                temp.append(block)
        return len(temp) == 2, temp
