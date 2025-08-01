import pandas as pd
import pickle

class CoverPage():
    def __init__(self):
        self.equipment_used = pd.DataFrame(columns=[
                            'Equipment Type', 
                            'Manufacturer',
                            'Model',
                            'Description',
                            'S/N',
                            'Last Calibrated',
                            'Calibration Due'])


        self.general_specifications = {}
        self.testing_and_review = {'Tested By': '',
                                   'Reviewed By': '',
                                   'Reviewed Date': ''}


    def add_equipment(self, equipment):
        new_row = pd.DataFrame([equipment])
        self.equipment_used = pd.concat([self.equipment_used, new_row], ignore_index=True)
    
    def add_general_specification(self, name, value):
        gs = {name: value}
        self.general_specifications[name] = value