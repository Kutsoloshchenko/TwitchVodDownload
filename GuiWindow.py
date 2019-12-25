from tkinter import *
from TwitchDowloader import *


window = Tk()
window.title("Twitch Downloader")
window.geometry('450x75')

txt = Entry(window, width=50)

txt.grid(column=1, row=0, padx = 20, pady = 20)

def clicked():
    download_video(txt.get())

btn = Button(window, text="download", command=clicked)

btn.grid(column=2, row=0)

window.mainloop()
