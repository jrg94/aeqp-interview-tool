import csv
import tkinter as tk
from contextlib import ExitStack
from tkinter import filedialog
import os


def get_names(survey_results: list) -> list:
    names = []
    for row in survey_results:
        names.append({
            "LastName": row.get("RecipientLastName"),
            "FirstName": row.get("RecipientFirstName"),

        })
    return names


def get_survey_segment(file_name: str):
    search_string = file_name.lower().split(os.sep)[-1]
    segments = ("before", "during", "after")
    for segment in segments:
        if segment in search_string:
            return segment
    return None


def load_surveys(file_paths):
    surveys = []
    with ExitStack() as stack:
        files = [stack.enter_context(open(path)) for path in file_paths]
        for file in files:
            surveys.append(list(csv.DictReader(file)))
    return surveys


def main():
    root = tk.Tk()
    root.withdraw()

    file_paths = filedialog.askopenfilenames()
    surveys = load_surveys(file_paths)
    master_survey = []

    # meta_data_1 = csv_mapping_list.pop(0)
    # meta_data_2 = csv_mapping_list.pop(0)
    # names = get_names(csv_mapping_list)
    # segment = get_survey_segment(file.name)


main()
