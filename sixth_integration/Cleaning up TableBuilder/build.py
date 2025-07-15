from parse import BasicInfo, RowConditions, ColumnConditions, TableConditions, Results, Specifications, Calculations
import pandas as pd

class Blocks:

    def __init__(self, 
                 basic_info: BasicInfo,
                 table_conditions: TableConditions, 
                 row_conditions: RowConditions, 
                 column_conditions: ColumnConditions, 
                 results: Results, 
                 specifications: Specifications, 
                 calculations: Calculations):
        
        self.BI = basic_info
        self.TC = table_conditions
        self.RC = row_conditions
        self.CC = column_conditions
        self.Re = results
        self.Sp = specifications
        self.Ca = calculations

        self.rc_block = self.BuildRCBlock(self.RC)
        self.header_block = self.BuildHeaderBlock()
        self.body_block = self.BuildBodyBlock()
        self.spec_block = self.BuildSpecBlock()
        
        self.calc_block, self.formulas = self.BuildCalcBlock()
        self.tables_metadata = self.BuildTablesMetadata(self, self.BI, self.TC)

    def BuildRCBlock(self, RC: RowConditions):
        # Normalize inputs to be lists of lists
        if not isinstance(RC.values[0], list):
            RC.values = [RC.values]
            RC.names = [RC.names[0]]
            RC.units = [RC.units[0] if RC.units else '']

        rows = []
        for name, value_list, unit in zip(RC.names, RC.values, RC.units):
            label = f"{name} ({unit})" if unit else name
            for val in value_list:
                rows.append([label, val])

        return pd.DataFrame(rows, columns=[0, 1])
    """
    # def BuildRCBlock(self, values, names, units):
    #     row = 0
    #     if isinstance(values[0], list):

    #         total_rows = sum(len(sub_arr) for sub_arr in values)
    #         block_frame = pd.DataFrame(index=range(total_rows), columns=range(2))

    #         for i, (name, value, unit) in enumerate(zip(names, values, units)):

    #             for j, val in enumerate(value):
    #                 if not unit:
    #                     block_frame.iloc[row, 0] = name
    #                 else:
    #                     block_frame.iloc[row, 0] = f"{name} ({unit})"

    #                 block_frame.iloc[row, 1] = value[j]
            
    #                 row+=1

    #     else:
    #         total_rows = len(values)
    #         block_frame = pd.DataFrame(index=range(total_rows), columns=range(2))

    #         for i, value in enumerate(values):
    #             if units[0] == '':
    #                 block_frame.iloc[row, 0] = names[0]
    #             else:
    #                 block_frame.iloc[row, 0] = f"{names[0]} ({units[0]})"

    #             block_frame.iloc[row, 1] = value

    #             row+=1

    #     return block_frame
    """

    def BuildHeaderBlock(self):
        pass
    
    def BuildBodyBlock(self):
        pass
    
    def BuildSpecBlock(self):
        pass

    def BuildCalcBlock(self):
        
        df1, df2 = pd.DataFrame(index=range(2), columns=range(2))

        return df1, df2

    def BuildTablesMetadata(self):
        list_of_df = []
        tables_metadata = pd.DataFrame()





