
class RowConditions:
    def __init__(self, metadata: dict = {}):
        self.metadata_whole = metadata
        self.metadata_RC = metadata.get('table_conditions')

        self.names = self.parse_values(self.metadata_RC.get('names'))
        self.units = self.parse_values(self.metadata_RC.get('units'))
        self.values = self.parse_values(self.metadata_RC.get('values'))
        
        self.table_array_dimensions = self.calculate_dimensions()
        self.table_array_shape = self.calculate_shape()
        self.num_tables = self.calculate_num_tables()



    def parse_values(self, values_str):
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
        
    
