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

    @property
    def column_condition_combos(self):
        cc_vals = list(self.column_conditions.values())
        cc_combos = list(product(*cc_vals))
        return cc_combos

    def add_CC(self, name: str = '', values=None):
        self.column_conditions[name] = values

        if name not in self.metadata.values():
            cc_number = sum(1 for k in self.metadata if 'CC' in k) + 1
            self.metadata[f'CC{cc_number}'] = name

        new_length = len(self.column_condition_combos)
        for re_name in self.results:
            self.results[re_name] = self._resize_result_list(self.results[re_name], new_length)

        self.build_table()

    def _resize_result_list(self, result_list, new_length, placeholder='--'):
        current_length = len(result_list)
        if current_length < new_length:
            result_list.extend([placeholder] * (new_length - current_length))
        return result_list

    def add_Re(self, name: str = ''):
        self.results[name] = ['--'] * len(self.column_condition_combos)

        if name not in self.metadata.values():
            re_number = sum(1 for k in self.metadata if 'Re' in k) + 1
            self.metadata[f'Re{re_number}'] = name

        self.results[name] = ['--'] * len(self.column_condition_combos)
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
            raise ValueError(f"Length of specifications ({len(specifications)}) does not match number of test cases ({expected_length}).")

        # Add to specifications dictionary
        self.specifications[name] = specifications

        # Register metadata
        if name not in self.metadata.values():
            sp_number = sum(1 for k in self.metadata if k.startswith('Sp')) + 1
            self.metadata[f'Sp{sp_number}'] = name

        # Rebuild the table
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
        num_rows = len(combos)
        df = pd.DataFrame(index=range(num_rows))

        for tag in self.metadata.keys():
            col_name = self.metadata[tag]

            if tag.startswith('CC'):
                cc_index = int(tag[2:]) - 1
                col_values = [combo[cc_index] for combo in combos]
                df[col_name] = col_values

            elif tag.startswith('Re'):
                df[col_name] = self.results.get(col_name, ['--'] * num_rows)

            elif tag.startswith('Ca'):
                formula = self.calculations.get(col_name, '')
                df[col_name] = [self.evaluate_formula(formula, df.iloc[i]) for i in range(num_rows)]

            elif tag.startswith('Sp'):
                df[col_name] = self.specifications[col_name]


            else:
                df[col_name] = [None] * num_rows

        self.root_table = df
