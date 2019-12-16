from model.audio_manager import AudioManager
from view.main_view import MainView
import numpy


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
        self.view.animate_plots()

    def process_stop_event(self) -> None:
        """
        Stops recording from the mic.

        :return: nothing
        """
        self.model.stop_recording()
        self.model.dump_recording()
        self.view.update_start_enabled(True)
        self.view.update_stop_enabled(False)

    def process_audio_animation(self, i):
        """
        Animates the audio plot the audio plot.

        :param i: the index of the current frame
        :return: an iterable of items to be cleared
        """
        self.view.audio_plot.clear()
        decoded = numpy.fromstring(b''.join(self.model.data), numpy.int16)
        self.view.curve, = self.view.audio_plot.plot(decoded)
        self.view.canvas.draw()
        return self.view.curve,
