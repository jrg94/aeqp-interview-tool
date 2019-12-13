from controller.sync_controller import SyncController
from model.audio_manager import AudioManager
from view.main_view import MainView
import tkinter

root = tkinter.Tk()

model = AudioManager()
view = MainView(root)
controller = SyncController(model, view)
view.register_observer(controller)

root.mainloop()
