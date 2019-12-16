from controller.sync_controller import SyncController
from model.audio_manager import AudioManager
from view.main_view import MainView
import tkinter

root = tkinter.Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

model = AudioManager()
view = MainView(root)
controller = SyncController(model, view)
view.register_observer(controller)

# TODO add audio visualization
# TODO add timer which tracks recording time
# TODO incorporate dongle recording

root.mainloop()
