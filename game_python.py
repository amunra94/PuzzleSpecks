from tkinter import * # Некрасиво, но сэкономило время
from random import * # Некрасиво
from PIL import Image, ImageTk

import os

SIDE = 4
count = 0


def make_mosaik(filename='test.jpg'):
    image = Image.open(filename)
    regions = []
    pixels = image.width // SIDE
    for i in range(SIDE):
        for j in range(SIDE):
            x1 = j * pixels
            y1 = i * pixels
            x2 = j * pixels + pixels
            y2 = i * pixels + pixels
            box = (x1, y1, x2, y2)
            region = image.crop(box)
            region.load()
            regions.append(ImageTk.PhotoImage(region))
    return regions


def key_press(btn, flag=True):
    near = None
    global count
    if btn == 'r' and curr.column > 0:
        near = label_left(curr)
        curr.column -= 1
        near.column += 1
        if flag: count += 1
    elif btn == 'l' and curr.column < SIDE - 1:
        near = label_right(curr)
        curr.column += 1
        near.column -= 1
        if flag: count += 1
    elif btn == 'u' and curr.row < SIDE - 1:
        near = label_under(curr)
        curr.row += 1
        near.row -= 1
        if flag: count += 1
    elif btn == 'd' and curr.row > 0:
        near = label_above(curr)
        curr.row -= 1
        near.row += 1
        if flag: count += 1
    exchange(curr, near)
    grid_x(curr, near)

    label_click['text'] = 'Steps: ' + str(count)
    if flag:
        check_end()

def check_end():
    flag_right = 0
    for i, lab in enumerate(labels):
        if i != lab.index:
            flag_right += 1
    if flag_right == 0:
        end()


def grid_x(curr, near):
    if near is not None:
        curr.grid(row=curr.row, column=curr.column)
        near.grid(row=near.row, column=near.column)


def end():
    label_click['text'] = 'Succesfull!'


def exchange(curr, near):
    if near is not None:
        ci = curr.row * SIDE + curr.column
        ni = near.row * SIDE + near.column
        labels[ci], labels[ni] = labels[ni], labels[ci]


def label_above(curr):
    return labels[(curr.row - 1) * SIDE + curr.column]


def label_under(curr):
    return labels[(curr.row + 1) * SIDE + curr.column]


def label_right(curr):
    return labels[curr.row * SIDE + curr.column + 1]


def label_left(curr):
    return labels[curr.row * SIDE + curr.column - 1]


def mix_up():
    buttons = ('u', 'd', 'l', 'r')
    for i in range(SIDE ** 5):
        key_press(choice(buttons), 0)


files = [os.path.join('nums', f) for f in sorted(os.listdir('nums'))]

main_window = Tk()
main_window.title("Пятнашки")
images = [PhotoImage(file=f) for f in files]
# images = make_mosaik()
# images[-1] = nums[-1]
labels = []
for i in range(SIDE):
    for j in range(SIDE):
        label = Label(main_window,
                      text="Hello",
                      image=images[i * SIDE + j])
        label.index = i * SIDE + j
        label.row = i
        label.column = j
        label.grid(row=i, column=j)  # Расположение лэйблов
        labels.append(label)
label_click = Label(main_window,
                    text='Wait!')
label_click.grid(row=4, column=0)

menu_main = Menu(main_window)

curr = labels[-1]

main_window.bind('<Right>', lambda e: key_press('r'))
main_window.bind('<Left>', lambda e: key_press('l'))
main_window.bind('<Up>', lambda e: key_press('u'))
main_window.bind('<Down>', lambda e: key_press('d'))

main_window.after(2000, mix_up)

main_window.mainloop()
