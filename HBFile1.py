from tkinter import *
from tkinter import Label, font

win = Tk()
fonts = list(font.families())

rowcount = 0
column_count = 0

for i in fonts:
    if rowcount % 30 == 0:
        column_count += 1
        rowcount = 0
    Label(win, text=i, font=(i, 10, 'bold')).grid(row=rowcount, column=column_count)
    rowcount += 1

win.mainloop()
