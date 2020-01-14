import csv
import tkinter as tk
from contextlib import ExitStack
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_paths = filedialog.askopenfilenames()

with ExitStack() as stack:
    files = [stack.enter_context(open(path)) for path in file_paths]
    for file in files:
        csv_mapping_list = list(csv.DictReader(file))
