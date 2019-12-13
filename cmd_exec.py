from model.audio_manager import AudioManager
import time
from view.main_view import MainView
import tkinter

root = tkinter.Tk()
app = MainView(root)
root.mainloop()

audio = AudioManager()
audio.start_recording()
time.sleep(5)
audio.stop_recording()
audio.close_manager()
audio.dump_recording()
