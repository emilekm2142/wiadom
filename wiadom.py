import tkinter as tk
from tkinter import ttk
from tkinter import *
import pyttsx3
import cherrypy
import sys,subprocess
class Wiadom(object):
    @cherrypy.expose
    def wiadom(self,msg=''):
        subprocess.Popen(f'python wiadomWindow.py "{msg}"')
        subprocess.Popen(f'python speak.py "{msg}"')

        return "ok"


cherrypy.server.socket_host = '0.0.0.0'
cherrypy.quickstart(Wiadom())
