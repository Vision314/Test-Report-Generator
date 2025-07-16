import pandas as pd
import pickle

class CoverPage():
    def __init__(self):
        self.equipment_used = self._init_equipment_used()
        self.general_specifications = self._init_general_specifications()
        self.testing_and_review = self._init_testing_and_review()

    def _init_equipment_used(self):
        return pd.DataFrame(columns=[
                            'Equipment Type', 
                            'Manufacturer',
                            'Model',
                            'Description',
                            'S/N',
                            'Last Calibrated',
                            'Calibration Due'])

    def _init_general_specifications(self):
        pass

    def _init_testing_and_review(self):
        pass

    def add_equipment(self, eq):
        new_row = pd.DataFrame([eq])
        self.equipment_used = pd.concat([self.equipment_used, new_row], ignore_index=True)
    
def pickle_object(obj, filepath):
    # filepath = 'cover_page.pickle'
    with open(filepath, 'wb') as file:
        pickle.dump(obj, file)