from controller.sync_controller import SyncController
from model.audio_manager import AudioManager
from model.eda_manager import EDAManager
from model.survey_manager import SurveyManager
from view.main_view import MainView
import tkinter


def main():
    root = tkinter.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    audio_model = AudioManager()
    survey_model = SurveyManager()
    eda_model = EDAManager()
    view = MainView(root)
    controller = SyncController(audio_model, survey_model, eda_model, view)
    view.register_observer(controller)

    root.mainloop()


if __name__ == '__main__':
    main()
