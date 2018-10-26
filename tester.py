from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.geometry('900x1200')
img = ImageTk.PhotoImage(Image.open("Chess_bdt60.png"))
# canvas = Canvas(root, width=img.width() * 2, height=img.height() * 2)
# # canvas.pack()
# canvas.create_image(img.width() / 2, img.height() / 2, anchor=NW, image=img)
# for item in dir(canvas.create_image(img.width() / 2, img.height() / 2, anchor=NW, image=img)):
#     print(item)
# print(dir(Canvas.create_image(img.width() / 2, img.height() / 2, image=img)))
for i in range(8):
    root.columnconfigure(i)
    root.rowconfigure(i)
frame_list = []
label_list = []
for i in range(64):
    if (i // 8) % 2 == 0:
        if i % 2 != 0:
            frame_list.append(Frame(root, height=80, width=80, bg='grey'))
            label_list.append(Label(root, image=img, height=50, width=50, bg='grey'))
        else:
            frame_list.append(Frame(root, height=80, width=80, bg='white'))
            label_list.append(Label(root, image=img, height=50, width=50))
    else:
        if i % 2 != 0:
            frame_list.append(Frame(root, height=80, width=80, bg='white'))
            label_list.append(Label(root, image=img, height=50, width=50))
        else:
            frame_list.append(Frame(root, height=80, width=80, bg='grey'))
            label_list.append(Label(root, image=img, height=50, width=50, bg='grey'))
    frame_list[i].grid(row=i // 8, column=i % 8)
    label_list[i].grid(row=i // 8, column=i % 8)
root.mainloop()
