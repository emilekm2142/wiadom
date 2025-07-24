import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import pyttsx3
import random
import cherrypy
import requests
import sys
class GUIWindow():
    def __init__(self):
        pass
    def get_random_pic(self,path):
        import glob, os,random
        os.chdir(path)
        return os.path.join(path,random.choice(glob.glob("*.gif")+glob.glob("*.jpg")+glob.glob("*.png")))
    
    def get_selected_pic(self, path, picture_name):
        if picture_name == 'random':
            return self.get_random_pic(path)
        else:
            return os.path.join(path, picture_name)

    def send_response(self, response):
        try:
            requests.post('http://localhost:8080/response', json={'response': response})
        except:
            pass  # If server is not running, just ignore

    def open_window(self, msg, imagesPath, selectedPic='random'):
        if len(sys.argv) > 3:
            selectedPic = sys.argv[3]
        chosenPic = self.get_selected_pic(imagesPath, selectedPic)
        print(f"Using picture: {chosenPic}")
        root = Tk()

        # This is the section of code which creates the main window
        random_color = random.choice(['#EE3B3B', '#FFC300', '#DAF7A6', '#FF5733', '#C70039', '#900C3F', '#581845', '#28A745'])
        root.geometry('492x180')  # Made taller for buttons
        root.configure(background=random_color)
        root.title('Wiadom.')

        # First, we create a canvas to put the picture on
        pic = Image.open(chosenPic)
        pic=pic.resize((48,48), Image.LANCZOS)

        worthAThousandWords = Canvas(root, height=48, width=48)
        # Then, we actually create the image file to use (it has to be a *.gif)
        picture_file = ImageTk.PhotoImage(pic)  # <-- you will have to copy-paste the filepath here, for example 'C:\Desktop\pic.gif'
        # Finally, we create the image on the canvas and then place it onto the main window
        worthAThousandWords.create_image(48, 0, anchor=NE, image=picture_file)
        worthAThousandWords.place(x=27, y=38)

        # This is the section of code which creates the a label
        Label(root, text=msg, bg='#F0F8FF', font=('Comic Sans MS', 12, 'normal')).place(x=110, y=55)

        # Response buttons
        def ok_response():
            self.send_response('ok')
            root.destroy()
            
        def not_ok_response():
            self.send_response('not_ok')
            root.destroy()

        Button(root, text='👌', bg='#90EE90', font=('arial', 14, 'bold'), 
               command=ok_response).place(x=110, y=100)
        
        Button(root, text='🚫', bg='#FFB6C1', font=('arial', 14, 'bold'), 
               command=not_ok_response).place(x=250, y=100)

        # This is the section of code which creates a button
        Button(root, text='X', bg='#F0F8FF', font=('arial', 12, 'normal'), command=lambda: root.destroy()).place(x=452, y=1)

        # root.overrideredirect(True)
        root.wm_attributes("-topmost", 1)
        root.mainloop()






import sys
print(sys.argv)
GUIWindow().open_window(sys.argv[1], sys.argv[2])
