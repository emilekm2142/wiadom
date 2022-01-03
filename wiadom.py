import tkinter as tk
from tkinter import ttk
from tkinter import *
import pyttsx3
import cherrypy
import sys,subprocess
import os
from pathlib import Path
p = Path(os.path.abspath(__file__)).parent
w=''
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
        subprocess.Popen(f'python{w} "{speakFilePath}" "{msg}"')

        return "ok"


cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(Wiadom())
