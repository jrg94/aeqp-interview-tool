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

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        # Initialize fields
        self.controller = None
        self.ani = None

        # Insert widgets
        self.start_button = tk.Button(self, text="Start", command=self.start_action)
        self.stop_button = tk.Button(self, text="Stop", command=self.stop_action, state=tk.DISABLED)
        self.file_select_button = tk.Button(self, text="Select Survey File", command=self.load_survey_event)
        self.survey_text = tk.Text(self, state=tk.DISABLED)

        self.plots = Figure(figsize=(5, 4), dpi=100)
        self.audio_plot = self.plots.add_subplot(111)
        self.curve, = self.audio_plot.plot([])
        self.canvas = FigureCanvasTkAgg(self.plots, master=self)

        # Arrange elements
        self.start_button.grid(row=1, column=0, sticky="nsew")
        self.stop_button.grid(row=1, column=1, sticky="nsew")
        self.file_select_button.grid(row=1, column=2, sticky="nsew")
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew", columnspan=2)
        self.survey_text.grid(row=0, column=2, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

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

    def update_survey_text(self, text) -> None:
        """
        Updates the survey text area with the survey results.

        :param text: the survey results in a readable format
        :return: nothing
        """
        self.survey_text.config(state=tk.NORMAL)
        self.survey_text.insert(tk.END, text)
        self.survey_text.config(state=tk.DISABLED)

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
            self.plots,
            self.controller.process_audio_animation,
            interval=100,
            blit=True
        )
