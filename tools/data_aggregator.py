import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_paths = filedialog.askopenfilenames()
