import time
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from pygame import mixer
from ttkthemes import themed_tk as tk
import os
import threading
from PIL import ImageTk, Image
from mutagen.mp3 import MP3

# Creating Parent-Window
root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")

# Create the Menu Bar
menu_bar = Menu(root)
root.config(menu=menu_bar)

# Create Sub-Menus
# SubMenu-1
sub_menu = Menu(menu_bar, tearoff=0)


# Browse-files
def browse_file():
    global file_path
    file_path = filedialog.askopenfilename()
    add_lb(file_path)


# Display Menu-Bar
menu_bar.add_cascade(label="File", menu=sub_menu)
sub_menu.add_command(label="New File", command=browse_file)
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

# Root (Parent) Window of HeartBeat
root.geometry('800x550')
root.title("HeartBeat")
root.iconbitmap(r'Images/HeartBeat.ico')

# Background Photo
photo = Image.open('C:\\Users\\a\\HeartBeat\\Images\\Orchestra.png')
back_photo = ImageTk.PhotoImage(photo)

# BackGround Image Of HeartBeat
background = ttk.Label(root, image=back_photo)
background.place(x=0, y=0)

# Headline Of HeartBeat
head_line = ttk.Label(root, text='The Crescendo Within.')
head_line.pack(side=TOP)

# Status-Bar
status_bar = ttk.Label(root, text="...It's HeartBeat Here.", relief=SUNKEN, anchor=W, font='YuGothic 10 bold')
status_bar.pack(side=BOTTOM, fill=X)

# Left-Frame
left_frame = ttk.Frame(root)
left_frame.pack(side=LEFT, padx=30, pady=20)

# Creating Playlist-Box
lb1 = Listbox(left_frame)
lb1.pack()

# playlist - Contains file + full path
playlist = []


# Add-Button
def add_lb(f):
    f = os.path.basename(file_path)
    index = 0
    lb1.insert(index, f)
    playlist.insert(index, file_path)
    index += 1


btn6 = ttk.Button(left_frame, text='Add', command=browse_file)
btn6.pack(side=LEFT)


# Remove-Button
def remove_btn():
    select_one = lb1.curselection()
    select_one = int(select_one[0])
    lb1.delete(select_one)
    playlist.pop(select_one)


btn7 = ttk.Button(left_frame, text='Remove', command=remove_btn)
btn7.pack(side=RIGHT)

# Right-Frame
right_frame = ttk.Frame(root)
right_frame.pack(side=LEFT, padx=30, pady=20)

# Top-Frame
top_frame = ttk.Frame(right_frame)
top_frame.pack()


# Show AudioFile-Details Function
def show_details(play_aud):
    file_data = os.path.splitext(play_aud)

    if file_data[1] == '.mp3':
        audio = MP3(play_aud)
        aud_length = audio.info.length
    else:
        a = mixer.Sound(play_aud)
        aud_length = a.get_length()

    # div(Quotient) - aud_length/60, mod(Remainder) - aud_length%60
    minutes, seconds = divmod(aud_length, 60)
    minutes = round(minutes)
    seconds = round(seconds)
    time_format = '{:02d}:{:02d}'.format(minutes, seconds)
    length['text'] = "Audio Length" + ' : ' + time_format

    # Start Threading
    t1 = threading.Thread(target=start_count, args=(aud_length,))
    t1.start()


# Length-Bar of AudioFile
length = ttk.Label(top_frame, text='Audio Length : --:--')
length.pack(pady=5)


# Start-Count Function
def start_count(t):
    ct = 0
    # mixer.music.get_busy()- Returns False value after pressing Stop or Pause button
    while ct <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            minutes, seconds = divmod(ct, 60)
            minutes = round(minutes)
            seconds = round(seconds)
            time_format = '{:02d}:{:02d}'.format(minutes, seconds)
            current_stat['text'] = "Current Status" + ' : ' + time_format
            time.sleep(1)
            ct += 1


# Current Status of Audio
current_stat = ttk.Label(top_frame, text='Current Status : --:--', relief=GROOVE)
current_stat.pack()

# Middle-Frame
middle_frame = ttk.Frame(right_frame)
middle_frame.pack(padx=30, pady=30)


# Play-Music
def play_btn():
    try:
        paused  # checks whether the 'pause'-variable is declared or not
    except NameError:  # if not; continues with this except-part of the code
        try:
            stop_btn()
            time.sleep(1)
            select_one = lb1.curselection()
            select_one = int(select_one[0])
            play_it = playlist[select_one]
            mixer.music.load(play_it)
            mixer.music.play()
            status_bar['text'] = "Playing Music..." + ' ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('Error', 'No File Found!')
    else:  # if yes; uses this un-pause functionality by tkinter
        mixer.music.unpause()
        status_bar['text'] = "Resumed..." + ' ' + os.path.basename(file_path)


photo1 = PhotoImage(file='Images/play (1).png')
btn1 = ttk.Button(middle_frame, image=photo1, command=play_btn)
btn1.grid(row=0, column=0, padx=10)


# Stop-Music
def stop_btn():
    mixer.music.stop()
    status_bar['text'] = "Track Stopped..." + ' ' + os.path.basename(file_path)


photo2 = PhotoImage(file='Images/stop (1).png')
btn2 = ttk.Button(middle_frame, image=photo2, command=stop_btn)
btn2.grid(row=0, column=1, padx=10)


# Pause-Music
def pause_btn():
    global paused
    paused = True
    mixer.music.pause()
    status_bar['text'] = "Paused..." + ' ' + os.path.basename(file_path)


photo3 = PhotoImage(file='Images/pause (1).png')
btn3 = ttk.Button(middle_frame, image=photo3, command=pause_btn)
btn3.grid(row=0, column=2, padx=10)

# Bottom-Frame
bottom_frame = ttk.Frame(right_frame)
bottom_frame.pack()


# Rewind-Music
def rewind_btn():
    play_btn()
    status_bar['text'] = "Rewinding..." + ' ' + os.path.basename(file_path)


photo4 = PhotoImage(file='Images/rewind (1).png')
btn4 = ttk.Button(bottom_frame, image=photo4, command=rewind_btn)
btn4.grid(row=0, column=0)

# Mute-Music
mute = False  # mute-Variable used as Switch


def mute_btn():
    global mute
    if mute:  # Turn Mute Off
        mixer.music.set_volume(0.2)
        btn5.configure(image=photo6)
        scale.set(20)
        mute = False
    else:  # Turn Mute On
        mixer.music.set_volume(0)
        btn5.configure(image=photo5)
        scale.set(0)
        mute = True


photo5 = PhotoImage(file='Images/mute (1).png')
photo6 = PhotoImage(file='Images/volume (1).png')
btn5 = ttk.Button(bottom_frame, image=photo6, command=mute_btn)
btn5.grid(row=0, column=1)


# Adjusting Volume Buttons
def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)  # set_volume of mixer takes value only from 0 to 1, e.g-0.1,0.55


scale = ttk.Scale(bottom_frame, from_=0, to=125, orient=HORIZONTAL, command=set_vol)
scale.set(60)  # Implement the Default Volume Value
mixer.music.set_volume(0.6)
scale.grid(row=0, column=2, pady=15, padx=37)


# Closing HeartBeat
def on_closing():
    tkinter.messagebox.showinfo('Exit HeartBeat', 'Music is still going on. You Sure ?')
    stop_btn()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
