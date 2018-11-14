from PIL import ImageTk, Image


class Images:
    def __init__(self):
        self.images_let = ['pawn', 'knight', 'bishop', 'rook', 'rook_&_bishop', 'king']
        self.images_list = []
        self.__open_images()

    def __open_images(self):
        for letter in self.images_let:
            self.images_list.append((ImageTk.PhotoImage(Image.open(letter + '1.png')), 'black', letter))
            self.images_list.append((ImageTk.PhotoImage(Image.open(letter + '2.png')), 'white', letter))
        self.images_list.append((ImageTk.PhotoImage(Image.open('grey.png')), 'empty', ''))
        self.images_list.append((ImageTk.PhotoImage(Image.open('white.png')), 'empty', ''))

    def return_images(self):
        return self.images_list
