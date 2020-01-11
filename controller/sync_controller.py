from model.audio_manager import AudioManager
from model.survey_manager import SurveyManager
from view.main_view import MainView
import numpy


class SyncController:
    """
    The glue between the view and the model. Provides functionality
    for the view by modifying the model.
    """

    FIRST_NAME_HEADER = "RecipientFirstName"
    LAST_NAME_HEADER = "RecipientLastName"

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
        survey_results = self.survey_model.get_survey_results()
        participants = [SyncController._participant_name(item) for item in survey_results]
        participants.sort()
        self.view.update_option_menu(participants)

    def process_participant_selection_event(self, name: str):
        last_and_first = name.replace(" ", "").split(",")
        survey_results = self.survey_model.get_survey_results()
        participant_results = next(
            item for item in survey_results
            if item.get(SyncController.LAST_NAME_HEADER) == last_and_first[0]
            and item.get(SyncController.FIRST_NAME_HEADER) == last_and_first[1]
        )
        self.view.update_survey_text(str(participant_results))

    @staticmethod
    def _participant_name(item: dict):
        """
        A helper method which generates a participant's name from a survey response.

        :param item: a survey response as a dictionary
        :return: a string in the form "LAST_NAME, FIRST_NAME"
        """
        return f'{item.get(SyncController.LAST_NAME_HEADER)}, {item.get(SyncController.FIRST_NAME_HEADER)}'

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
