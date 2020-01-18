from model.audio_manager import AudioManager
from model.eda_manager import EDAManager
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

    def __init__(self, audio_model: AudioManager, survey_model: SurveyManager, eda_model: EDAManager, view: MainView):
        self.audio_model = audio_model
        self.survey_model = survey_model
        self.eda_model = eda_model
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

    def process_participant_selection_event(self, name: str) -> None:
        """
        Processes the participant selection by updating the survey
        text with our user's survey results. Survey results are pretty
        printed.

        :param name: the name of the participant in the format of the _participant_name method
        :return: nothing
        """
        last_and_first = name.replace(" ", "").split(",")
        survey_results = self.survey_model.get_survey_results()
        participant_results = next(
            item for item in survey_results
            if item.get(SyncController.LAST_NAME_HEADER) == last_and_first[0]
            and item.get(SyncController.FIRST_NAME_HEADER) == last_and_first[1]
        )
        sub_scales_to_segments = {}
        sub_scales = {participant_results[key] for key in participant_results if "subscale" in key}
        for sub_scale in sub_scales:
            sub_scale_questions = [
                "_".join(key.split("_")[1:3])
                for key, value in participant_results.items()
                if sub_scale == value
            ]
            sub_scales_to_segments[sub_scale] = {
                "before": [x for x in sub_scale_questions if "before" in x],
                "during": [x for x in sub_scale_questions if "during" in x],
                "after": [x for x in sub_scale_questions if "after" in x]
            }
        self.view.survey_view.update_survey_text(participant_results, sub_scales_to_segments)
        self.view.update_start_enabled(True)

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
        self.eda_model.start_recording()
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
        self.eda_model.stop_recording()
        self.view.update_start_enabled(True)
        self.view.update_stop_enabled(False)

    def process_audio_animation(self, i):
        """
        Animates the audio plot the audio plot.

        :param i: the index of the current frame
        :return: an iterable of items to be cleared
        """
        self.view.audio_plot.plot.clear()
        decoded = numpy.fromstring(b''.join(self.audio_model.data), numpy.int16)
        self.view.curve, = self.view.audio_plot.plot.plot(decoded)
        self.view.audio_plot.canvas.draw()
        return self.view.curve,
