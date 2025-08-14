import tkinter as tk
from tkinter import ttk
from tkinter import *
from time import sleep
import pyttsx3
import cherrypy
import sys, subprocess
import os
from datetime import datetime
from pathlib import Path
# Using Windows PowerShell for sound playback instead of playsound
import threading
import random
import json

# Set up the working directory and file paths
p = Path(os.path.abspath(__file__)).parent
w = 'w'
def play_sound(filename):
    return
    sound_path = os.path.join(p, f"sounds/{filename}")
    subprocess.Popen(f'powershell -c (New-Object Media.SoundPlayer "{sound_path}").PlaySync();', shell=True)
class Wiadom(object):
    def __init__(self):
        self.latest_response = None
    
    @cherrypy.expose
    def index(self):
        with open(os.path.join(p, "index.html"), encoding='utf-8') as i:
            return i.read()
    
    @cherrypy.expose
    def wiadom(self, msg='', picture='random', sound='random'):
        wiadomWindowFilePath = os.path.join(p, 'wiadomWindow.py')
        speakFilePath = os.path.join(p, 'speak.py')
        picturesPath = p
        
        # Handle picture selection
        if picture == 'random':
            selected_picture = 'random'
        else:
            selected_picture = picture
            
        # Handle sound selection
        if sound == 'random':
            selected_sound = random.choice(['wiadomosc_od_twojego_doradcy.wav', 'wiadomosc_od_szczura.wav'])
        else:
            selected_sound = sound
            
        subprocess.Popen(f'python "{wiadomWindowFilePath}" "{msg}" "{picturesPath}" "{selected_picture}"')
        play_sound(selected_sound)
      
        sleep(1.2)
        if 'obiad' in msg: 
            play_sound("moze_bys_cos_przekasil_sir.wav")
        subprocess.Popen(f'python{w} "{speakFilePath}" "{msg}"')
        
        # Log the message
        self.log_message("MESSAGE", msg, f"Picture: {selected_picture}, Sound: {selected_sound}")
        
        return "ok"
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def response(self):
        if cherrypy.request.method == 'POST':
            input_json = cherrypy.request.json
            self.latest_response = input_json.get('response')
            
            # Log the brother's response
            response_text = "👌 OK HAND" if self.latest_response == 'ok' else "🚫 NOT OK HAND"
            self.log_message("RESPONSE", response_text)
            
            return "ok"
        return "method not allowed"
    
    @cherrypy.expose
    def get_chat_history(self):
        log_file = os.path.join(p, 'chat_history.txt')
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return ""
        except Exception as e:
            return f"Error reading chat history: {e}"
    
    @cherrypy.expose
    def clear_chat_history(self):
        if cherrypy.request.method == 'POST':
            log_file = os.path.join(p, 'chat_history.txt')
            try:
                if os.path.exists(log_file):
                    os.remove(log_file)
                return "Chat history cleared successfully"
            except Exception as e:
                return f"Error clearing chat history: {e}"
        return "method not allowed"
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_response(self):
        response = self.latest_response
        self.latest_response = None  # Clear after reading
        return {"response": response}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_pictures(self):
        import glob
        pictures = []
        for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif']:
            pictures.extend([os.path.basename(f) for f in glob.glob(os.path.join(p, ext))])
        return {"pictures": pictures}
    
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def get_sounds(self):
        import glob
        sounds_dir = os.path.join(p, 'sounds')
        sounds = []
        if os.path.exists(sounds_dir):
            for ext in ['*.wav', '*.mp3']:
                sounds.extend([os.path.basename(f) for f in glob.glob(os.path.join(sounds_dir, ext))])
        return {"sounds": sounds}
    
    @cherrypy.expose
    def upload_file(self, file_upload=None, auto_open='false'):
        if file_upload is None or not hasattr(file_upload, 'filename'):
            return "No file uploaded"
        
        # Get Downloads folder path
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        # Save the uploaded file
        file_path = os.path.join(downloads_path, file_upload.filename)
        
        # Handle duplicate filenames
        counter = 1
        original_path = file_path
        while os.path.exists(file_path):
            name, ext = os.path.splitext(original_path)
            file_path = f"{name}_{counter}{ext}"
            counter += 1
        
        # Write the file
        with open(file_path, 'wb') as f:
            while True:
                data = file_upload.file.read(8192)
                if not data:
                    break
                f.write(data)
        
        # Check if auto-open is requested
        should_auto_open = auto_open.lower() == 'true'
        
        if should_auto_open:
            # Auto-open the file without showing popup
            try:
                os.startfile(file_path)
                # Still play a sound to notify
                play_sound(random.choice(['wiadomosc_od_twojego_doradcy.wav', 'wiadomosc_od_szczura.wav']))
            except Exception as e:
                print(f"Failed to auto-open file: {e}")
                # If auto-open fails, show popup as fallback
                wiadomWindowFilePath = os.path.join(p, 'wiadomWindow.py')
                picturesPath = p
                message = f"📁 File received: {file_upload.filename}"
                subprocess.Popen(f'pythonw "{wiadomWindowFilePath}" "{message}" "{picturesPath}" "random"')
                play_sound(random.choice(['wiadomosc_od_twojego_doradcy.wav', 'wiadomosc_od_szczura.wav']))
        else:
            # Show popup notification as usual
            wiadomWindowFilePath = os.path.join(p, 'wiadomWindow.py')
            picturesPath = p
            message = f"📁 File received: {file_upload.filename}"
            subprocess.Popen(f'pythonw "{wiadomWindowFilePath}" "{message}" "{picturesPath}" "random"')
            play_sound(random.choice(['wiadomosc_od_twojego_doradcy.wav', 'wiadomosc_od_szczura.wav']))
        
        # Log the file upload
        self.log_message("FILE", file_upload.filename, f"Auto-open: {should_auto_open}")
        
        return f"File uploaded successfully: {os.path.basename(file_path)}"
    
    @cherrypy.expose
    def update_system(self):
        import threading
        
        def do_update():
            import time
            time.sleep(2)  # Give time for response to be sent
            
            # Run git pull first
            try:
                result = subprocess.run(['git', 'pull', 'origin', 'master'], 
                                      cwd=p, capture_output=True, text=True)
                print(f"Git pull result: {result.stdout}")
                if result.stderr:
                    print(f"Git pull errors: {result.stderr}")
            except Exception as e:
                print(f"Git pull failed: {e}")
            
            # Create a batch file to restart the application
            restart_script = os.path.join(p, 'restart_wiadom.bat')
            with open(restart_script, 'w') as f:
                f.write('@echo off\n')
                f.write('timeout /t 3 /nobreak >nul\n')  # Wait 3 seconds
                f.write(f'cd /d "{p}"\n')
                f.write('pythonw wiadom.py\n')
                f.write('del "%~f0"\n')  # Delete the batch file after running
            
            # Start the restart script
            subprocess.Popen([restart_script], shell=True)
            
            # Stop the server
            cherrypy.engine.exit()
        
        # Start update in background thread
        update_thread = threading.Thread(target=do_update, daemon=True)
        update_thread.start()
        
        return "System update initiated! Restarting..."
    
    @cherrypy.expose
    def sticky_note(self, note_text='', note_color='yellow'):
        if not note_text.strip():
            return "No note text provided"
        
        # Create sticky note window
        wiadomWindowFilePath = os.path.join(p, 'wiadomWindow.py')
        picturesPath = p
        message = f"📝 Sticky Note: {note_text}"
        
        subprocess.Popen(f'python "{wiadomWindowFilePath}" "{message}" "{picturesPath}" "random" "{note_color}"')
        play_sound(random.choice(['wiadomosc_od_twojego_doradcy.wav', 'wiadomosc_od_szczura.wav']))
        
        # Log the sticky note
        self.log_message("STICKY_NOTE", note_text, note_color)
        
        return "Sticky note sent!"
    
    def log_message(self, msg_type, content, extra_data=""):
        import datetime
        log_file = os.path.join(p, 'chat_history.txt')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(log_file, 'a', encoding='utf-8') as f:
            if msg_type == "MESSAGE":
                f.write(f"[{timestamp}] MESSAGE: {content} | Response: {extra_data}\n")
            elif msg_type == "FILE":
                f.write(f"[{timestamp}] FILE: {content} | Auto-open: {extra_data}\n")
            elif msg_type == "STICKY_NOTE":
                f.write(f"[{timestamp}] STICKY_NOTE: {content} | Color: {extra_data}\n")
            elif msg_type == "RESPONSE":
                f.write(f"[{timestamp}] BROTHER_RESPONSE: {content}\n")

# Function to run on a separate thread every 5 hours
def periodic_task1():
    while True:
        sleep(5 * 60 * 60)  # 5 hours in seconds
        play_sound("grasz_juz_od_dluzszego_czasu_sir.wav")
def periodic_task2():
    while True:
        sleep(60*60)
        current_hour = datetime.now().hour
        if current_hour >= 23:
            play_sound("pozno_juz_sir.wav")
# Start the periodic task in a background thread
thread = threading.Thread(target=periodic_task1, daemon=True)
thread.start()
thread = threading.Thread(target=periodic_task2, daemon=True)
thread.start()


# Start CherryPy server
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.server.socket_port = 8080
cherrypy.quickstart(Wiadom())
