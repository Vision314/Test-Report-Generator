import pandas as pd

class Test():
    def __init__(self, test_category: str='', test_name: str=''):
        self.column_conditions = {}
        
        self.table_conditions = {}

        self.result = []
        self.calculations = {}

        self.specifications = {} # placeholder for now
                                # not sure how to do specs

        self.name = test_name
        self.category = test_category
        # self.description = description

        self.metadata = {}
            # CC - column condition column
            # Re - result column
            # Ca - calculation column
            # Sp - specification column

        self.formulas = [{}]
        self.tables = []
        self.equipment_used = pd.DataFrame()

    @property
    def shape_of_table_arr(self):
        shape = []

        if not self.table_conditions:
            shape = [1]
            return shape
        else:
            for value in self.table_conditions.values():
                shape.append(len(value))
            return shape
        
    @property
    def num_of_tables(self):
        prod = 1
        
        for side in self.shape_of_table_arr:
            prod = prod * side

        return prod 

    def add_CC(self, name: str = '', values=None):

        # update self.column_condition
        self.column_conditions[name] = values

        # update metadata
        self.update_metadata('CC', name)

        # update table that you are editing
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        

    def add_TC(self, name: str = '', values=None):
        self.table_conditions[name] = values

    # def add_Re(self, name: str = ''):
    #     pass
    
    # def add_Ca(self, name: str = '', values=None):
    #     pass

    # def add_Sp(self, name: str='', values=None):
    #     pass

    def update_metadata(self, col_type, col_name):
        new_key = col_type
        existing_CC_count = 0

        for key in self.metadata:
            if 'CC' in key:
                existing_CC_count+=1
        
        new_key = new_key + existing_CC_count

        self.metadata[new_key] = col_name

    
