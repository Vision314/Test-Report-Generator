import pandas as pd
from itertools import product

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
        self.tables = {}
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
    
    @property
    def dimension_of_tables(self):
        return len(self.shape_of_table_arr)

    def add_CC(self, name: str = '', values=None):

        # update self.column_condition
        self.column_conditions[name] = values

        # update metadata
        self.add_metadata('CC', name)

        # update all tables to add a CC#
        # self.rebuild_tables()

    def append_CC(self, df, col_tag, metadata, cc_combos):
        cc_number = int(''.join(filter(str.isdigit, col_tag)))
        print(cc_number)

        col_content = []
        for combo in cc_combos:
            col_content.append(combo[cc_number - 1])

        df[metadata[col_tag]] = col_content

        return df
    

    def add_TC(self, name: str = '', values=None):
        self.table_conditions[name] = values
        # print(f"HIT: {self.shape_of_table_arr}")

        # self.generate_tables()


    def add_metadata(self, col_type, col_name):
        existing_CC_count = 1

        for key in self.metadata:
            if 'CC' in key:
                existing_CC_count+=1
        
        new_key = f"{col_type}{existing_CC_count}"

        self.metadata[new_key] = col_name


    def build_tables(self):

        self.generate_tables()

        cc_vals = list(self.table_conditions.values())
        cc_combos = list(product(*cc_vals))

        ordered_tags = list(metadata.keys())
        print(f"ORDERED COLUMNS: {ordered_columns}")

        for df in tables.values():

            for col_tag in ordered_tags:

                if 'CC' in col_tag:
                    df = append_CC(df, col_tag, metadata, cc_combos)

                elif 'Re' in col_tag:
                    pass

    def generate_tables(self):
        keys = list(self.table_conditions.keys())
        values = list(self.table_conditions.values())

        combos = product(*values)

        self.tables = {}
        for combo in combos:
            key_str = ", ".join(f"{k} = {v}" for k, v in zip(keys, combo))
            self.tables[key_str] = pd.DataFrame()

                

        
