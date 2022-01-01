import tkinter as tk
from tkinter import ttk
from tkinter import *
import pyttsx3
import cherrypy
class GUIWindow():
    def __init__(self):
        pass
    def open_window(self, msg):
        root = Tk()

        # This is the section of code which creates the main window
        root.geometry('626x395')
        root.configure(background='#EE3B3B')
        root.title('Wiadom.')


        # This is the section of code which creates the a label
        Label(root, text=msg, bg='#EE3B3B', font=('Comic Sans MS', 12, 'normal')).place(x=179, y=134)

        root.wm_attributes("-topmost", 1)
        root.mainloop()


import sys
print(sys.argv)
GUIWindow().open_window(sys.argv[1])
