import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import pyttsx3
import cherrypy
class GUIWindow():
    def __init__(self):
        pass
    def get_random_pic(self,path):
        import glob, os,random
        os.chdir(path)
        return os.path.join(path,random.choice(glob.glob("*.gif")+glob.glob("*.jpg")+glob.glob("*.png")))

    def open_window(self, msg, imagesPath):
        randomPic = self.get_random_pic(imagesPath)
        print(randomPic)
        root = Tk()

        # This is the section of code which creates the main window
        # w = 492
        # h = 138
        # ws = root.winfo_screenwidth()
        # hs = root.winfo_screenheight()
        # x = (ws / 2) - (w / 2)
        # y = (hs / 2) - (h / 2)
        # root.geometry('+%d+%d' % (x, y))

        root.geometry('492x138')
        root.configure(background='#EE3B3B')
        root.title('Wiadom.')

        # First, we create a canvas to put the picture on
        pic = Image.open(randomPic)
        pic=pic.resize((48,48), Image.ANTIALIAS)

        worthAThousandWords = Canvas(root, height=48, width=48)
        # Then, we actually create the image file to use (it has to be a *.gif)
        picture_file = ImageTk.PhotoImage(pic)  # <-- you will have to copy-paste the filepath here, for example 'C:\Desktop\pic.gif'
        # Finally, we create the image on the canvas and then place it onto the main window
        worthAThousandWords.create_image(48, 0, anchor=NE, image=picture_file)
        worthAThousandWords.place(x=27, y=38)

        # This is the section of code which creates the a label
        Label(root, text=msg, bg='#F0F8FF', font=('Comic Sans MS', 12, 'normal')).place(x=110, y=55)

        # This is the section of code which creates a button
        Button(root, text='X', bg='#F0F8FF', font=('arial', 12, 'normal'), command=lambda: sys.exit()).place(x=452, y=1)

        # root.overrideredirect(True)
        root.wm_attributes("-topmost", 1)
        root.mainloop()






import sys
print(sys.argv)
GUIWindow().open_window(sys.argv[1], sys.argv[2])
