import tkinter as tk
from tkinter import ttk
from tkinter import *
from time import sleep
import pyttsx3
import cherrypy
import sys,subprocess
import os
from pathlib import Path
from playsound import  playsound
p = Path(os.path.abspath(__file__)).parent
w='w'
class Wiadom(object):
    @cherrypy.expose
    def index(self):
        with open(os.path.join(p,"index.html")) as i:
            return i.read()
    @cherrypy.expose
    def wiadom(self,msg=''):
        wiadomWindowFilePath = os.path.join(p, 'wiadomWindow.py')
        speakFilePath = os.path.join(p, 'speak.py')
        picturesPath = p
        subprocess.Popen(f'python{w} "{wiadomWindowFilePath}" "{msg}" "{picturesPath}"')
        sound_path = os.path.join(p,"sounds/wiadomosc_od_szczura.wav")
        subprocess.Popen(f'powershell -c (New-Object Media.SoundPlayer "{sound_path}").PlaySync();')
        sleep(1.2)
        subprocess.Popen(f'python{w} "{speakFilePath}" "{msg}"')

        return "ok"


cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(Wiadom())