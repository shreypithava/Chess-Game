import tkinter as tk
import block as bk
import images as im
import random as rm


class Window:
    def __init__(self):
        self.master = tk.Tk()
        self.master.title('Chess')
        self.master.geometry('900x1200')
        self.images = im.Images()
        self.images_list = self.images.open_images()
        for i in range(10):
            self.master.rowconfigure(i)
            self.master.rowconfigure(i)
        self.blocks = []
        for i in range(64):
            if i // 8 % 2 == 0:
                if i % 2 == 0:
                    self.blocks.append(bk.Block(self.master, 'white', i, rm.choice(self.images.images_list)))
                else:
                    self.blocks.append(bk.Block(self.master, 'grey', i, rm.choice(self.images.images_list)))
            else:
                if i % 2 == 0:
                    self.blocks.append(bk.Block(self.master, 'grey', i, rm.choice(self.images.images_list)))
                else:
                    self.blocks.append(bk.Block(self.master, 'white', i, rm.choice(self.images.images_list)))
        self.labeling = []
        for i in range(8):
            self.labeling.append((tk.Label(self.master, text=chr(97 + i)), tk.Label(self.master, text=8 - i)))
            self.labeling[i][0].grid(row=8, column=i, sticky='s')
            self.labeling[i][1].grid(row=i, column=8, sticky='e')

    def run(self):
        print('Running')
        self.master.mainloop()
        print('Stop')
