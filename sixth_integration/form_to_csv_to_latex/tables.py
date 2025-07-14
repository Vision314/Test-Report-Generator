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
        print(self.calculations)
        
        # Determine dimensions and create multi-dimensional array
        self.dimensions = self._calculate_dimensions()
        self.shape = self._calculate_shape()
        
        # Create the multi-dimensional array of tables
        self.tables = self._create_table_array()
        
        # Create formula arrays - list of dictionaries, one per table
        self.formulas = self._create_formula_array()
        
        # Populate formulas for calculation columns after formulas array is created
        self._populate_calculation_formulas() 

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
        connection = self._parse_values(c.get('connection', ''))
        equation = self._parse_values(c.get('equation', ''))
        return {'names': names, 'units': units, 'connection': connection, 'equation': equation}

    def _parse_calculation_connections(self):
        """Parse calculation connections and return list of connection info"""
        connections = []
        if not self.calculations['connection']:
            return connections
        
        # Split multiple connections by comma

        # connection_strings = [c.strip() for c in self.calculations['connection'].split(',')]

        # print(connection_strings)
        
        for i, conn_str in enumerate(self.calculations['connection']):
            if '->' in conn_str:
                source, target = conn_str.split('->', 1)
                source = source.strip()
                target = target.strip()
                
                # Get corresponding calculation name and unit
                calc_name = self.calculations['names'][i] if i < len(self.calculations['names']) else ''
                calc_unit = self.calculations['units'][i] if i < len(self.calculations['units']) else ''
                
                connections.append({
                    'type': source,  # CN, CV, RN, etc.
                    'target': target,  # column name to find
                    'calc_name': calc_name,
                    'calc_unit': calc_unit,
                    'calc_index': i
                })

        print(connections)
        
        return connections

    def _normalize_column_name(self, col_name):
        """Normalize column name by removing units in parentheses for comparison"""
        if '(' in col_name and ')' in col_name:
            # Find the last occurrence of parentheses (in case there are multiple)
            last_paren = col_name.rfind('(')
            return col_name[:last_paren].strip()
        return col_name.strip()
    
    def _find_rightmost_matching_column(self, header_row, target_name, max_col):
        """Find the rightmost column that matches the target name (ignoring units)
        Supports both exact matching and partial matching (target as prefix)"""
        target_normalized = self._normalize_column_name(target_name)
        rightmost_col = -1
        
        # Search through the header row to find column headers
        for col_idx in range(min(len(header_row), max_col)):
            cell_value = header_row[col_idx]
            if cell_value and cell_value != '--':
                cell_normalized = self._normalize_column_name(str(cell_value))
                
                # Check for exact match first, then partial match (target as prefix)
                if (cell_normalized == target_normalized or 
                    cell_normalized.startswith(target_normalized + ' ') or
                    cell_normalized.startswith(target_normalized + '_')):
                    rightmost_col = max(rightmost_col, col_idx)
        
        return rightmost_col if rightmost_col >= 0 else None

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
    
    def get_table_count(self):
        """Get total number of tables"""
        if self.dimensions == 0:
            return 1
        return np.prod(self.shape)
    
    def _create_formula_array(self):
        """Create formula arrays - one dictionary per table"""
        total_tables = self.get_table_count()
        
        # Initialize empty formula dictionaries for each table
        formulas = []
        for i in range(total_tables):
            formulas.append({})  # Empty dict with string keys like "row,col": "formula"
        
        # Populate formulas based on metadata (placeholder for now)
        self._populate_formulas_from_metadata()
        
        return formulas
    
    def _populate_formulas_from_metadata(self):
        """Populate formulas based on metadata - placeholder function"""
        # TODO: Implement formula population based on calculations section
        # This will parse self.calculations['equation'] and create formulas
        # for specific cells in specific tables
        pass
    
    def _generate_formulas_for_calculations(self):
        """Generate formulas for calculation columns - placeholder function"""
        # TODO: This will handle creating formulas for calculation results
        # based on the calculations section in metadata
        pass
    
    def get_all_formulas(self):
        """Get all formula dictionaries as a list"""
        return self.formulas
    
    def get_formulas_for_table(self, table_index):
        """Get formulas for a specific table by index"""
        if 0 <= table_index < len(self.formulas):
            return self.formulas[table_index]
        return {}
    
    def set_formula(self, table_index, row, col, formula):
        """Set a formula for a specific cell in a specific table"""
        if 0 <= table_index < len(self.formulas):
            key = f"{row},{col}"
            self.formulas[table_index][key] = formula

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
        
        # Calculation columns - only count CN connections for now
        if self.calculations['names'] and self.calculations['connection']:
            # connection_type, _ = self._parse_calculation_connections(self.calculations['connection'])
            connection_type, _ = self._parse_calculation_connections()
            if connection_type == 'CN':
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
        
        # === INSERT CALCULATION COLUMNS ===
        # Insert calculation columns for CN connections
        all_rows = self._insert_calculation_columns(all_rows, total_columns)
        
        # === DATA ROWS ===
        # Add row condition data if it exists
        if self.row_conditions['names']:
            # Use actual column count from the modified table structure
            actual_columns = len(all_rows[0]) if all_rows else total_columns
            row_condition_data = self._build_row_condition_data(actual_columns)
            all_rows.extend(row_condition_data)
        else:
            # No row conditions - create simple placeholder rows
            num_data_rows = 1
            for i in range(num_data_rows):
                placeholder_row = ['--'] * (len(all_rows[0]) if all_rows else total_columns)
                all_rows.append(placeholder_row)
        
        # === PLACE CALCULATION NAMES IN DATA ROWS ===
        # Place calculation names with units in the correct data row position
        all_rows = self._place_calculation_names_in_data_rows(all_rows)
        
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
    
    def print_structure(self):
        """Print the structure of the table array"""
        print(f"Dimensions: {self.dimensions}")
        print(f"Shape: {self.shape}")
        print(f"Total tables: {self.get_table_count()}")
        
        if self.dimensions > 0:
            print("Table conditions:")
            for i, name in enumerate(self.table_conditions['names']):
                print(f"  {name}: {self.table_conditions['values']}")

    def get_all_formulas(self):
        """Get all formula dictionaries as a list"""
        return self.formulas
    
    def _shift_columns_right(self, table_data, from_col):
        """Shift all columns to the right starting from from_col"""
        for row in table_data:
            if len(row) > from_col:
                # Insert a new column and shift everything right
                row.insert(from_col, '--')
    
    # def _parse_calculation_connections(self, connection_string):
    #     """Parse calculation connection string like 'CN->Frequency' into type and target"""
    #     if not connection_string:
    #         return None, None
        
    #     if '->' in connection_string:
    #         connection_type, target = connection_string.split('->', 1)
    #         return connection_type.strip(), target.strip()
    #     else:
    #         # Just connection type without target
    #         return connection_string.strip(), None
    
    def _insert_calculation_columns(self, table_data, total_columns):
        """Insert calculation columns for CN connections after finding rightmost matches"""
        if not self.calculations['names']:
            return table_data
        
        # Parse the connection string to get type and target
        connection_type, target_name = self._parse_calculation_connections(self.calculations['connection'])
        print(connection_type)
        print(target_name)

        
        if connection_type == 'CN':
        
            # Determine header structure
            has_column_conditions = bool(self.column_conditions['names'])
            has_results = bool(self.results['names'])
            start_col = 2 if self.row_conditions['names'] else 0
            
            # Track inserted calculation columns for later name placement
            self._calculation_columns = {}  # Maps calc_name to column index
            
            # For each calculation, find where to insert it
            columns_inserted = 0
            
            for calc_name in self.calculations['names']:
                target_col = None
                
                # Use the target from connection string, or default to the calc_name
                search_target = target_name if target_name else calc_name
                
                # Find the rightmost matching column by searching in column header rows
                if has_column_conditions and has_results and len(table_data) > 2:
                    # For CN connections, search in column header rows (row 0), not results rows
                    target_col = self._find_rightmost_matching_column(
                        table_data[0], search_target, len(table_data[0])
                    )
                                
                elif not has_column_conditions and len(table_data) > 0:
                    # No column conditions - search in first row (results header)
                    target_col = self._find_rightmost_matching_column(
                        table_data[0], search_target, len(table_data[0])
                    )
                
                if target_col is not None:
                    insert_col = target_col + 1 + columns_inserted
                    
                    # Track this calculation column
                    self._calculation_columns[calc_name] = insert_col
                    
                    # Shift all rows to make space for the new column
                    for row in table_data:
                        if len(row) > insert_col:
                            row.insert(insert_col, '--')
                        else:
                            # Extend row if necessary
                            while len(row) <= insert_col:
                                row.append('--')
                            row[insert_col] = '--'
                    
                    # Do not insert calculation names in header rows - leave them as '--'
                    # The calculation names will be placed in the correct data row later
                    # by _place_calculation_names_in_data_rows method
                    
                    columns_inserted += 1
            
            return table_data
        

        elif connection_type == 'CV':
            # Determine header structure
            has_column_conditions = bool(self.column_conditions['names'])
            has_results = bool(self.results['names'])
            start_col = 2 if self.row_conditions['names'] else 0

            # Track inserted calculation columns for later name placement
            self._calculation_columns = {}  # Maps calc_name to column index
            
            # For each calculation, find where to insert it
            columns_inserted = 0


            for calc_name in self.calculations['names']:
                target_col = None




            return table_data

        elif connection_type == 'RN':
            return table_data

        else:
            # Unsupported connection type for now
            return table_data
    
    def _place_calculation_names_in_data_rows(self, table_data):
        """Place calculation names in the correct data row position after table is fully built"""
        if not self.calculations['names'] or not hasattr(self, '_calculation_columns'):
            return table_data
        
        # Calculate where to place calculation names: above first row condition value
        # Formula: total_rows - num_row_condition_values - 1 (for zero indexing)
        total_rows = len(table_data)
        
        if self.row_conditions['names']:
            # Count total row condition values across all conditions
            num_row_condition_values = sum(len(values) for values in self.row_conditions['values'])
            name_row_index = total_rows - num_row_condition_values - 1
            
            # Place each calculation name with units in the calculated row
            for i, calc_name in enumerate(self.calculations['names']):
                # Use tracked column index from insertion phase
                if calc_name in self._calculation_columns:
                    col_idx = self._calculation_columns[calc_name]
                    
                    # Add units to the calculation name if available
                    calc_units = self.calculations.get('units', [])
                    if i < len(calc_units) and calc_units[i]:
                        full_calc_name = f"{calc_name} ({calc_units[i]})"
                    else:
                        full_calc_name = calc_name
                    
                    # Place the calculation name with units in the appropriate row
                    if 0 <= name_row_index < len(table_data):
                        table_data[name_row_index][col_idx] = full_calc_name
                    
                    # Place equation values in all data rows below the calculation name
                    equation = self.calculations.get('equation', '')
                    if equation:
                        # Loop through all rows below the calculation name row
                        for row_idx in range(name_row_index + 1, total_rows):
                            if row_idx < len(table_data) and col_idx < len(table_data[row_idx]):
                                table_data[row_idx][col_idx] = equation
        
        return table_data
    
    def _populate_calculation_formulas(self):
        """Populate formulas dictionary with calculation equations for all tables"""
        if not self.calculations['names'] or not hasattr(self, '_calculation_columns'):
            return
        
        equation = self.calculations.get('equation', '')
        if not equation:
            return
        
        # For each table, populate formulas for calculation columns
        for table_idx in range(len(self.formulas)):
            table = self.get_table(table_idx) if self.dimensions > 0 else self.tables[0]
            total_rows = table.shape[0]
            
            if self.row_conditions['names']:
                # Calculate the same name_row_index as in _place_calculation_names_in_data_rows
                num_row_condition_values = sum(len(values) for values in self.row_conditions['values'])
                name_row_index = total_rows - num_row_condition_values - 1
                
                # Populate formulas for all calculation columns
                for calc_name in self.calculations['names']:
                    if calc_name in self._calculation_columns:
                        col_idx = self._calculation_columns[calc_name]
                        
                        # Add formula entries for all data rows below the calculation name
                        for row_idx in range(name_row_index + 1, total_rows):
                            formula_key = f"{row_idx},{col_idx}"
                            self.formulas[table_idx][formula_key] = equation

