from model.audio_manager import AudioManager
from view.main_view import MainView


class SyncController:
    """
    The glue between the view and the model. Provides functionality
    for the view by modifying the model.
    """

    def __init__(self, model: AudioManager, view: MainView):
        self.model = model
        self.view = view

    def process_start_event(self) -> None:
        """
        Starts recording the mic.

        :return: nothing
        """
        self.model.start_recording()
        self.view.update_start_enabled(False)
        self.view.update_stop_enabled(True)

    def process_stop_event(self) -> None:
        """
        Stops recording from the mic.

        :return: nothing
        """
        self.model.stop_recording()
        self.model.dump_recording()
        self.view.update_start_enabled(True)
        self.view.update_stop_enabled(False)
