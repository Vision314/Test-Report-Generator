from cover_page import *
from test_subclass import *

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

    def add_TC(self, name: str = '', values=None):
        self.selected_test.add_TC(name, values)

    # ----- Cover Page Getter Functions -----

    def get_equipment_used(self):
        return self.cover_page.equipment_used
    
    def get_general_specifications(self):
        return self.cover_page.general_specifications
    
    def get_testing_and_review(self):
        return self.cover_page.testing_and_review
    
    # -------- Test Getter Functions ---------

    def get_table_conditions(self):
        return self.selected_test.table_conditions

    def get_shape_of_table_arr(self):
        return self.selected_test.shape_of_table_arr

    def get_num_of_tables(self):
        return self.selected_test.num_of_tables

    def save(self, filepath=None):
        if filepath is None:
            filepath = f"{self.title}.pickle"

        with open(filepath, 'wb') as file:
            pickle.dump(self, file)
