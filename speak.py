import pyttsx3,sys
def speak(msg):
    engine = pyttsx3.init()
    engine.say(msg)
    engine.runAndWait()
speak(sys.argv[1])