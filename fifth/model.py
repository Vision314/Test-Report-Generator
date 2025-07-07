import pandas as pd

class Model:
    def __init__(self, report_path: str = None) -> None:
        # base path for report project
        self.report_path = report_path

        # main data containers
        self.cover_page_data = {}
        self.test_description = {}
        self.test_selections = {}