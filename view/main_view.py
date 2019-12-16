import tkinter as tk


class MainView(tk.Frame):
    """
    The main application view. In this case, we've defined a window
    which allows us to start an stop recording from the PC mic.
    """

    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        # Initialize fields
        self.controller = None

        # Insert widgets
        self.start_button = tk.Button(self, text="Start", command=self.start_action)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_action, state=tk.DISABLED)

        # Arrange elements
        self.start_button.grid(row=0, column=0, sticky="nsew")
        self.stop_button.grid(row=0, column=1, sticky="nsew")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Pack window
        self.grid(row=0, column=0, sticky="nsew")

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
