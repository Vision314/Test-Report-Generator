from cover_page import *
from test_SIMPLIFIED import *
import pickle

class TestReport():
    def __init__(self, title=''):
        self.title = title
        self.cover_page = CoverPage()
        self.tests = []

        self.selected_test = None


    def add_test(self, test_category, test_name):
        new_test = Test(test_category, test_name)
        self.tests.append(new_test)
        print("A new test has been created!")

        if not self.selected_test:
            self.selected_test = new_test

    def select_test(self, test_category, test_name):
        for test in self.tests:
            if test_category == test.test_category and test_name == test.test_name:
                self.selected_test = test
            
    
    # ----- Cover Page Pass Through Functions -----

    def add_equipment(self, equipment):
        self.cover_page.add_equipment(equipment)

    def add_general_specification(self, name, value):
        self.cover_page.add_general_specification(name, value)



    # -------- Test Pass through Functions ---------

    def add_CC(self, name: str = '', values=None):
        
        
        self.selected_test.add_CC(name, values)

    

    def add_Re(self, name: str = ''):
        self.selected_test.add_Re(name)

    def add_Ca(self, name: str = '', formula: str = ''):
        self.selected_test.add_Ca(name, formula)

    def add_Sp(self, name: str = '', specifications=None):
        self.selected_test.add_Sp(name, specifications)

    def update_from_dataframe(self, new_df: pd.DataFrame):
        self.selected_test.update_from_dataframe(new_df)
    
    # ----- Cover Page Getter Functions -----

    def get_equipment_used(self):
        return self.cover_page.equipment_used
    
    def get_general_specifications(self):
        return self.cover_page.general_specifications        
    
    def get_testing_and_review(self):
        return self.cover_page.testing_and_review
    
    def build_tables(self):
        self.selected_test.build_tables()


    # -------- Test Getter Functions ---------

    def get_metadata(self):
        return self.selected_test.metadata

    def get_CC(self):
        return self.selected_test.column_conditions
    
    def get_Re(self):
        return self.selected_test.results
    
    def get_Ca(self):
        return self.selected_test.calculations
    
    def get_root_table(self):
        return self.selected_test.root_table







    def reference_cp_gen_specs(self):
        pass


    def pickle(self, filepath=None):
        if filepath is None:
            filepath = f"{self.title}.pickle"

        with open(filepath, 'wb') as file:
            pickle.dump(self, file)

    def save_latex_pdf(self, filepath=None):
        pass

    def save_csv(self, filepath=None):
        pass