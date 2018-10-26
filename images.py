from PIL import ImageTk, Image


class Images:
    def __init__(self):
        self.images_let = ['p', 'h', 'b', 'r', 'q', 'k']
        self.images_list = []

    def open_images(self):
        for letter in self.images_let:
            for i in range(2):
                if i == 0:
                    self.images_list.append((ImageTk.PhotoImage(Image.open(letter + str(i + 1) + '.png')), 'black'))
                else:
                    self.images_list.append((ImageTk.PhotoImage(Image.open(letter + str(i + 1) + '.png')), 'white'))
        self.images_list.append((ImageTk.PhotoImage(Image.open('g.png')), 'blank'))
        self.images_list.append((ImageTk.PhotoImage(Image.open('w.png')), 'blank'))
        return self.images_list
