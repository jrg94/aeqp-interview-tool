import tkinter as tk
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation


class MainView(tk.Frame):
    """
    The main application view. In this case, we've defined a window
    which allows us to start an stop recording from the PC mic.
    """

    PARTICIPANT_STRING = "Select a Participant"

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        # Initialize fields
        self.controller = None
        self.ani = None
        self.option = tk.StringVar(self)
        self.option.set(MainView.PARTICIPANT_STRING)
        self.option.trace("w", self.load_participant_survey)

        # Insert widgets
        self.start_button = tk.Button(self, text="Start", command=self.start_action)
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_action, state=tk.DISABLED)
        self.file_select_button = tk.Button(self, text="Select Survey File", command=self.load_survey_event)
        self.survey_view = SurveyView(self)
        self.audio_plot = PlotView(self, "Audio Plot", "Time", "Amplitude")
        self.eda_plot = PlotView(self, "EDA Plot", "Time", "Galvanic Skin Response")
        self.participant_menu = tk.OptionMenu(self, self.option, MainView.PARTICIPANT_STRING)
        self.participant_menu.config(state=tk.DISABLED)

        # Arrange elements
        self.file_select_button.grid(row=0, column=0, sticky="nsew")
        self.participant_menu.grid(row=0, column=1, sticky="nsew")
        self.start_button.grid(row=0, column=2, sticky="nsew")
        self.stop_button.grid(row=0, column=3, sticky="nsew")
        self.survey_view.grid(row=1, column=0, sticky="nsew", columnspan=4)
        self.audio_plot.grid(row=2, column=0, sticky="nsew", columnspan=2)
        self.eda_plot.grid(row=2, column=2, sticky="nsew", columnspan=2)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # Pack window
        self.grid(row=0, column=0, sticky="nsew")

    def load_survey_event(self) -> None:
        """
        Prompts the user to select a file before passing off the
        path to the controller.

        :return: nothing
        """
        path = filedialog.askopenfilename()
        self.controller.process_survey_load_event(path)

    def load_participant_survey(self, *_) -> None:
        """
        Loads the participant survey based on updates to the option menu.

        :param _: unused arguments that are passed by the trace function
        :return: nothing
        """
        self.controller.process_participant_selection_event(str(self.option.get()))

    def update_option_menu(self, participants: list) -> None:
        """
        Updates the option menu to include new participants.

        :param participants: a list of participants
        :return: nothing
        """
        menu = self.participant_menu["menu"]
        menu.delete(0, "end")
        for participant in participants:
            menu.add_command(
                label=participant,
                command=lambda value=participant: self.option.set(value)
            )
        self.participant_menu.config(state=tk.NORMAL)

    @staticmethod
    def _update_button_enabled(button: tk.Button, state: bool) -> None:
        """
        Updates the enabled state of a button based on inputs.

        :param button: the input button
        :param state: the new state of the button (True for enabled)
        :return: nothing
        """
        if state:
            button.config(state=tk.NORMAL)
        else:
            button.config(state=tk.DISABLED)

    def update_start_enabled(self, state: bool) -> None:
        """
        Updates the enabled state of the start button.

        :param state: the new state of the start button (True for enabled)
        """
        MainView._update_button_enabled(self.start_button, state)

    def update_stop_enabled(self, state: bool) -> None:
        """
        Updates the enabled state of the stop button.

        :param state: the new state of the stop button (True for enabled)
        """
        MainView._update_button_enabled(self.stop_button, state)

    def register_observer(self, controller) -> None:
        """
        Registers the observer for this view.

        :param controller: the controller for this view
        """
        self.controller = controller

    def start_action(self) -> None:
        """
        Executes the start action.

        :return: nothing
        """
        self.controller.process_start_event()

    def stop_action(self) -> None:
        """
        Executes the stop action.

        :return: nothing
        """
        self.controller.process_stop_event()

    def animate_plots(self) -> None:
        """
        Sets up the animation after we get our controller reference.

        :return: nothing
        """
        self.ani = animation.FuncAnimation(
            self.audio_plot.plots,
            self.controller.process_audio_animation,
            interval=100,
            blit=True
        )


class SurveyView(tk.Frame):
    """
    A custom survey element which can be reused and contained.
    """

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

    def update_survey_text(self, survey, subscales_to_segments: dict) -> None:
        """
        Updates the survey text area with the survey results.

        :param survey: the survey results
        :param subscales_to_segments: a mapping of subscales to segments
        :return: nothing
        """
        row = 0
        for subscale, segments in subscales_to_segments.items():
            questions = [questions for segment, questions in segments.items()]
            table = TableView(self, subscale, questions)
            table.grid(row=row, column=0, sticky='nsew')


class TableView(tk.Frame):

    def __init__(self, root, title, grid, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        title_text = tk.Text(self)
        title_text.insert(tk.END, title)
        title_text.config(state=tk.DISABLED)
        title_text.grid(row=0, column=0, columnspan=len(grid))
        for i, column in enumerate(grid):
            for j, row in enumerate(column):
                item = tk.Text(self)
                item.grid(row=j+1, column=i, sticky="nsew")
                item.insert(tk.END, row)
                item.config(state=tk.DISABLED)
                self.rowconfigure(i, weight=1)
                self.columnconfigure(j, weight=1)


class PlotView(tk.Frame):

    def __init__(self, root, title, x_label, y_label, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        self.plots = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.plots.add_subplot(111)
        self.curve, = self.plot.plot([])
        self.canvas = FigureCanvasTkAgg(self.plots, master=self)

        self.plots.suptitle(title)
        self.plot.set_xlabel(x_label)
        self.plot.set_ylabel(y_label)

        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
