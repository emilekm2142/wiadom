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
from playsound import playsound
import threading

# Set up the working directory and file paths
p = Path(os.path.abspath(__file__)).parent
w = 'w'
def play_sound(filename):
    sound_path = os.path.join(p, f"sounds/{filename}")
    subprocess.Popen(f'powershell -c (New-Object Media.SoundPlayer "{sound_path}").PlaySync();', shell=True)
class Wiadom(object):
    @cherrypy.expose
    def index(self):
        with open(os.path.join(p, "index.html")) as i:
            return i.read()
    
    @cherrypy.expose
    def wiadom(self, msg=''):
        wiadomWindowFilePath = os.path.join(p, 'wiadomWindow.py')
        speakFilePath = os.path.join(p, 'speak.py')
        picturesPath = p
        subprocess.Popen(f'python{w} "{wiadomWindowFilePath}" "{msg}" "{picturesPath}"')
        play_sound(random.choice['wiadomosc_od_twojego_doradcy.wav', 'wiadomosc_od_szczura.wav'])
      
        sleep(1.2)
        if 'obiad' in msg: 
            play_sound("moze_bys_cos_przekasil_sir.wav")
        subprocess.Popen(f'python{w} "{speakFilePath}" "{msg}"')
        return "ok"

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
thread = threading.Thread(target=periodic_task, daemon=True)
thread.start()


# Start CherryPy server
cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(Wiadom())
