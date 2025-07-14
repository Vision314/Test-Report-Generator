import numpy as np

def parse_values(values_str):
        """Parse values that can be multi-dimensional like '[F1, F2], [99, 277]' or simple 'A, B, C'"""
        if not values_str:
            return []
        
        # check if this is a multidemensional format with brackets
        if '[' in values_str and ']' in values_str:
            # split by '], [' to get individual arrays
            arrays = []

            # split on '], ['
            parts = values_str.split('], [')
            

            # for each split value (and enumerate variable i)
            for i, part in enumerate(parts):
                # clean up brackets with .strip() to remove whitespace
                part = part.strip()

                # remove the first bracket
                if i == 0:
                    part = part.lstrip('[')
                    print("")

                # remove the last bracket
                elif i == len(parts) - 1:
                    part = part.rstrip(']')


                # strip the whitespace for each value in the part
                # and put it into an array, then append it to arrays
                array = [v.strip() for v in part.split(',')]
                arrays.append(array)

            return arrays


        else:
            """Parse a single value or a comma-separated list into a list"""
            return [v.strip() for v in values_str.split(',')] if values_str else []

def split_connection_str(connections):
            type_arr = []
            to_arr = []

            for connection in connections:
                arr = connection.split('->')

                type_arr.append(arr[0])
                to_arr.append(arr[1])

            return to_arr, type_arr

class TableConditions:
    def __init__(self, metadata: dict = {}):
        self.metadata_whole = metadata
        self.metadata_TC = metadata.get('table_conditions')

        self.names = parse_values(self.metadata_TC.get('names'))
        self.units = parse_values(self.metadata_TC.get('units'))
        self.values = parse_values(self.metadata_TC.get('values'))
        
        self.table_array_dimensions = self.calculate_dimensions()
        self.table_array_shape = self.calculate_shape()
        self.num_tables = self.calculate_num_tables()    

    def calculate_dimensions(self):
        return len(self.names)

    def calculate_shape(self):
        if self.table_array_dimensions == 0:
            return (1,)

        return tuple(len(value_array) for value_array in self.values)

    def calculate_num_tables(self):
        return np.prod(self.table_array_shape)
    
class RowConditions:
    def __init__(self, metadata: dict = {}):
        self.metadata_whole = metadata
        self.metadata_RC = metadata.get('row_conditions')

        self.names = parse_values(self.metadata_RC.get('names'))
        self.units = parse_values(self.metadata_RC.get('units'))
        self.values = parse_values(self.metadata_RC.get('values'))

        self.are_multiple_names = True if len(self.names) > 1 else False

class ColumnConditions:
    def __init__(self, metadata: dict = {}):
        self.metadata_whole = metadata
        self.metadata_CC = metadata.get('column_conditions')

        self.names = parse_values(self.metadata_CC.get('names'))
        self.units = parse_values(self.metadata_CC.get('units'))
        self.values = parse_values(self.metadata_CC.get('values'))

class Results:
    def __init__(self, metadata: dict = {}):
        self.metadata_whole = metadata
        self.metadata_results = metadata.get('results')

        self.names = parse_values(self.metadata_results.get('names'))
        self.units = parse_values(self.metadata_results.get('units'))
        self.values = parse_values(self.metadata_results.get('values'))

        self.contains_results = bool(self.metadata_results.get('names', False))

class Specifications:
    def __init__(self, metadata: dict = {}):
        self.metadata_whole = metadata
        self.metadata_specifications = metadata.get('specifications')

        self.names = parse_values(self.metadata_specifications.get('names'))
        self.units = parse_values(self.metadata_specifications.get('units'))
        self.values = parse_values(self.metadata_specifications.get('values'))

        self.connections = parse_values(self.metadata_specifications.get('connections'))
        self.types = parse_values(self.metadata_specifications.get('types'))
        
        # connection to
        # connection type
        self.connection_to, self.connection_type = split_connection_str(self.connections)


class Calculations:
    def __init__(self, metadata: dict = {}):
        self.metadata_whole = metadata
        self.metadata_calculations = metadata.get('specifications')

        self.names = parse_values(self.metadata_specifications.get('names'))
        self.units = parse_values(self.metadata_specifications.get('units'))

        self.connections = parse_values(self.metadata_specifications.get('connections'))
        self.equations = parse_values(self.metadata_calculations.get('equations'))

        self.connection_to, self.connection_type = split_connection_str(self.connections)

