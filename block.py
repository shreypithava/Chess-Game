import tkinter as tk


class Block:
    def __init__(self, window, color, i, im=None):
        self.frame = tk.Frame(window, height=80, width=80, bg=color)
        self.frame.grid(row=i // 8, column=i % 8)
        self.label = [tk.Label(window, image=im[0], height=50, width=50, bg=color), im[1]]
        self.label[0].grid(row=i // 8, column=i % 8)
