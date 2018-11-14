import tkinter as tk
import block as bk


class Window:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title('Chess')
        self.master.geometry('900x900')
        # for i in range(9):
        #     self.master.rowconfigure(i)
        #     self.master.rowconfigure(i)
        self.blocks = []
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
        self.labeling = []
        for i in range(8):
            self.labeling.append((tk.Label(self.master, text=chr(97 + i)), tk.Label(self.master, text=8 - i)))
            self.labeling[i][0].grid(row=8, column=i)
            self.labeling[i][1].grid(row=i, column=8)
        self.__setup()
        self.button = tk.Button(self.master, text='Move', command=self.__make_move)
        self.button.grid(row=9)

    def run(self):
        self.master.mainloop()

    def __setup(self):
        for block in self.blocks:
            block.setup()

    def __make_move(self):
        times = []
        for i in self.blocks:
            if i.return_time():
                times.append(i)
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
            times[0].reset_time()
            times[1].reset_time()
        else:
            print('Only 2 click\'s expected')

    def __move_checker(self, start, end):
        print('{} to {}'.format(start.position, end.position))
        piece_name = start.label[2]
        possible_positions = []
        if piece_name == 'pawn':
            print('It is a pawn')
            if start.label[1] == 'black':
                print('It is black')
                if '7' in start.position:
                    print('On 7')
                    for i in range(2):
                        temp = None
                        for block in self.blocks:
                            if block.position == start.position[0] + str(int(start.position[1]) - (i + 1)):
                                temp = block
                                break
                        if temp.label[1] == 'empty':
                            possible_positions.append(temp.position)
                        else:
                            break
                else:
                    print('Not on 7')
                    for block in self.blocks:
                        if block.position == start.position[0] + str(int(start.position[1]) - 1) and block.label[1] == \
                                'empty':
                            possible_positions.append(block.position)
                            break
            else:
                print('It is white')
                if '2' in start.position:
                    print('On 2')
                    for i in range(2):
                        temp = None
                        for block in self.blocks:
                            if block.position == start.position[0] + str(int(start.position[1]) + (i + 1)):
                                temp = block
                                break
                        if temp.label[1] == 'empty':
                            possible_positions.append(temp.position)
                        else:
                            break
                else:
                    print('Not on 2')
                    for block in self.blocks:
                        if block.position == start.position[0] + str(int(start.position[1]) + 1) and block.label[1] == \
                                'empty':
                            possible_positions.append(block.position)
                            break
        if 'rook' in piece_name:
            if 'h' not in start.position:
                rook_positions = []
                temp = 0
                for i in range(len(self.blocks)):
                    if self.blocks[i] == start:
                        temp = ord('h') - ord(self.blocks[i].position[0])
                        break
                for i in range(temp):
                    rook_positions.append('{}{}'.format(chr(ord(start.position[0]) + i + 1), start.position[1]))
                breakout = False
                temp = 0
                for i in range(len(rook_positions)):
                    for block in self.blocks:
                        if rook_positions[i] == block.position and block.label[1] != 'empty':
                            breakout = True
                            temp = i
                            if (start.label[1] == 'white' and block.label[1] == 'black') or (
                                    start.label[1] == 'black' and block.label[1] == 'white'):
                                temp += 1
                            break
                    if breakout:
                        break
                while len(rook_positions) != temp:
                    rook_positions.pop()
                for i in rook_positions:
                    possible_positions.append(i)
            if 'a' not in start.position:
                for i in range(len(self.blocks)):
                    if start == self.blocks[i]:
                        for k in range(i - 1, 8 * (i // 8) - 1, -1):
                            if self.blocks[k].label[1] == 'empty':
                                possible_positions.append(self.blocks[k].position)
                            elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                    self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                                possible_positions.append(self.blocks[k].position)
                                break
                            else:
                                break
                        break
            if '8' not in start.position:
                for i in range(len(self.blocks)):
                    if start == self.blocks[i]:
                        for k in range(i - 1, 0, -1):
                            if self.blocks[k].position[0] == start.position[0]:
                                if self.blocks[k].label[1] == 'empty':
                                    possible_positions.append(self.blocks[k].position)
                                elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                        self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                                    possible_positions.append(self.blocks[k].position)
                                    break
                                else:
                                    break
                        break
            if '1' not in start.position:
                for i in range(len(self.blocks)):
                    if start == self.blocks[i]:
                        for k in range(i + 1, 64):
                            if self.blocks[k].position[0] == start.position[0]:
                                if self.blocks[k].label[1] == 'empty':
                                    possible_positions.append(self.blocks[k].position)
                                elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                        self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                                    possible_positions.append(self.blocks[k].position)
                                    break
                                else:
                                    break
                        break
        if 'bishop' in piece_name:
            if 'h' not in start.position:
                if '8' not in start.position:  # top rightwards
                    for i in range(len(self.blocks)):
                        if start == self.blocks[i]:
                            for k in range(i - 7, -1, -7):
                                if self.blocks[k].label[1] == 'empty':
                                    possible_positions.append(self.blocks[k].position)
                                elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                        self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                                    possible_positions.append(self.blocks[k].position)
                                    break
                                if 'h' in self.blocks[k].position:
                                    break
                            break
                if '1' not in start.position:
                    for i in range(len(self.blocks)):  # bottom rightwards
                        if start == self.blocks[i]:
                            for k in range(i + 9, 64, 9):
                                if self.blocks[k].label[1] == 'empty':
                                    possible_positions.append(self.blocks[k].position)
                                elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                        self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                                    possible_positions.append(self.blocks[k].position)
                                    break
                                else:
                                    break
                                if 'a' in self.blocks[k].position:
                                    break
                            break
            if 'a' not in start.position:
                if '8' not in start.position:  # top leftwards
                    for i in range(len(self.blocks)):
                        if start == self.blocks[i]:
                            for k in range(i - 9, -1, -9):
                                if self.blocks[k].label[1] == 'empty':
                                    possible_positions.append(self.blocks[k].position)
                                elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                        self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                                    possible_positions.append(self.blocks[k].position)
                                    break
                                else:
                                    break
                                if 'a' in self.blocks[k].position:
                                    break
                            break
                if '1' not in start.position:  # bottom leftwards
                    for i in range(len(self.blocks)):
                        if start == self.blocks[i]:
                            for k in range(i + 7, 64, 7):
                                if self.blocks[k].label[1] == 'empty':
                                    possible_positions.append(self.blocks[k].position)
                                elif (self.blocks[k].label[1] == 'black' and start.label[1] == 'white') or (
                                        self.blocks[k].label[1] == 'white' and start.label[1] == 'black'):
                                    possible_positions.append(self.blocks[k].position)
                                    break
                                else:
                                    break
                                if 'a' in self.blocks[k].position:
                                    break
                            break
        if piece_name == 'knight':
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
        print(possible_positions)
        return end.position in possible_positions

# rook right done, start doing left
