from parse import RowConditions, ColumnConditions, TableConditions, Results, Specifications, Calculations
import pandas as pd

class Blocks:

    def __init__(self, 
                 table_conditions: TableConditions, 
                 row_conditions: RowConditions, 
                 column_conditions: ColumnConditions, 
                 results: Results, 
                 specifications: Specifications, 
                 calculations: Calculations):
        
        
        self.TC = table_conditions
        self.RC = row_conditions
        self.CC = column_conditions
        self.Re = results
        self.Sp = specifications
        self.Ca = calculations

        self.rc_block = self.BuildRCBlock()
        self.header_block = self.BuildHeaderBlock()
        self.body_block = self.BuildBodyBlock()
        self.spec_block = self.BuildSpecBlock()
        self.calc_block, self.formulas = self.BuildCalcBlock()

    def BuildRCBlock(self):
        # make a df that just holds the data for the row conditions
        if not self.row_conditions['names']:
            return []

        row_data = []

        for i, (name, unit) in enumerate(zip(self.row_conditions['names'], self.row_conditions['units'])):
            # Format the row condition name with units
            if unit:
                row_name = f"{name} ({unit})"
            else:
                row_name = name
            
            # Get values for this specific row condition
            if i < len(self.row_conditions['values']):
                condition_values = self.row_conditions['values'][i]
            else:
                condition_values = ['']  # Default if no values
            
            # Create rows for each value
            for j, value in enumerate(condition_values):
                row = [''] * total_columns
                
                # All rows get the same name (simulating merged cells by repetition)
                row[0] = row_name
                
                # Second column gets the value
                row[1] = value
                
                # Fill remaining columns with placeholders
                for col in range(2, total_columns):
                    row[col] = '--'
                
                row_data.append(row)

        

    def BuildHeaderBlock(self):
        pass
    
    def BuildBodyBlock(self):
        pass
    
    def BuildSpecBlock(self):
        pass

    def BuildCalcBlock(self):
        pass



