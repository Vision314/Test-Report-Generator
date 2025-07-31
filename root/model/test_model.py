import pandas as pd
from itertools import product
import re

class Test():
    def __init__(self, test_category: str = '', test_name: str = ''):
        self.column_conditions = {}
        self.results = {}
        self.calculations = {}
        self.specifications = {}

        self.name = test_name
        self.category = test_category

        self.metadata = {}

        self.root_table = pd.DataFrame()
        self.equipment_used = pd.DataFrame(index=self.column_condition_combos)

        cover_page_vars = {}

    @property
    def column_condition_combos(self):
        
        cc_vals = []

        for tag in self.metadata.keys():
            if tag.startswith('CC'):
                name = self.metadata[tag]
                cc_vals.append(self.column_conditions[name])    

        cc_combos = list(product(*cc_vals))
        return cc_combos

    def add_CC(self, name: str = '', values=None):
        self.column_conditions[name] = values

        if name not in self.metadata.values():
            # cc_number = sum(1 for k in self.metadata if 'CC' in k) + 1
            # cc_number = greates tag # for CC's
            cc_number = str(max((int(tag[2:]) for tag in self.metadata if tag.startswith('CC')), default=0) + 1)
            print(f"\n\nTHIS IS THE CCNUMBER: {cc_number}\n\n")
            self.metadata[f'CC{cc_number}'] = name

        
        new_length = len(self.column_condition_combos)
        for re_name in self.results:
            self.results[re_name] = self._resize_result_list(self.results[re_name], new_length)

        self.build_table()

    def edit_CC(self, col_tag, new_name: str='', new_values=None):
        # get old name
        # change value in metdata
        # remove the column and values from column_conditions dict
        # append a new column with the new name and new values
            # metadata holds order of df
        # build_table()

        print("\n\n")
        print(f"EDITING COLUMN: {col_tag}")


        # get the old name
        old_name = self.metadata[col_tag]

        print(f"OLD NAME: {old_name}\tNEW NAME: {new_name}")
        print(f"OLD METADATA: {self.metadata}")
        # change the value in the METADATA (keeping same order in df)
        self.metadata[col_tag] = new_name
        print(f"NEW METADATA: {self.metadata}")

        print(f"OLD COLUMN CONDITIONS: {self.column_conditions}")


        # remove the old column
        self.column_conditions.pop(old_name)

        print(f"REMOVED {col_tag} COLUMN CONDITIONS: {self.column_conditions}")

        # insert the new column at the end, doesn't matter because
        # metadata holds order of df
        self.column_conditions[new_name] = new_values

        print(f"NEW COLUMN CONDITIONS: {self.column_conditions}")

        print("\n\n")

        new_length = len(self.column_condition_combos)
        for re_name in self.results:
            self.results[re_name] = self._resize_result_list(self.results[re_name], new_length)


        self.build_table()




    def del_CC(self, col_tag):
        name = self.metadata[col_tag]

        del self.column_conditions[name]
        del self.metadata[col_tag]

        new_length = len(self.column_condition_combos)
        for re_name in self.results:
            self.results[re_name] = self._resize_result_list(self.results[re_name], new_length)

        print("\n\n\n DEBUG BUILD:")
        print(f"COMBOS: {self.column_condition_combos}")
        print(f"CONDITIONS: {self.column_conditions}")
        print(f"\nMETADATA: {self.metadata}")


        self.build_table()

    def _resize_result_list(self, result_list, new_length, placeholder=''):
        current_length = len(result_list)
        if current_length < new_length:
            result_list.extend([placeholder] * (new_length - current_length))

        elif current_length > new_length:
            result_list = result_list[:new_length]
        return result_list

    def add_Re(self, name: str = ''):
        # commented out for result test
        # self.results[name] = ['--'] * len(self.column_condition_combos)
        self.results[name] = []

        if name not in self.metadata.values():
            re_number = sum(1 for k in self.metadata if 'Re' in k) + 1
            self.metadata[f'Re{re_number}'] = name

        # commented out for result test
        self.results[name] = [''] * len(self.column_condition_combos)
        self.build_table()

    def edit_Re_name(self, col_tag, new_name: str = ''):
        # 1. get old name
        old_name = self.metadata[col_tag]
        old_values = self.results[old_name]
        # 2. change value in metdata
        self.metadata[col_tag] = new_name
        # 3. remove the column and values from results dict
        self.results.pop(old_name)

        # append a new column with the new name and original values
            # metadata holds order of df

        self.results[new_name] = old_values
        self.build_table()

    def del_Re(self, col_tag):
        name = self.metadata[col_tag]

        del self.results[name]
        del self.metadata[col_tag]

        self.build_table()

    def edit_Re_val(self, name, row, value):
        self.results[name][row] = value
        print(f"RESULTS: {self.results}")
        self.build_table()

    def add_Ca(self, name: str = '', formula: str = ''):

        if not (formula.startswith('=') and ('CC(' in formula or 'Re(' in formula)):
            raise ValueError(f"Invalid formula syntax: {formula}")

        if not formula.startswith('='):
            formula = f'={formula}'

        self.calculations[name] = formula

        if name not in self.metadata.values():
            ca_number = sum(1 for k in self.metadata if k.startswith('Ca')) + 1
            self.metadata[f'Ca{ca_number}'] = name

        self.build_table()


    def add_Sp(self, name: str = '', specifications=None):
        if specifications is None:
            raise ValueError("Specifications list is required.")

        expected_length = len(self.column_condition_combos)
        if len(specifications) != expected_length:
            raise ValueError(
                f"Length of specifications ({len(specifications)}) does not match number of test cases ({expected_length})."
            )

        # Add to specifications dictionary
        self.specifications[name] = specifications

        # Register in metadata
        if name not in self.metadata.values():
            sp_number = sum(1 for k in self.metadata if k.startswith('Sp')) + 1
            self.metadata[f'Sp{sp_number}'] = name

        # Rebuild the table to include this column
        self.build_table()


    def evaluate_formula(self, formula: str, row: pd.Series):
        """
        Evaluates a formula string row-wise by replacing CC() and Re() with actual values.
        """
        if not isinstance(formula, str) or not formula.startswith('='):
            return formula  # Not a formula

        expr = formula[1:]  # remove leading '='

        try:
            # Replace CC('colname') and Re('colname') with actual row values
            expr = re.sub(r"CC\('(.+?)'\)", lambda m: str(row.get(m.group(1), 'None')), expr)
            expr = re.sub(r"Re\('(.+?)'\)", lambda m: str(row.get(m.group(1), 'None')), expr)

            return eval(expr)
        except Exception as e:
            return "#ERR"

    def update_from_dataframe(self, new_df: pd.DataFrame):
        """
        Update internal structures from an externally edited DataFrame.
        Assumes CC columns remain unchanged.
        Updates result and spec columns, and registers new ones if needed.
        """
        cc_cols = [self.metadata[k] for k in self.metadata if k.startswith('CC')]
        existing_results = set(self.results.keys())
        existing_specs = set(self.specifications.keys())

        for col in new_df.columns:
            if col in cc_cols:
                continue

            col_data = new_df[col].tolist()

            if col not in existing_results and col not in existing_specs:
                # Assume it's a result by default
                re_number = sum(1 for k in self.metadata if k.startswith('Re')) + 1
                self.results[col] = col_data
                self.metadata[f'Re{re_number}'] = col

            elif col in existing_results:
                self.results[col] = col_data

            elif col in existing_specs:
                self.specifications[col] = col_data

        self.build_table()


    def build_table(self):
        combos = self.column_condition_combos
        print(f"THESE ARE THE CC COMBOS:\n{combos}")
        num_rows = len(combos)
        df = pd.DataFrame(index=range(num_rows))
        cc_index = 0
        for tag in self.metadata.keys():
            col_name = self.metadata[tag]

            if tag.startswith('CC'):
                # cc_index = int(tag[2:]) - 1
                
                print(f"\nCC_INDEX: {cc_index}\n")
                # cc_index = list(self.column_conditions.keys()).index(col_name)
                col_values = [combo[cc_index] for combo in combos]
                df[col_name] = col_values
                cc_index+=1

            elif tag.startswith('Re'):
                df[col_name] = self.results[col_name]

            elif tag.startswith('Ca'):
                formula = self.calculations.get(col_name, '')
                df[col_name] = [self.evaluate_formula(formula, df.iloc[i]) for i in range(num_rows)]

            elif tag.startswith('Sp'):
                df[col_name] = self.specifications[col_name]


            else:
                df[col_name] = [None] * num_rows

        self.root_table = df

        print(self.root_table.head())

    def manual_table_input(self):
        pass
