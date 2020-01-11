from model.audio_manager import AudioManager
from model.survey_manager import SurveyManager
from view.main_view import MainView
import numpy


class SyncController:
    """
    The glue between the view and the model. Provides functionality
    for the view by modifying the model.
    """

    def __init__(self, audio_model: AudioManager, survey_model: SurveyManager, view: MainView):
        self.audio_model = audio_model
        self.survey_model = survey_model
        self.view = view

    def process_survey_load_event(self, path) -> None:
        """
        Takes a path and loads it as a survey.

        :return: nothing
        """
        self.survey_model.set_path(path)
        self.survey_model.process_survey()
        self.view.update_survey_text(self.survey_model.get_survey_results())

    def process_start_event(self) -> None:
        """
        Starts recording the mic.

        :return: nothing
        """
        self.audio_model.start_recording()
        self.view.update_start_enabled(False)
        self.view.update_stop_enabled(True)
        self.view.animate_plots()

    def process_stop_event(self) -> None:
        """
        Stops recording from the mic.

        :return: nothing
        """
        self.audio_model.stop_recording()
        self.audio_model.dump_recording()
        self.view.update_start_enabled(True)
        self.view.update_stop_enabled(False)

    def process_audio_animation(self, i):
        """
        Animates the audio plot the audio plot.

        :param i: the index of the current frame
        :return: an iterable of items to be cleared
        """
        self.view.audio_plot.clear()
        decoded = numpy.fromstring(b''.join(self.audio_model.data), numpy.int16)
        self.view.curve, = self.view.audio_plot.plot(decoded)
        self.view.canvas.draw()
        return self.view.curve,
