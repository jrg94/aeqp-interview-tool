import csv
import tkinter as tk
from contextlib import ExitStack
from tkinter import filedialog
import os

SEGMENTS = ("before", "during", "after")
FIRST_NAME = "RecipientFirstName"
LAST_NAME = "RecipientLastName"

EMOTIONS_TO_PROMPTS = {
    "before": ["enjoyment", "enjoyment", "enjoyment", "enjoyment", "enjoyment", "hope", "hope", "hope", "hope", "hope",
               "hope", "pride", "anger", "anger", "anxiety", "anxiety", "anxiety", "anxiety", "anxiety", "shame",
               "hopelessness", "hopelessness", "hopelessness", "hopelessness", "hopelessness"],
    "during": ["enjoyment", "enjoyment", "enjoyment", "hope", "hope", "pride", "pride", "anger", "anger", "anxiety",
               "anxiety", "anxiety", "anxiety", "anxiety", "anxiety", "anxiety", "shame", "shame", "shame", "shame",
               "shame", "hopelessness", "hopelessness", "hopelessness", "hopelessness", "hopelessness", "hopelessness"],
    "after": ["enjoyment", "enjoyment", "pride", "pride", "pride", "pride", "pride", "pride", "pride", "anger", "anger",
              "anger", "anger", "anger", "anger", "shame", "shame", "shame", "shame", "relief", "relief", "relief",
              "relief", "relief", "relief"]
}


def get_survey_segment(file_name: str):
    """
    Gets the segment of a survey file (before, during, after)

    :param file_name: the name of the file
    :return: the segment as a string
    """
    search_string = file_name.lower().split(os.sep)[-1]
    for segment in SEGMENTS:
        if segment in search_string:
            return segment
    return None


def load_surveys(file_paths: list) -> dict:
    """
    A helper function which loads a set of surveys from a list of file paths.

    :param file_paths: a list of CSV file paths
    :return: a dict of surveys (one for each file)
    """
    surveys = {}
    with ExitStack() as stack:
        files = [stack.enter_context(open(path)) for path in file_paths]
        for file in files:
            survey = list(csv.DictReader(file))
            surveys[get_survey_segment(file.name)] = {
                "survey": survey,
                "metadata1": survey.pop(0),
                "metadata2": survey.pop(0)
            }
    return surveys


def get_student_responses(surveys: dict, index: int):
    student_responses = {
        FIRST_NAME: surveys[SEGMENTS[0]]["survey"][index][FIRST_NAME],
        LAST_NAME: surveys[SEGMENTS[0]]["survey"][index][LAST_NAME]
    }
    for segment in SEGMENTS:
        metadata = surveys[segment]["metadata1"]
        for participant in surveys[segment]["survey"]:
            if participant[FIRST_NAME] == student_responses[FIRST_NAME] \
                    and participant[LAST_NAME] == student_responses[LAST_NAME]:
                load_questions(student_responses, participant, segment, metadata)
    return student_responses


def load_questions(responses: dict, participant: dict, segment: str, metadata: dict) -> None:
    """
    Loads the questions into the survey alongside their description and subscale.

    :param responses: the final list of responses
    :param participant: the current participant
    :param segment: the current segment (before, during, after)
    :param metadata: the metadata for this segment
    :return: nothing
    """
    for i in range(len(EMOTIONS_TO_PROMPTS[segment])):
        question_base = f'Q1_{i}'
        if question_base in participant:
            question = f'{question_base}_{segment}'
            responses[question] = participant[question_base]
            description = f'{question}_description'
            responses[description] = metadata[question_base].split("-")[-1].strip()
            sub_scale = f'{question}_subscale'
            responses[sub_scale] = EMOTIONS_TO_PROMPTS[segment][i]


def main():
    root = tk.Tk()
    root.withdraw()

    file_paths = filedialog.askopenfilenames()
    surveys = load_surveys(file_paths)
    master_survey = []
    for i in range(len(surveys[SEGMENTS[0]]["survey"])):
        master_survey.append(get_student_responses(surveys, i))
    print(master_survey)


main()
