# ╭──────────────────────────────────────────────────────────────────────────╮
# │                    Engineering Test Report Generator                     │
# │                     Model Component (MVC) + FORMULA EDITOR              │
# │                            WITH CSV FORMULA SUPPORT                     │
# ╰──────────────────────────────────────────────────────────────────────────╯

import os
import json
import pandas as pd
import re

class FormulaModel:
    def __init__(self, report_path: str = None) -> None:
        # Base path for the report project
        self.report_path = report_path
        
        # Main data containers
        self.test_selections = {}
        self.cover_page_data = {}
        self.test_data = {}
        
        # Formula editor data structures
        self.formulas = {}       # {(section, row, col): formula_string}
        self.dependencies = {}   # {(section, row, col): set of dependent cells}
        
        # File paths
        self.tests_path = None
        self.cover_page_path = None
        self.report_output_path = None
        
        if self.report_path:
            self._initialize_paths()
            self._load_existing_data()
    
    def _initialize_paths(self):
        """Set up the file paths based on the report structure"""
        self.tests_path = os.path.join(self.report_path, 'tests')
        self.cover_page_path = os.path.join(self.report_path, 'cover_page')
        self.report_output_path = os.path.join(self.report_path, 'report')
    
    def _load_existing_data(self):
        """Load existing data from the report structure"""
        # Load test selections
        selections_file = os.path.join(self.tests_path, 'test_selections.json')
        if os.path.exists(selections_file):
            with open(selections_file, 'r') as f:
                self.test_selections = json.load(f)
        
        # Load cover page data
        if os.path.exists(self.cover_page_path):
            self._load_cover_page_data()
    
    def _load_cover_page_data(self):
        """Load cover page JSON files into data structures"""
        cover_page_files = [
            'equipment_used.json',
            'general_specifications.json', 
            'product_information.json',
            'testing_and_review.json'
        ]
        
        for file_name in cover_page_files:
            file_path = os.path.join(self.cover_page_path, file_name)
            if os.path.exists(file_path):
                key = file_name.replace('.json', '')
                with open(file_path, 'r') as f:
                    self.cover_page_data[key] = json.load(f)

    # FORMULA EDITOR METHODS
    def load_formulas(self, section_id: str, filepath: str = None):
        """Load formulas for a specific section"""
        if not filepath:
            filepath = self._get_formula_filepath(section_id)
        
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    formulas_data = json.load(f)
                for key, formula in formulas_data.items():
                    row, col = map(int, key.split(","))
                    self.formulas[(section_id, row, col)] = formula
            except Exception as e:
                print(f"Failed to load formulas for {section_id}: {e}")

    def save_formulas(self, section_id: str, filepath: str = None):
        """Save formulas for a specific section"""
        if not filepath:
            filepath = self._get_formula_filepath(section_id)
        
        # Filter formulas for this section
        section_formulas = {}
        for (sec_id, row, col), formula in self.formulas.items():
            if sec_id == section_id:
                section_formulas[f"{row},{col}"] = formula
        
        if section_formulas:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(section_formulas, f, indent=2)
        elif os.path.exists(filepath):
            os.remove(filepath)

    def _get_formula_filepath(self, section_id: str):
        """Get formula file path for section"""
        if section_id.startswith('cover_'):
            section_name = section_id.replace('cover_', '')
            return os.path.join(self.cover_page_path, f"{section_name}.formulas.json")
        else:
            # Test data formula file
            parts = section_id.split('_')
            if len(parts) >= 3:
                category, test_name = parts[0], parts[1]
                table_name = '_'.join(parts[2:])
                return os.path.join(self.tests_path, category, test_name, 'csv', f"{table_name}.formulas.json")
        return None

    def set_formula(self, section_id: str, row: int, col: int, formula: str):
        """Set formula for specific cell"""
        self.formulas[(section_id, row, col)] = formula
        self.update_dependencies(section_id, row, col, formula)

    def get_formula(self, section_id: str, row: int, col: int):
        """Get formula for specific cell"""
        return self.formulas.get((section_id, row, col))

    def remove_formula(self, section_id: str, row: int, col: int):
        """Remove formula for specific cell"""
        key = (section_id, row, col)
        if key in self.formulas:
            del self.formulas[key]
            self.clear_dependencies(section_id, row, col)

    def update_dependencies(self, section_id: str, row: int, col: int, formula: str):
        """Update dependency tracking for a formula cell"""
        self.clear_dependencies(section_id, row, col)
        refs = re.findall(r"[A-Z]+\d+", formula.upper())
        for ref in refs:
            r, c = self.cell_name_to_index(ref)
            dep_key = (section_id, r, c)
            self.dependencies.setdefault(dep_key, set()).add((section_id, row, col))

    def clear_dependencies(self, section_id: str, row: int, col: int):
        """Remove cell from all dependency lists"""
        for dep_set in self.dependencies.values():
            dep_set.discard((section_id, row, col))

    def cell_name_to_index(self, name: str):
        """Convert cell name (e.g., 'A1') to (row, col) indices"""
        match = re.match(r"([A-Z]+)(\d+)", name.upper())
        if not match:
            return 0, 0
        
        col_letters, row_number = match.groups()
        col_number = 0
        for i, char in enumerate(reversed(col_letters)):
            col_number += (ord(char) - 65 + 1) * (26 ** i)
        return int(row_number) - 1, col_number - 1

    def adjust_formula_references(self, formula: str, source_row: int, source_col: int, target_row: int, target_col: int):
        """Adjust cell references in formula when copying to different location (Excel-like)"""
        if not formula.startswith("="):
            return formula
            
        row_diff = target_row - source_row
        col_diff = target_col - source_col
        
        def replace_ref(match):
            full_ref = match.group(0)
            col_part = match.group(1)
            row_part = match.group(2)
            
            # Parse column (handle $ for absolute reference)
            if col_part.startswith('$'):
                new_col_part = col_part  # Absolute column reference
            else:
                # Relative column reference - adjust it
                col_letters = col_part
                col_num = 0
                for i, char in enumerate(reversed(col_letters)):
                    col_num += (ord(char) - 65 + 1) * (26 ** i)
                
                new_col_num = col_num + col_diff
                if new_col_num < 1:
                    new_col_num = 1
                    
                # Convert back to letters
                new_col_part = ""
                while new_col_num > 0:
                    new_col_num -= 1
                    new_col_part = chr(65 + new_col_num % 26) + new_col_part
                    new_col_num //= 26
            
            # Parse row (handle $ for absolute reference)
            if row_part.startswith('$'):
                new_row_part = row_part  # Absolute row reference
            else:
                # Relative row reference - adjust it
                row_num = int(row_part)
                new_row_num = row_num + row_diff
                if new_row_num < 1:
                    new_row_num = 1
                new_row_part = str(new_row_num)
            
            return new_col_part + new_row_part
        
        # Pattern to match cell references like A1, $A1, A$1, $A$1
        pattern = r'(\$?[A-Z]+)(\$?\d+)'
        adjusted_formula = re.sub(pattern, replace_ref, formula)
        return adjusted_formula

    # ORIGINAL TEST REPORT METHODS
    def get_cover_page_section(self, section_name: str):
        """Get cover page section data for tksheet display"""
        return self.cover_page_data.get(section_name, [])
    
    def save_cover_page_section(self, section_name: str, tksheet_data: list):
        """Save tksheet data to cover page section"""
        self.cover_page_data[section_name] = tksheet_data
        
        if self.cover_page_path:
            os.makedirs(self.cover_page_path, exist_ok=True)
            file_path = os.path.join(self.cover_page_path, f"{section_name}.json")
            with open(file_path, 'w') as f:
                json.dump(tksheet_data, f, indent=2)
        
        # Save formulas for this section
        self.save_formulas(f"cover_{section_name}")

    def get_cover_page_dataframe(self, section_name: str):
        """Convert cover page section to pandas DataFrame"""
        data = self.cover_page_data.get(section_name, [])
        if not data or len(data) < 2:
            return pd.DataFrame()
        
        headers = data[0]
        rows = data[1:]
        return pd.DataFrame(rows, columns=headers)

    def initialize_default_cover_page(self):
        """Initialize default cover page structure with headers"""
        default_sections = {
            'product_information': [
                ['Field', 'Value'],
                ['Globtek Model Name', ''],
                ['Globtek Product Number', ''],
                ['Customer Product Number', '']
            ],
            'general_specifications': [
                ['Parameter', 'Min', 'Max', 'Typ', 'Notes'],
                ['Input Voltages', '', '', '', ''],
                ['Output Voltages (V)', '', '', '', ''],
                ['Output Current (A)', '', '', '', ''],
                ['Power Rating (W)', '', '', '', '']
            ],
            'testing_and_review': [
                ['Role', 'Name', 'Date'],
                ['Tested By', '', ''],
                ['Start Date', '', ''],
                ['End Date', '', ''],
                ['Reviewed By', '', ''],
                ['Start Date', '', ''],
                ['End Date', '', '']
            ],
            'equipment_used': [
                ['Equipment Type', 'Manufacturer', 'Model', 'Description', 'S/N', 'Last Calibrated', 'Calibration Due'],
                ['', '', '', '', '', '', '']
            ]
        }
        
        for section_name, default_data in default_sections.items():
            if section_name not in self.cover_page_data:
                self.save_cover_page_section(section_name, default_data)

    def get_test_data(self, category: str, test_name: str):
        """Get all data files for a specific test"""
        test_data = {}
        test_path = os.path.join(self.tests_path, category, test_name, 'csv')
        
        if not os.path.exists(test_path):
            return test_data
        
        for file_name in os.listdir(test_path):
            if file_name.startswith('table') and file_name.endswith('.csv'):
                file_path = os.path.join(test_path, file_name)
                try:
                    df = pd.read_csv(file_path)
                    data_list = [df.columns.tolist()] + df.values.tolist()
                    section_name = file_name.replace('.csv', '')
                    test_data[section_name] = data_list
                    
                    # Load formulas for this table
                    section_id = f"{category}_{test_name}_{section_name}"
                    self.load_formulas(section_id)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue
        
        return test_data
    
    def save_test_data(self, category: str, test_name: str, section_name: str, tksheet_data: list):
        """Save test data to CSV file"""
        test_path = os.path.join(self.tests_path, category, test_name, 'csv')
        os.makedirs(test_path, exist_ok=True)
        
        file_path = os.path.join(test_path, f"{section_name}.csv")
        
        if not tksheet_data or len(tksheet_data) < 2:
            pd.DataFrame().to_csv(file_path, index=False)
            return
        
        try:
            headers = tksheet_data[0]
            rows = tksheet_data[1:]
            df = pd.DataFrame(rows, columns=headers)
            df.to_csv(file_path, index=False)
            
            # Save formulas for this table
            section_id = f"{category}_{test_name}_{section_name}"
            self.save_formulas(section_id)
        except Exception as e:
            print(f"Error saving {file_path}: {e}")

    def create_report(self):
        """Generate the complete report from selected tests and cover page data"""
        pass

    def send_report(self):
        """Send or distribute the generated report"""
        pass
