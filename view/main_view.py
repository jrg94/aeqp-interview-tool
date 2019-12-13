import tkinter as tk


class MainView(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        # Initialize fields
        self.controller = None

        # Insert widgets
        self.start_button = tk.Button(self, text="Start", command=self.start_action)
        self.start_button.pack()

        self.stop_button = tk.Button(self, text="Stop", command=self.stop_action, state=tk.DISABLED)
        self.stop_button.pack()

        # Pack window
        self.pack()

    @staticmethod
    def _update_button_enabled(button: tk.Button, state: bool):
        if state:
            button.config(state=tk.NORMAL)
        else:
            button.config(state=tk.DISABLED)

    def update_start_enabled(self, state: bool):
        MainView._update_button_enabled(self.start_button, state)

    def update_stop_enabled(self, state: bool):
        MainView._update_button_enabled(self.stop_button, state)

    def register_observer(self, controller):
        self.controller = controller

    def start_action(self):
        self.controller.process_start_event()

    def stop_action(self):
        self.controller.process_stop_event()
