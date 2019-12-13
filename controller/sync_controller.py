from model.audio_manager import AudioManager
from view.main_view import MainView


class SyncController:
    def __init__(self, model: AudioManager, view: MainView):
        self.model = model
        self.view = view

    def process_start_event(self):
        self.model.start_recording()
        self.view.update_start_enabled(False)
        self.view.update_stop_enabled(True)

    def process_stop_event(self):
        self.model.stop_recording()
        self.model.dump_recording()
        self.view.update_start_enabled(True)
        self.view.update_stop_enabled(False)
