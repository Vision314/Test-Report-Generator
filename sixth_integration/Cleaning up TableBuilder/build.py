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
        df = pd.DataFrame(index=range(len(self.RC.values)), columns=range(2))

        for value in self.RC.values:
            
        

    def BuildHeaderBlock(self):
        pass
    
    def BuildBodyBlock(self):
        pass
    
    def BuildSpecBlock(self):
        pass

    def BuildCalcBlock(self):
        pass



