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
            
        subprocess.Popen(f'python{w} "{wiadomWindowFilePath}" "{msg}" "{picturesPath}" "{selected_picture}"')
        play_sound(selected_sound)
      
        sleep(1.2)
        if 'obiad' in msg: 
            play_sound("moze_bys_cos_przekasil_sir.wav")
        subprocess.Popen(f'python{w} "{speakFilePath}" "{msg}"')
        return "ok"
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def response(self):
        if cherrypy.request.method == 'POST':
            input_json = cherrypy.request.json
            self.latest_response = input_json.get('response')
            return "ok"
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
