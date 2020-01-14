import tkinter as tk
from tkinter import filedialog
import csv
from contextlib import ExitStack

root = tk.Tk()
root.withdraw()

file_paths = filedialog.askopenfilenames()

with ExitStack() as stack:
    files = [stack.enter_context(open(fname)) for fname in file_paths]
    for file in files:
        csv_mapping_list = list(csv.DictReader(file))
