import json
import numpy as np
import itertools
import pandas as pd

class Tables:
    def __init__(self, table_metadata: dict = {}):
        self.table_metadata = table_metadata
        
        # Parse all sections
        self.row_conditions = self._parse_row_conditions(table_metadata)
        self.column_conditions = self._parse_column_conditions(table_metadata)
        self.table_conditions = self._parse_table_conditions(table_metadata)
        self.results = self._parse_results(table_metadata)
        self.specifications = self._parse_specifications(table_metadata)
        self.calculations = self._parse_calculations(table_metadata)
        
        # Determine dimensions and create multi-dimensional array
        self.dimensions = self._calculate_dimensions()
        self.shape = self._calculate_shape()
        
        # Create the multi-dimensional array of tables
        self.tables = self._create_table_array()
    
    def _parse_values(self, value):
        """Parse a single value or a comma-separated list into a list"""
        if isinstance(value, str):
            return [v.strip() for v in value.split(',')] if value else []
        elif isinstance(value, list):
            return [v.strip() for v in value]
        else:
            return []
    
    def _parse_multi_dimensional_values(self, values_str):
        """Parse values that can be multi-dimensional like '[F1, F2], [99, 277]' or simple 'A, B, C'"""
        if not values_str:
            return []
        
        # Check if this is a multi-dimensional format with brackets
        if '[' in values_str and ']' in values_str:
            # Split by '], [' to get individual arrays
            arrays = []
            # First, split on '], [' 
            parts = values_str.split('], [')
            
            for i, part in enumerate(parts):
                # Clean up brackets
                part = part.strip()
                if i == 0:  # First part: remove leading '['
                    part = part.lstrip('[')
                if i == len(parts) - 1:  # Last part: remove trailing ']'
                    part = part.rstrip(']')
                
                # Split by comma and clean up
                array = [v.strip() for v in part.split(',')]
                arrays.append(array)
            
            return arrays
        else:
            # Simple comma-separated format - return as single array
            return [self._parse_values(values_str)]
    
    def _parse_row_conditions(self, metadata):
        """Parse row conditions - these become row labels"""
        rc = metadata.get('row_conditions', {})
        names = self._parse_values(rc.get('names', ''))
        units = self._parse_values(rc.get('units', ''))
        values = self._parse_multi_dimensional_values(rc.get('values', ''))
        return {'names': names, 'units': units, 'values': values}
    
    def _parse_column_conditions(self, metadata):
        """Parse column conditions - these become measurement columns"""
        cc = metadata.get('column_conditions', {})
        names = self._parse_values(cc.get('names', ''))
        units = self._parse_values(cc.get('units', ''))
        values = self._parse_multi_dimensional_values(cc.get('values', ''))
        return {'names': names, 'units': units, 'values': values}
    
    def _parse_table_conditions(self, metadata):
        """Parse table conditions - these determine multi-dimensional structure"""
        tc = metadata.get('table_conditions', {})
        names = self._parse_values(tc.get('names', ''))
        units = self._parse_values(tc.get('units', ''))
        values = self._parse_multi_dimensional_values(tc.get('values', ''))
        return {'names': names, 'units': units, 'values': values}
    
    def _parse_results(self, metadata):
        """Parse results section"""
        r = metadata.get('results', {})
        names = self._parse_values(r.get('names', ''))
        units = self._parse_values(r.get('units', ''))
        return {'names': names, 'units': units}
    
    def _parse_specifications(self, metadata):
        """Parse specifications section"""
        s = metadata.get('specifications', {})
        names = self._parse_values(s.get('names', ''))
        units = self._parse_values(s.get('units', ''))
        values = self._parse_values(s.get('values', ''))
        connection = s.get('connection', '')
        spec_type = s.get('type', '')
        return {'names': names, 'units': units, 'values': values, 'connection': connection, 'type': spec_type}
    
    def _parse_calculations(self, metadata):
        """Parse calculations section"""
        c = metadata.get('calculations', {})
        names = self._parse_values(c.get('names', ''))
        units = self._parse_values(c.get('units', ''))
        connection = c.get('connection', '')
        equation = c.get('equation', '')
        return {'names': names, 'units': units, 'connection': connection, 'equation': equation}
    
    def _calculate_dimensions(self):
        """Calculate the number of dimensions based on table conditions"""
        # If no table conditions, we have 1 table (0D)
        if not self.table_conditions['names']:
            return 0
        
        # The dimensions equal the number of table condition names
        return len(self.table_conditions['names'])
    
    def _calculate_shape(self):
        """Calculate the shape of the multi-dimensional array"""
        if self.dimensions == 0:
            return (1,)  # Single table
        
        values = self.table_conditions['values']
        if not values:
            return (1,)
        
        # Calculate shape based on the length of each value array
        shape = tuple(len(value_array) for value_array in values)
        return shape
    
    def _create_table_array(self):
        """Create the multi-dimensional array of DataFrames"""
        if self.dimensions == 0:
            # Single table case
            return [self._create_single_table()]
        
        # Multi-dimensional case
        # Create empty array with the right shape
        tables = np.empty(self.shape, dtype=object)
        
        # Fill the array with DataFrames
        for indices in np.ndindex(self.shape):
            table_condition_values = self._get_table_condition_values(indices)
            tables[indices] = self._create_single_table(table_condition_values)
        
        return tables
    
    def _calculate_total_columns(self):
        """Calculate the total number of columns needed for the table"""
        total_cols = 0
        
        # Row condition columns (first 2 columns if row conditions exist)
        if self.row_conditions['names']:
            total_cols += 2
        
        # Column condition columns (count total values across all conditions)
        if self.column_conditions['values']:
            for condition_values in self.column_conditions['values']:
                total_cols += len(condition_values)
        else:
            # No column conditions: results need their own columns
            if self.results['names']:
                total_cols += len(self.results['names'])
        
        # Specification columns
        if self.specifications['names']:
            total_cols += len(self.specifications['names'])
        
        # Calculation columns
        if self.calculations['names']:
            total_cols += len(self.calculations['names'])
        
        # Minimum of 1 column
        return max(total_cols, 1)
    
    def _format_table_conditions(self, table_condition_values):
        """Format table conditions as: NAME1 (UNIT1) = VALUE1, NAME2 (UNIT2) = VALUE2"""
        if not table_condition_values or not self.table_conditions['names']:
            return ""
        
        condition_parts = []
        names = self.table_conditions['names']
        units = self.table_conditions['units']
        
        for i, (name, value) in enumerate(zip(names, table_condition_values)):
            # Get unit if available, otherwise use empty string
            unit = units[i] if i < len(units) else ""
            
            if unit:
                condition_parts.append(f"{name} = {value} {unit}")
            else:
                condition_parts.append(f"{name} = {value}")
        
        return ", ".join(condition_parts)
    
    def _build_row_condition_data(self, total_columns):
        """Build row condition data with proper grouping and merging simulation"""
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
        
        return row_data

    def _build_column_condition_data(self, total_columns):
        """Build column condition header data with proper grouping and merging simulation"""
        # Always create two rows for column conditions (name row and value row)
        name_row = ['--'] * total_columns
        value_row = ['--'] * total_columns
        
        if not self.column_conditions['names']:
            return [name_row, value_row]
        
        # Start column index after row condition columns
        start_col = 2 if self.row_conditions['names'] else 0
        current_col = start_col
        
        # Build column headers for each column condition
        for i, (name, unit) in enumerate(zip(self.column_conditions['names'], self.column_conditions['units'])):
            # Format the column condition name with units
            if unit:
                col_name = f"{name} ({unit})"
            else:
                col_name = name
            
            # Get values for this specific column condition
            if i < len(self.column_conditions['values']):
                condition_values = self.column_conditions['values'][i]
            else:
                condition_values = ['--']  # Default if no values
            
            # Fill the name row (merge horizontally by repeating the name)
            for j in range(len(condition_values)):
                if current_col < total_columns:
                    name_row[current_col] = col_name
                    current_col += 1
            
            # Reset current_col for value row
            current_col = start_col
            # Skip to the correct position for this condition
            for prev_i in range(i):
                if prev_i < len(self.column_conditions['values']):
                    current_col += len(self.column_conditions['values'][prev_i])
            
            # Fill the value row
            for j, value in enumerate(condition_values):
                if current_col < total_columns:
                    value_row[current_col] = value
                    current_col += 1
        
        return [name_row, value_row]
    
    def _build_results_data(self, total_columns):
        """Build results row data with proper grouping across column conditions"""
        if not self.results['names']:
            return []
        
        # Start column index after row condition columns
        start_col = 2 if self.row_conditions['names'] else 0
        
        if self.column_conditions['values']:
            # With column conditions: create one row for each result
            results_rows = []
            for i, (name, unit) in enumerate(zip(self.results['names'], self.results['units'])):
                # Format the result name with units
                if unit:
                    result_name = f"{name} ({unit})"
                else:
                    result_name = name
                
                # Create row filled with "--" initially
                result_row = ['--'] * total_columns
                
                # Fill column condition areas with the result name
                current_col = start_col
                for condition_values in self.column_conditions['values']:
                    # Fill all columns for this condition group with the result name
                    for j in range(len(condition_values)):
                        if current_col < total_columns:
                            result_row[current_col] = result_name
                            current_col += 1
                
                results_rows.append(result_row)
            
            return results_rows
        else:
            # No column conditions: create header row with result names as columns
            result_header = ['--'] * total_columns
            
            # Fill remaining columns with result names
            current_col = start_col
            for i, (name, unit) in enumerate(zip(self.results['names'], self.results['units'])):
                if current_col < total_columns:
                    # Format the result name with units
                    if unit:
                        result_name = f"{name} ({unit})"
                    else:
                        result_name = name
                    result_header[current_col] = result_name
                    current_col += 1
            
            return [result_header]
    
    def _get_table_condition_values(self, indices):
        """Get the specific table condition values for given indices"""
        if self.dimensions == 0:
            return []
        
        if isinstance(indices, tuple):
            # Multi-dimensional case: get one value from each array
            return [self.table_conditions['values'][i][indices[i]] for i in range(len(indices))]
        else:
            # Single dimension case: get value from first array
            return [self.table_conditions['values'][0][indices]]
    
    def _create_single_table(self, table_condition_values=None):
        """Create a single DataFrame for specific table condition values"""
        # First, calculate the total number of columns we'll need
        total_columns = self._calculate_total_columns()
        
        # Build the complete table data including header rows
        all_rows = []
        
        # === COLUMN CONDITION HEADER ROWS ===
        # Add column condition headers only if column conditions exist
        if self.column_conditions['names']:
            column_condition_data = self._build_column_condition_data(total_columns)
            all_rows.extend(column_condition_data)
        
        # === RESULTS ROWS ===
        # Add results rows (if results exist)
        if self.results['names']:
            results_data = self._build_results_data(total_columns)
            all_rows.extend(results_data)
        
        # === DATA ROWS ===
        # Add row condition data if it exists
        if self.row_conditions['names']:
            row_condition_data = self._build_row_condition_data(total_columns)
            all_rows.extend(row_condition_data)
        else:
            # No row conditions - create simple placeholder rows
            num_data_rows = 1
            for i in range(num_data_rows):
                placeholder_row = ['--'] * total_columns
                all_rows.append(placeholder_row)
        
        # Create DataFrame with all rows (headers + data) - no row labels/index
        # Don't specify columns to avoid any header issues
        df = pd.DataFrame(all_rows)
        
        # Add metadata to DataFrame
        df.attrs['table_conditions'] = table_condition_values or []
        df.attrs['title'] = self._generate_title(table_condition_values)
        
        return df
    
    def _generate_title(self, table_condition_values):
        """Generate title for a specific table"""
        basic_info = self.table_metadata.get('basic_info', {})
        base_title = f"{basic_info.get('category', '')} - {basic_info.get('test_name', '')}"
        
        return base_title
    
    def get_table(self, *indices):
        """Get a specific table by indices"""
        if self.dimensions == 0:
            return self.tables[0]
        return self.tables[indices]
    
    def get_all_tables(self):
        """Get all tables as a flat list"""
        if self.dimensions == 0:
            return [self.tables[0]]
        return self.tables.flatten()
    
    def get_table_count(self):
        """Get total number of tables"""
        if self.dimensions == 0:
            return 1
        return np.prod(self.shape)
    
    def print_structure(self):
        """Print the structure of the table array"""
        print(f"Dimensions: {self.dimensions}")
        print(f"Shape: {self.shape}")
        print(f"Total tables: {self.get_table_count()}")
        
        if self.dimensions > 0:
            print("Table conditions:")
            for i, name in enumerate(self.table_conditions['names']):
                print(f"  {name}: {self.table_conditions['values']}")


