from PIL import ImageTk, Image


class Images:
    def __init__(self):
        self.__images_let = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
        self.__images_list = []
        self.__open_images()

    def __open_images(self):
        for letter in self.__images_let:
            self.__images_list.append((ImageTk.PhotoImage(Image.open(letter + '1.png')), 'black', letter))
            self.__images_list.append((ImageTk.PhotoImage(Image.open(letter + '2.png')), 'white', letter))
        self.__images_list.append((ImageTk.PhotoImage(Image.open('grey.png')), 'empty', ''))
        self.__images_list.append((ImageTk.PhotoImage(Image.open('white.png')), 'empty', ''))

    def return_images(self):
        return self.__images_list
