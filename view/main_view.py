import statistics
import tkinter as tk
from collections import OrderedDict
from tkinter import filedialog

import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


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
        self.ani_audio = None
        self.ani_eda = None
        self.option = tk.StringVar(self)
        self.option.set(MainView.PARTICIPANT_STRING)
        self.option.trace("w", self.load_participant_survey)

        # Insert widgets
        self.start_button = tk.Button(self, text="Start", command=self.start_action, state=tk.DISABLED)
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_action, state=tk.DISABLED)
        self.file_select_button = tk.Button(self, text="Select Survey File", command=self.load_survey_event)
        self.survey_canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.survey_canvas.yview)
        self.survey_view = SurveyView(self.survey_canvas)
        self.audio_plot = PlotView(self, "Audio Plot", "Time", "Amplitude")
        self.eda_plot = PlotView(self, "EDA Plot", "Time", "Galvanic Skin Response")
        self.participant_menu = tk.OptionMenu(self, self.option, MainView.PARTICIPANT_STRING)
        self.participant_menu.config(state=tk.DISABLED)

        # Arrange elements
        self.file_select_button.grid(row=0, column=0, sticky="nsew")
        self.participant_menu.grid(row=0, column=1, sticky="nsew")
        self.start_button.grid(row=0, column=2, sticky="nsew")
        self.stop_button.grid(row=0, column=3, sticky="nsew")
        self.survey_canvas.grid(row=1, column=0, sticky="nsew", columnspan=4)
        self.scrollbar.grid(row=1, column=4, sticky="ns")
        self.audio_plot.grid(row=2, column=0, sticky="nsew", columnspan=2)
        self.eda_plot.grid(row=2, column=2, sticky="nsew", columnspan=2)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1, minsize=500)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)

        # Setup scroll window
        self.survey_view.bind(
            "<Configure>",
            lambda e: self.survey_canvas.configure(
                scrollregion=self.survey_canvas.bbox("all")
            )
        )

        self.canvas_id = self.survey_canvas.create_window((0, 0), window=self.survey_view, anchor="n")
        self.survey_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.survey_canvas.bind(
            "<Configure>",
            lambda event: self.survey_canvas.itemconfigure(self.canvas_id, width=event.width)
        )

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
        self.ani_audio = animation.FuncAnimation(
            self.audio_plot.plots,
            self.controller.process_audio_animation,
            interval=500,
            blit=True
        )
        self.ani_eda: animation.FuncAnimation = animation.FuncAnimation(
            self.eda_plot.plots,
            self.controller.process_eda_animation,
            interval=500,
            blit=True
        )

    def get_output_file_name(self):
        participant_name = self.option.get()
        file_name = "_".join(participant_name.lower().replace(" ", "").split(","))
        return file_name


class SurveyView(tk.Frame):
    """
    A custom survey element which can be reused and contained.
    """

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

    def update_survey_text(self, survey: OrderedDict, subscales_to_segments: dict) -> None:
        """
        Updates the survey text area with the survey results.

        :param survey: the survey results
        :param subscales_to_segments: a mapping of subscales to segments
        :return: nothing
        """
        row = 0
        self.columnconfigure(0, weight=1)
        subscales = list(subscales_to_segments.keys())
        subscales.sort()
        for subscale in subscales:
            questions = [questions for segment, questions in subscales_to_segments[subscale].items()]
            table = TableView(self, subscale, questions, survey, pady=10, padx=10)
            table.grid(row=row, column=0, sticky='nsew')
            self.rowconfigure(row, weight=1)
            row += 1


class TableView(tk.Frame):

    def __init__(self, root, title: str, grid: list, survey: OrderedDict, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        title_text = tk.Label(self, text=title, pady=20, font="Verdana 16 bold")
        title_text.grid(row=0, column=0, columnspan=len(grid)*2)
        self.rowconfigure(0, weight=1)
        rows = max([len(item) for item in grid])
        for i in range(len(grid)):
            column = 2 * i
            segment = TableView.get_segment(i)
            segment_label = tk.Label(self, text=segment, pady=15, borderwidth=2, relief="solid", font="Verdana 10 bold")
            segment_label.grid(row=1, column=column, sticky="nsew")
            average = TableView.compute_average_and_median(grid[i], survey)
            average_label = tk.Label(self, text=average, pady=15, borderwidth=2, relief="solid", font="Verdana 10 bold")
            average_label.grid(row=1, column=column+1, sticky="nsew")
            self.rowconfigure(1, weight=1)
            for j in range(rows):
                row = j + 2
                self._generate_table_cell(grid, survey, row, column, i, j)

    def _generate_table_cell(self, grid: list, survey: OrderedDict, row: int, column: int, i: int, j: int):
        """
        Generates a table cell consisting of a subscale score and a subscale description.

        :param grid: a list of question lists organized by subscale (i.e. [['13_before', '14_before'], ...])
        :param survey: the survey results for a participant
        :param row: the physical row that content will appear in the table
        :param column: the physical column that content will appear in the table
        :param i: the row index of the grid
        :param j: the column index of the grid
        :return: nothing
        """
        subscale_score_label = self._create_subscale_score_label(grid, survey, i, j)
        subscale_desc_label = self._create_subscale_desc_label(grid, survey, i, j)
        subscale_score_label.grid(row=row, column=column + 1, sticky="nsew")
        subscale_desc_label.grid(row=row, column=column, sticky="nsew")
        self.rowconfigure(row, weight=1)
        self.columnconfigure(column, weight=1, minsize=150)
        self.columnconfigure(column + 1, weight=1, minsize=50)

    def _create_subscale_score_label(self, grid: list, survey: OrderedDict, i: int, j: int) -> tk.Label:
        """
        Creates a subscale score label from the grid of questions and the participant survey.

        :param grid: a list of question lists organized by subscale (i.e. [['13_before', '14_before'], ...])
        :param survey: the survey results for a participant
        :param i: the row index of the grid
        :param j: the column index of the grid
        :return: a subscale score label
        """
        subscale_score_text = "" if len(grid[i]) <= j else survey[f'Q1_{grid[i][j]}_question']
        subscale_score_label = tk.Label(
            self,
            text=subscale_score_text,
            padx=5,
            pady=15,
            borderwidth=1,
            relief="solid"
        )
        return subscale_score_label

    def _create_subscale_desc_label(self, grid: list, survey: OrderedDict, i: int, j: int) -> tk.Message:
        """
        Creates a subscale description label from the participant survey and the grid of questions.

        :param grid: a list of question lists organized by subscale (i.e. [['13_before', '14_before'], ...])
        :param survey: the survey results for a participant
        :param i: the row index of the grid
        :param j: the column index of the grid
        :return: a subscale description label
        """
        subscale_desc_text = "" if len(grid[i]) <= j else survey[f'Q1_{grid[i][j]}_description']
        subscale_desc_label = tk.Message(
            self,
            text=subscale_desc_text,
            padx=5,
            pady=10,
            anchor="w",
            borderwidth=1,
            relief="solid",
            aspect=500
        )
        return subscale_desc_label

    @staticmethod
    def get_segment(index: int) -> str:
        """
        Given an index, this method returns a survey segment (i.e. before, during, or after).

        :param index: the index of the segment
        :return: a segment
        """
        return [
            "before",
            "during",
            "after"
        ][index]

    @staticmethod
    def compute_average_and_median(column, survey) -> str:
        """
        Computes the average and median from a column of question IDs and the participant survey.

        :param column: a column of question IDs of the form [id1, id2, ..., idn] (i.e. ['13_before', '14_before'])
        :param survey: the participant survey results
        :return: a mean and median as a string (empty string if empty column)
        """
        scores = [int(survey[f'Q1_{item}_question']) for item in column]
        return "" if not scores else f'Mean: {statistics.mean(scores):.2f}\nMedian: {statistics.median(scores):.2f}'


class PlotView(tk.Frame):

    def __init__(self, root, title, x_label, y_label, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        self.title = title
        self.x_label = x_label
        self.y_label = y_label

        self.plots = Figure(figsize=(6, 4), dpi=100)
        self.plot = self.plots.add_subplot(111)
        self.curve, = self.plot.plot([])
        self.canvas = FigureCanvasTkAgg(self.plots, master=self)

        self.plots.suptitle(title)
        self.plot.set_xlabel(x_label)
        self.plot.set_ylabel(y_label)

        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def clear(self):
        self.plot.clear()

    def redraw(self):
        self.plots.suptitle(self.title)
        self.plot.set_xlabel(self.x_label)
        self.plot.set_ylabel(self.y_label)
        self.canvas.draw()
