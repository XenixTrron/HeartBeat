from tkinter import *
import tkinter.messagebox
from pygame import mixer

root = Tk()

# Create the Menu Bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Create Sub-Menus
# SubMenu-1
sub_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=sub_menu)
sub_menu.add_command(label="New File")
sub_menu.add_command(label="Open")
sub_menu.add_command(label="Exit", command=root.destroy)


# SubMenu-2
def abt_heartbeat():
    tkinter.messagebox.showinfo('HeartBeat', 'This Media Player is designed using Basic UI known as Tkinter in '
                                             'Python.Further version of this Player will be much more sophisticated.'
                                             'Aspiring to be Leading Artist Destination- An Ultimate '
                                             'Streaming-Service Application.')


def abt_developer():
    tkinter.messagebox.showinfo('About Developer', "Developer of HeartBeat is Tejas Karanjkar.He's an aspiring "
                                                   "Inventor currently studying Web & Application Development.")


sub_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=sub_menu)
sub_menu.add_command(label="About HeartBeat", command=abt_heartbeat)
sub_menu.add_command(label="About Developer", command=abt_developer)
sub_menu.add_command(label="Visit Us")

mixer.init()  # initializing the mixer

root.geometry('400x400')
root.title("HeartBeat")
root.iconbitmap(r'HeartBeat.ico')

text = Label(root, text='The Crescendo Within.')
text.pack()

# photo = PhotoImage(file="Orchestra.png")
# label_photo = Label(root, image=photo)
# label_photo.pack()


# Play-Music
def play_btn():
    mixer.music.load("PianoCine.mp3")
    mixer.music.play()


photo1 = PhotoImage(file='play (1).png')
btn1 = Button(root, image=photo1, command=play_btn)
btn1.pack()


# Stop-Music
def stop_btn():
    mixer.music.stop()


photo2 = PhotoImage(file='stop (1).png')
btn2 = Button(root, image=photo2, command=stop_btn)
btn2.pack()


# Adjusting Volume Buttons
def set_vol(val):
    volume = int(val)/100
    mixer.music.set_volume(volume)  # set_volume of mixer takes value only from 0 to 1, e.g-0.1,0.55


scale = Scale(root, from_=0, to=125, orient=HORIZONTAL, command=set_vol)
scale.set(60)
mixer.music.set_volume(60)
scale.pack()

root.mainloop()
