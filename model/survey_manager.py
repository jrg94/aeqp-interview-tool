import csv


class SurveyManager:
    def __init__(self):
        self.survey_results = list()
        self.survey_path = None

    def set_path(self, path):
        self.survey_path = path

    def process_survey(self):
        if self.survey_path:
            with open(self.survey_path) as my_data:
                self.survey_results = list(csv.DictReader(my_data))

    def get_survey_results(self):
        return self.survey_results
