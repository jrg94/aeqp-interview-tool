import tkinter as tk


class MainView(tk.Frame):
    def __init__(self, root, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)

        # Initialize fields
        self.controller = None

        # Insert widgets
        start_button = tk.Button(self, text="Start", command=self.start_action)
        start_button.pack()

        # Pack window
        self.pack()

    def register_observer(self, controller):
        self.controller = controller

    def start_action(self):
        self.controller.processStartEvent()
