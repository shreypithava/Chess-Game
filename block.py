import tkinter as tk
import images as im
import random as rm
import time

a = 5


class Block:
    def __init__(self, window, color, i):
        self.__time = self.temp = self.images = self.images_list = self.image = self.frame = self.position = \
            self.label = None
        self.__rest_of_init(window, color, i)

    def __rest_of_init(self, window, color, i):
        self.images = im.Images()
        self.images_list = self.images.return_images()
        self.image = rm.choice(self.images_list)
        self.frame = tk.Frame(window, height=a, width=a, bg=color)
        self.frame.grid(row=i // 8, column=i % 8)
        self.position = '{}{}'.format(chr(97 + (i % 8)), 8 - i // 8)
        self.label = [tk.Label(self.frame, image=self.image[0], height=50, width=50, bg=color), self.image[1],
                      self.image[2]]
        self.label[0].grid()
        self.label[0].bind("<1>", self.__click)
        self.empty_position()

    def setup(self):
        if self.position == 'a8' or self.position == 'h8':  # black rook
            self.help_setup(6)
        elif self.position == 'b8' or self.position == 'g8':  # black knight
            self.help_setup(2)
        elif self.position == 'c8' or self.position == 'f8':  # black bishop
            self.help_setup(4)
        elif self.position == 'a1' or self.position == 'h1':  # white rook
            self.help_setup(7)
        elif self.position == 'b1' or self.position == 'g1':  # white knight
            self.help_setup(3)
        elif self.position == 'c1' or self.position == 'f1':  # white bishop
            self.help_setup(5)
        elif self.position == 'd8':  # black queen
            self.help_setup(8)
        elif self.position == 'd1':  # white queen
            self.help_setup(9)
        elif self.position == 'e8':  # black king
            self.help_setup(10)
        elif self.position == 'e1':  # white king
            self.help_setup(11)
        elif '7' in self.position:  # black pawns
            self.help_setup(0)
        elif '2' in self.position:  # white pawns
            self.help_setup(1)

    def help_setup(self, num):
        self.label[0]['image'] = self.images_list[num][0]
        self.label[1] = self.images_list[num][1]
        self.label[2] = self.images_list[num][2]
        self.temp = num

    def __click(self, event=None):
        if event:
            pass
        self.__time = time.time()

    def return_time(self):
        return self.__time

    def empty_position(self):
        if self.frame['bg'] == 'white':
            self.help_setup(13)
        else:
            self.help_setup(12)

    def reset_time(self):
        self.__time = None
