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

    def open_file(self, filename):
        import os
        import subprocess
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path = os.path.join(downloads_path, filename)
        
        # Check if file exists
        if os.path.exists(file_path):
            # Open file with default application
            os.startfile(file_path)
        else:
            # Try to find the file with a counter suffix
            name, ext = os.path.splitext(filename)
            counter = 1
            while counter <= 10:  # Check up to 10 variations
                alt_filename = f"{name}_{counter}{ext}"
                alt_path = os.path.join(downloads_path, alt_filename)
                if os.path.exists(alt_path):
                    os.startfile(alt_path)
                    return
                counter += 1
            
            # If file not found, open Downloads folder
            os.startfile(downloads_path)

    def open_window(self, msg, imagesPath, selectedPic='random'):
        if len(sys.argv) > 3:
            selectedPic = sys.argv[3]
        
        # Check for sticky note color parameter
        note_color = 'yellow'  # default
        if len(sys.argv) > 4:
            note_color = sys.argv[4]
            
        chosenPic = self.get_selected_pic(imagesPath, selectedPic)
        print(f"Using picture: {chosenPic}")
        
        # Check if this is a file notification or sticky note
        is_file_notification = msg.startswith("📁 File received:")
        is_sticky_note = msg.startswith("📝 Sticky Note:")
        filename = None
        
        if is_file_notification:
            # Extract filename from message
            filename = msg.replace("📁 File received: ", "")
        
        root = Tk()

        # This is the section of code which creates the main window
        if is_sticky_note:
            # Use sticky note colors
            color_map = {
                'yellow': '#FFFF99',
                'pink': '#FFB6C1', 
                'blue': '#ADD8E6',
                'green': '#90EE90',
                'orange': '#FFD700'
            }
            window_color = color_map.get(note_color, '#FFFF99')
            root.title('📝 Sticky Note')
        else:
            window_color = random.choice(['#EE3B3B', '#FFC300', '#DAF7A6', '#FF5733', '#C70039', '#900C3F', '#581845', '#28A745'])
            root.title('Wiadom.')
        
        # Make window taller if it's a file notification (for the extra button)
        window_height = 220 if is_file_notification else 180
        root.geometry(f'492x{window_height}')
        root.configure(background=window_color)

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

        # Different button layouts based on message type
        if is_sticky_note:
            # Sticky notes only have a "Got it!" button
            def got_it_response():
                root.destroy()
            
            Button(root, text='📌 Got it!', bg='#FFD700', font=('arial', 16, 'bold'), 
                   command=got_it_response).place(x=180, y=100)
        else:
            # Regular messages and file notifications have response buttons
            def ok_response():
                self.send_response('ok')
                root.destroy()
                
            def not_ok_response():
                self.send_response('not_ok')
                root.destroy()

            # File open button (only for file notifications)
            if is_file_notification and filename:
                def open_file_action():
                    self.open_file(filename)
                    root.destroy()
                
                Button(root, text='📂 Open File', bg='#87CEEB', font=('arial', 12, 'bold'), 
                       command=open_file_action).place(x=110, y=140)

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
