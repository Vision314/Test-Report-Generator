import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import csv
from datetime import datetime
import re

class DataParser:
    """Utility class to parse different data formats from form inputs"""
    
    @staticmethod
    def parse_value(value_str):
        """
        Parse a string value into appropriate Python data structure
        Handles:
        - Single values: "vin" -> "vin"
        - Arrays: "1.0, 4.5, 0.05" -> [1.0, 4.5, 0.05]
        - 2D Arrays: "[F1, F2], [120, 240]" -> [["F1", "F2"], [120, 240]]
        """
        if not value_str or not value_str.strip():
            return None
            
        value_str = value_str.strip()
        
        # Check if it's a 2D array (contains brackets)
        if '[' in value_str and ']' in value_str:
            return DataParser._parse_2d_array(value_str)
        
        # Check if it's a comma-separated array
        elif ',' in value_str:
            return DataParser._parse_array(value_str)
        
        # Single value
        else:
            return DataParser._parse_single_value(value_str)
    
    @staticmethod
    def _parse_single_value(value_str):
        """Parse a single value (string or number)"""
        # Try to convert to number first
        try:
            if '.' in value_str:
                return float(value_str)
            else:
                return int(value_str)
        except ValueError:
            # Return as string if not a number
            return value_str
    
    @staticmethod
    def _parse_array(value_str):
        """Parse comma-separated values into an array"""
        values = []
        for item in value_str.split(','):
            item = item.strip()
            values.append(DataParser._parse_single_value(item))
        return values
    
    @staticmethod
    def _parse_2d_array(value_str):
        """Parse 2D array format: [val1, val2], [val3, val4]"""
        try:
            # Use regex to find all bracket groups
            bracket_pattern = r'\[([^\]]+)\]'
            matches = re.findall(bracket_pattern, value_str)
            
            result = []
            for match in matches:
                # Parse each bracket group as an array
                row = DataParser._parse_array(match)
                result.append(row)
            
            return result
        except Exception as e:
            print(f"Error parsing 2D array '{value_str}': {e}")
            return value_str

class TestReportGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Test Report Generator")
        self.root.geometry("900x800")
        
        # Initialize data storage
        self.test_data = {}
        
        # Create main canvas and scrollbar for scrolling
        self.canvas = tk.Canvas(root)
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Bind mousewheel to canvas
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        # Create all sections in one window
        self.create_all_sections()
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def create_all_sections(self):
        """Create all sections in one scrollable window"""
        main_frame = self.scrollable_frame
        
        # Add padding to main frame
        main_frame.configure(padding=20)
        
        current_row = 0
        
        # Basic Information Section
        current_row = self.create_basic_info_section(main_frame, current_row)
        
        # Add separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=current_row, column=0, columnspan=2, sticky='ew', pady=20)
        current_row += 1
        
        # Conditions Section
        current_row = self.create_conditions_section(main_frame, current_row)
        
        # Add separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=current_row, column=0, columnspan=2, sticky='ew', pady=20)
        current_row += 1
        
        # Results Section
        current_row = self.create_results_section(main_frame, current_row)
        
        # Add separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=current_row, column=0, columnspan=2, sticky='ew', pady=20)
        current_row += 1
        
        # Specifications Section
        current_row = self.create_specifications_section(main_frame, current_row)
        
        # Add separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=current_row, column=0, columnspan=2, sticky='ew', pady=20)
        current_row += 1
        
        # Calculations Section
        current_row = self.create_calculations_section(main_frame, current_row)
        
        # Add separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=current_row, column=0, columnspan=2, sticky='ew', pady=20)
        current_row += 1
        
        # Generation Section
        current_row = self.create_generation_section(main_frame, current_row)
        
        # Configure column weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
    def create_basic_info_section(self, parent, start_row):
        """Create basic information section"""
        # Section title
        title_label = ttk.Label(parent, text="Basic Information", font=('Arial', 12, 'bold'))
        title_label.grid(row=start_row, column=0, columnspan=2, sticky='w', pady=(0, 10))
        start_row += 1
        
        # Test Category
        ttk.Label(parent, text="Test Category:").grid(row=start_row, column=0, sticky='w', padx=5, pady=5)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(parent, textvariable=self.category_var, 
                                     values=["input", "output", "safety", "performance", "environmental"])
        category_combo.grid(row=start_row, column=1, sticky='ew', padx=5, pady=5)
        start_row += 1
        
        # Test Name
        ttk.Label(parent, text="Test Name:").grid(row=start_row, column=0, sticky='w', padx=5, pady=5)
        self.test_name_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.test_name_var).grid(row=start_row, column=1, sticky='ew', padx=5, pady=5)
        start_row += 1
        
        # Test Description
        ttk.Label(parent, text="Test Description:").grid(row=start_row, column=0, sticky='nw', padx=5, pady=5)
        self.description_text = tk.Text(parent, height=4, width=50)
        self.description_text.grid(row=start_row, column=1, sticky='ew', padx=5, pady=5)
        start_row += 1
        
        return start_row
        
    def create_conditions_section(self, parent, start_row):
        """Create conditions section"""
        # Section title
        title_label = ttk.Label(parent, text="Test Conditions", font=('Arial', 12, 'bold'))
        title_label.grid(row=start_row, column=0, columnspan=2, sticky='w', pady=(0, 10))
        start_row += 1
        
        # Row Conditions
        row_frame = ttk.LabelFrame(parent, text="Row Conditions", padding=10)
        row_frame.grid(row=start_row, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        start_row += 1
        
        ttk.Label(row_frame, text="Names:").grid(row=0, column=0, sticky='w')
        self.row_names_var = tk.StringVar()
        ttk.Entry(row_frame, textvariable=self.row_names_var, width=60).grid(row=0, column=1, sticky='ew')
        
        ttk.Label(row_frame, text="Units:").grid(row=1, column=0, sticky='w')
        self.row_units_var = tk.StringVar()
        ttk.Entry(row_frame, textvariable=self.row_units_var, width=60).grid(row=1, column=1, sticky='ew')
        
        ttk.Label(row_frame, text="Values:").grid(row=2, column=0, sticky='w')
        self.row_values_var = tk.StringVar()
        ttk.Entry(row_frame, textvariable=self.row_values_var, width=60).grid(row=2, column=1, sticky='ew')
        
        row_frame.columnconfigure(1, weight=1)
        
        # Column Conditions
        col_frame = ttk.LabelFrame(parent, text="Column Conditions", padding=10)
        col_frame.grid(row=start_row, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        start_row += 1
        
        ttk.Label(col_frame, text="Names:").grid(row=0, column=0, sticky='w')
        self.col_names_var = tk.StringVar()
        ttk.Entry(col_frame, textvariable=self.col_names_var, width=60).grid(row=0, column=1, sticky='ew')
        
        ttk.Label(col_frame, text="Units:").grid(row=1, column=0, sticky='w')
        self.col_units_var = tk.StringVar()
        ttk.Entry(col_frame, textvariable=self.col_units_var, width=60).grid(row=1, column=1, sticky='ew')
        
        ttk.Label(col_frame, text="Values:").grid(row=2, column=0, sticky='w')
        self.col_values_var = tk.StringVar()
        ttk.Entry(col_frame, textvariable=self.col_values_var, width=60).grid(row=2, column=1, sticky='ew')
        
        col_frame.columnconfigure(1, weight=1)
        
        # Table Conditions
        table_frame = ttk.LabelFrame(parent, text="Table Conditions", padding=10)
        table_frame.grid(row=start_row, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        start_row += 1
        
        ttk.Label(table_frame, text="Names:").grid(row=0, column=0, sticky='w')
        self.table_names_var = tk.StringVar()
        ttk.Entry(table_frame, textvariable=self.table_names_var, width=60).grid(row=0, column=1, sticky='ew')
        
        ttk.Label(table_frame, text="Units:").grid(row=1, column=0, sticky='w')
        self.table_units_var = tk.StringVar()
        ttk.Entry(table_frame, textvariable=self.table_units_var, width=60).grid(row=1, column=1, sticky='ew')
        
        ttk.Label(table_frame, text="Values:").grid(row=2, column=0, sticky='w')
        self.table_values_var = tk.StringVar()
        ttk.Entry(table_frame, textvariable=self.table_values_var, width=60).grid(row=2, column=1, sticky='ew')
        
        table_frame.columnconfigure(1, weight=1)
        
        return start_row
        
    def create_results_section(self, parent, start_row):
        """Create results section"""
        # Section title
        title_label = ttk.Label(parent, text="Test Results", font=('Arial', 12, 'bold'))
        title_label.grid(row=start_row, column=0, columnspan=2, sticky='w', pady=(0, 10))
        start_row += 1
        
        results_frame = ttk.LabelFrame(parent, text="Results", padding=10)
        results_frame.grid(row=start_row, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        start_row += 1
        
        ttk.Label(results_frame, text="Names:").grid(row=0, column=0, sticky='w')
        self.results_names_var = tk.StringVar()
        ttk.Entry(results_frame, textvariable=self.results_names_var, width=60).grid(row=0, column=1, sticky='ew')
        
        ttk.Label(results_frame, text="Units:").grid(row=1, column=0, sticky='w')
        self.results_units_var = tk.StringVar()
        ttk.Entry(results_frame, textvariable=self.results_units_var, width=60).grid(row=1, column=1, sticky='ew')
        
        ttk.Label(results_frame, text="Values:").grid(row=2, column=0, sticky='w')
        self.results_values_var = tk.StringVar()
        ttk.Entry(results_frame, textvariable=self.results_values_var, width=60).grid(row=2, column=1, sticky='ew')
        
        results_frame.columnconfigure(1, weight=1)
        
        return start_row
        
    def create_specifications_section(self, parent, start_row):
        """Create specifications section"""
        # Section title
        title_label = ttk.Label(parent, text="Test Specifications", font=('Arial', 12, 'bold'))
        title_label.grid(row=start_row, column=0, columnspan=2, sticky='w', pady=(0, 10))
        start_row += 1
        
        specs_frame = ttk.LabelFrame(parent, text="Specifications", padding=10)
        specs_frame.grid(row=start_row, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        start_row += 1
        
        ttk.Label(specs_frame, text="Names:").grid(row=0, column=0, sticky='w')
        self.specs_names_var = tk.StringVar()
        ttk.Entry(specs_frame, textvariable=self.specs_names_var, width=60).grid(row=0, column=1, sticky='ew')
        
        ttk.Label(specs_frame, text="Units:").grid(row=1, column=0, sticky='w')
        self.specs_units_var = tk.StringVar()
        ttk.Entry(specs_frame, textvariable=self.specs_units_var, width=60).grid(row=1, column=1, sticky='ew')
        
        ttk.Label(specs_frame, text="Values:").grid(row=2, column=0, sticky='w')
        self.specs_values_var = tk.StringVar()
        ttk.Entry(specs_frame, textvariable=self.specs_values_var, width=60).grid(row=2, column=1, sticky='ew')
        
        ttk.Label(specs_frame, text="Connection:").grid(row=3, column=0, sticky='w')
        self.specs_connection_var = tk.StringVar()
        ttk.Entry(specs_frame, textvariable=self.specs_connection_var, width=60).grid(row=3, column=1, sticky='ew')
        
        ttk.Label(specs_frame, text="Type:").grid(row=4, column=0, sticky='w')
        self.specs_type_var = tk.StringVar()
        ttk.Entry(specs_frame, textvariable=self.specs_type_var, width=60).grid(row=4, column=1, sticky='ew')
        
        specs_frame.columnconfigure(1, weight=1)
        
        return start_row
        
    def create_calculations_section(self, parent, start_row):
        """Create calculations section"""
        # Section title
        title_label = ttk.Label(parent, text="Test Calculations", font=('Arial', 12, 'bold'))
        title_label.grid(row=start_row, column=0, columnspan=2, sticky='w', pady=(0, 10))
        start_row += 1
        
        calc_frame = ttk.LabelFrame(parent, text="Calculations", padding=10)
        calc_frame.grid(row=start_row, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        start_row += 1
        
        ttk.Label(calc_frame, text="Names:").grid(row=0, column=0, sticky='w')
        self.calc_names_var = tk.StringVar()
        ttk.Entry(calc_frame, textvariable=self.calc_names_var, width=60).grid(row=0, column=1, sticky='ew')
        
        ttk.Label(calc_frame, text="Units:").grid(row=1, column=0, sticky='w')
        self.calc_units_var = tk.StringVar()
        ttk.Entry(calc_frame, textvariable=self.calc_units_var, width=60).grid(row=1, column=1, sticky='ew')
        
        ttk.Label(calc_frame, text="Connection:").grid(row=2, column=0, sticky='w')
        self.calc_connection_var = tk.StringVar()
        ttk.Entry(calc_frame, textvariable=self.calc_connection_var, width=60).grid(row=2, column=1, sticky='ew')
        
        ttk.Label(calc_frame, text="Equation:").grid(row=3, column=0, sticky='w')
        self.calc_equation_var = tk.StringVar()
        ttk.Entry(calc_frame, textvariable=self.calc_equation_var, width=60).grid(row=3, column=1, sticky='ew')
        
        calc_frame.columnconfigure(1, weight=1)
        
        return start_row
        
    def create_generation_section(self, parent, start_row):
        """Create generation section"""
        # Section title
        title_label = ttk.Label(parent, text="File Generation", font=('Arial', 12, 'bold'))
        title_label.grid(row=start_row, column=0, columnspan=2, sticky='w', pady=(0, 10))
        start_row += 1
        
        # Output Directory Selection
        dir_frame = ttk.LabelFrame(parent, text="Output Directory", padding=10)
        dir_frame.grid(row=start_row, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        start_row += 1
        
        self.output_dir_var = tk.StringVar(value=os.getcwd())
        ttk.Entry(dir_frame, textvariable=self.output_dir_var, width=60).pack(side='left', fill='x', expand=True)
        ttk.Button(dir_frame, text="Browse", command=self.browse_output_dir).pack(side='right', padx=(5,0))
        
        # Generation Buttons
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=start_row, column=0, columnspan=2, sticky='ew', padx=5, pady=20)
        start_row += 1
        
        ttk.Button(button_frame, text="Save Test Data", command=self.save_test_data).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Load Test Data", command=self.load_test_data).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Generate Files", command=self.generate_files).pack(side='right', padx=5)
        
        # Status Text
        self.status_text = tk.Text(parent, height=8, width=80)
        self.status_text.grid(row=start_row, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        start_row += 1
        
        return start_row
        
    def browse_output_dir(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
            
    def collect_form_data(self):
        """Collect all data from the form"""
        data = {
            'basic_info': {
                'category': self.category_var.get(),
                'test_name': self.test_name_var.get(),
                'description': self.description_text.get('1.0', tk.END).strip()
            },
            'row_conditions': {
                'names': self.row_names_var.get(),
                'units': self.row_units_var.get(),
                'values': self.row_values_var.get()
            },
            'column_conditions': {
                'names': self.col_names_var.get(),
                'units': self.col_units_var.get(),
                'values': self.col_values_var.get()
            },
            'table_conditions': {
                'names': self.table_names_var.get(),
                'units': self.table_units_var.get(),
                'values': self.table_values_var.get()
            },
            'results': {
                'names': self.results_names_var.get(),
                'units': self.results_units_var.get(),
                'values': self.results_values_var.get()
            },
            'specifications': {
                'names': self.specs_names_var.get(),
                'units': self.specs_units_var.get(),
                'values': self.specs_values_var.get(),
                'connection': self.specs_connection_var.get(),
                'type': self.specs_type_var.get()
            },
            'calculations': {
                'names': self.calc_names_var.get(),
                'units': self.calc_units_var.get(),
                'connection': self.calc_connection_var.get(),
                'equation': self.calc_equation_var.get()
            }
        }
        return data
        
    def save_test_data(self):
        """Save current form data to JSON file"""
        data = self.collect_form_data()
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Save Test Data"
        )
        if filename:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2)
            self.status_text.insert(tk.END, f"Test data saved to {filename}\n")
            
    def load_test_data(self):
        """Load test data from JSON file"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json")],
            title="Load Test Data"
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                self.populate_form(data)
                self.status_text.insert(tk.END, f"Test data loaded from {filename}\n")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load test data: {str(e)}")
                
    def populate_form(self, data):
        """Populate form with loaded data"""
        # Basic info
        self.category_var.set(data.get('basic_info', {}).get('category', ''))
        self.test_name_var.set(data.get('basic_info', {}).get('test_name', ''))
        self.description_text.delete('1.0', tk.END)
        self.description_text.insert('1.0', data.get('basic_info', {}).get('description', ''))
        
        # Row conditions
        self.row_names_var.set(data.get('row_conditions', {}).get('names', ''))
        self.row_units_var.set(data.get('row_conditions', {}).get('units', ''))
        self.row_values_var.set(data.get('row_conditions', {}).get('values', ''))
        
        # Column conditions
        self.col_names_var.set(data.get('column_conditions', {}).get('names', ''))
        self.col_units_var.set(data.get('column_conditions', {}).get('units', ''))
        self.col_values_var.set(data.get('column_conditions', {}).get('values', ''))
        
        # Table conditions
        self.table_names_var.set(data.get('table_conditions', {}).get('names', ''))
        self.table_units_var.set(data.get('table_conditions', {}).get('units', ''))
        self.table_values_var.set(data.get('table_conditions', {}).get('values', ''))
        
        # Results
        self.results_names_var.set(data.get('results', {}).get('names', ''))
        self.results_units_var.set(data.get('results', {}).get('units', ''))
        self.results_values_var.set(data.get('results', {}).get('values', ''))
        
        # Specifications
        self.specs_names_var.set(data.get('specifications', {}).get('names', ''))
        self.specs_units_var.set(data.get('specifications', {}).get('units', ''))
        self.specs_values_var.set(data.get('specifications', {}).get('values', ''))
        self.specs_connection_var.set(data.get('specifications', {}).get('connection', ''))
        self.specs_type_var.set(data.get('specifications', {}).get('type', ''))
        
        # Calculations
        self.calc_names_var.set(data.get('calculations', {}).get('names', ''))
        self.calc_units_var.set(data.get('calculations', {}).get('units', ''))
        self.calc_connection_var.set(data.get('calculations', {}).get('connection', ''))
        self.calc_equation_var.set(data.get('calculations', {}).get('equation', ''))
        
    def generate_files(self):
        """Generate CSV and LaTeX files from form data"""
        data = self.collect_form_data()
        
        # Validate required fields
        if not data['basic_info']['category'] or not data['basic_info']['test_name']:
            messagebox.showerror("Error", "Please fill in Category and Test Name")
            return
            
        self.status_text.insert(tk.END, "Starting file generation...\n")
        self.status_text.update()
        
        try:
            # Create directory structure
            self.create_directory_structure(data)
            
            # Generate CSV files
            self.generate_csv_files(data)
            
            # Generate LaTeX files
            self.generate_latex_files(data)
            
            self.status_text.insert(tk.END, "File generation completed successfully!\n")
            messagebox.showinfo("Success", "Files generated successfully!")
            
        except Exception as e:
            error_msg = f"Error generating files: {str(e)}\n"
            self.status_text.insert(tk.END, error_msg)
            messagebox.showerror("Error", error_msg)
            
    def create_directory_structure(self, data):
        """Create the directory structure for the test"""
        base_dir = self.output_dir_var.get()
        category = data['basic_info']['category']
        test_name = data['basic_info']['test_name'].replace(' ', '_').lower()
        
        # Create main directories
        test_dir = os.path.join(base_dir, "tests", category, test_name)
        csv_dir = os.path.join(test_dir, "csv")
        images_dir = os.path.join(test_dir, "images")
        latex_dir = os.path.join(test_dir, "latex")
        
        for directory in [csv_dir, images_dir, latex_dir]:
            os.makedirs(directory, exist_ok=True)
            
        self.test_dir = test_dir
        self.csv_dir = csv_dir
        self.latex_dir = latex_dir
        
        self.status_text.insert(tk.END, f"Created directory structure at: {test_dir}\n")
        
    def generate_csv_files(self, data):
        """Generate CSV files from the form data"""
        try:
            # Parse all data fields
            parsed_data = self._parse_all_data(data)
            
            # Generate different CSV files based on the data
            csv_files_created = []
            
            # 1. Generate Row Conditions CSV
            if any(parsed_data['row_conditions'].values()):
                csv_files_created.append(self._create_conditions_csv(parsed_data['row_conditions'], 'row_conditions.csv'))
            
            # 2. Generate Column Conditions CSV
            if any(parsed_data['column_conditions'].values()):
                csv_files_created.append(self._create_conditions_csv(parsed_data['column_conditions'], 'column_conditions.csv'))
            
            # 3. Generate Table Conditions CSV
            if any(parsed_data['table_conditions'].values()):
                csv_files_created.append(self._create_conditions_csv(parsed_data['table_conditions'], 'table_conditions.csv'))
            
            # 4. Generate Results CSV
            if any(parsed_data['results'].values()):
                csv_files_created.append(self._create_results_csv(parsed_data['results'], 'results.csv'))
            
            # 5. Generate Specifications CSV
            if any(parsed_data['specifications'].values()):
                csv_files_created.append(self._create_specifications_csv(parsed_data['specifications'], 'specifications.csv'))
            
            # 6. Generate Calculations CSV
            if any(parsed_data['calculations'].values()):
                csv_files_created.append(self._create_calculations_csv(parsed_data['calculations'], 'calculations.csv'))
            
            # 7. Generate Tables metadata CSV
            if csv_files_created:
                self._create_tables_metadata_csv(csv_files_created)
            
            # 8. Generate Equipment Used CSV (placeholder)
            self._create_equipment_csv()
            
            self.status_text.insert(tk.END, f"Generated {len(csv_files_created)} CSV files\n")
            
        except Exception as e:
            raise Exception(f"CSV generation failed: {str(e)}")
    
    def _parse_all_data(self, data):
        """Parse all form data using DataParser"""
        parsed = {}
        
        # Parse each section
        for section_name, section_data in data.items():
            if section_name == 'basic_info':
                parsed[section_name] = section_data
                continue
                
            parsed[section_name] = {}
            for field_name, field_value in section_data.items():
                parsed[section_name][field_name] = DataParser.parse_value(field_value)
        
        return parsed
    
    def _create_conditions_csv(self, conditions_data, filename):
        """Create CSV file for conditions (row/column/table)"""
        csv_path = os.path.join(self.csv_dir, filename)
        
        # Get parsed data
        names = conditions_data.get('names', [])
        units = conditions_data.get('units', [])
        values = conditions_data.get('values', [])
        
        # Ensure all are lists
        if not isinstance(names, list):
            names = [names] if names else []
        if not isinstance(units, list):
            units = [units] if units else []
        if not isinstance(values, list):
            values = [values] if values else []
        
        # Create CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['Name', 'Unit', 'Value'])
            
            # Write data rows
            max_len = max(len(names), len(units), len(values))
            for i in range(max_len):
                name = names[i] if i < len(names) else ''
                unit = units[i] if i < len(units) else ''
                value = values[i] if i < len(values) else ''
                
                # Handle 2D arrays in values
                if isinstance(value, list):
                    value = str(value)
                
                writer.writerow([name, unit, value])
        
        return {'file_name': filename, 'title': filename.replace('.csv', '').replace('_', ' ').title(), 'caption': f"Test {filename.replace('.csv', '').replace('_', ' ')}"}
    
    def _create_results_csv(self, results_data, filename):
        """Create CSV file for results"""
        csv_path = os.path.join(self.csv_dir, filename)
        
        # Get parsed data
        names = results_data.get('names', [])
        units = results_data.get('units', [])
        values = results_data.get('values', [])
        
        # Ensure all are lists
        if not isinstance(names, list):
            names = [names] if names else []
        if not isinstance(units, list):
            units = [units] if units else []
        if not isinstance(values, list):
            values = [values] if values else []
        
        # Create CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['Parameter', 'Unit', 'Measured Value'])
            
            # Write data rows
            max_len = max(len(names), len(units), len(values))
            for i in range(max_len):
                name = names[i] if i < len(names) else ''
                unit = units[i] if i < len(units) else ''
                value = values[i] if i < len(values) else ''
                
                # Handle 2D arrays in values
                if isinstance(value, list):
                    value = str(value)
                
                writer.writerow([name, unit, value])
        
        return {'file_name': filename, 'title': 'Test Results', 'caption': 'Measured test results'}
    
    def _create_specifications_csv(self, specs_data, filename):
        """Create CSV file for specifications"""
        csv_path = os.path.join(self.csv_dir, filename)
        
        # Get parsed data
        names = specs_data.get('names', [])
        units = specs_data.get('units', [])
        values = specs_data.get('values', [])
        connections = specs_data.get('connection', [])
        types = specs_data.get('type', [])
        
        # Ensure all are lists
        for data_list in [names, units, values, connections, types]:
            if not isinstance(data_list, list):
                data_list = [data_list] if data_list else []
        
        # Create CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['Parameter', 'Unit', 'Specification', 'Connection', 'Type'])
            
            # Write data rows
            max_len = max(len(names), len(units), len(values), len(connections), len(types))
            for i in range(max_len):
                name = names[i] if i < len(names) else ''
                unit = units[i] if i < len(units) else ''
                value = values[i] if i < len(values) else ''
                connection = connections[i] if i < len(connections) else ''
                spec_type = types[i] if i < len(types) else ''
                
                # Handle 2D arrays in values
                if isinstance(value, list):
                    value = str(value)
                
                writer.writerow([name, unit, value, connection, spec_type])
        
        return {'file_name': filename, 'title': 'Test Specifications', 'caption': 'Test specifications and limits'}
    
    def _create_calculations_csv(self, calc_data, filename):
        """Create CSV file for calculations"""
        csv_path = os.path.join(self.csv_dir, filename)
        
        # Get parsed data
        names = calc_data.get('names', [])
        units = calc_data.get('units', [])
        connections = calc_data.get('connection', [])
        equations = calc_data.get('equation', [])
        
        # Ensure all are lists
        for data_list in [names, units, connections, equations]:
            if not isinstance(data_list, list):
                data_list = [data_list] if data_list else []
        
        # Create CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['Parameter', 'Unit', 'Connection', 'Equation'])
            
            # Write data rows
            max_len = max(len(names), len(units), len(connections), len(equations))
            for i in range(max_len):
                name = names[i] if i < len(names) else ''
                unit = units[i] if i < len(units) else ''
                connection = connections[i] if i < len(connections) else ''
                equation = equations[i] if i < len(equations) else ''
                
                writer.writerow([name, unit, connection, equation])
        
        return {'file_name': filename, 'title': 'Test Calculations', 'caption': 'Calculated parameters and equations'}
    
    def _create_tables_metadata_csv(self, csv_files_info):
        """Create tables.csv metadata file"""
        tables_path = os.path.join(self.csv_dir, 'tables.csv')
        
        with open(tables_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['file_name', 'title', 'caption'])
            
            # Write data for each CSV file
            for file_info in csv_files_info:
                writer.writerow([file_info['file_name'], file_info['title'], file_info['caption']])
    
    def _create_equipment_csv(self):
        """Create equipment_used.csv placeholder"""
        equipment_path = os.path.join(self.csv_dir, 'equipment_used.csv')
        
        with open(equipment_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Write header
            writer.writerow(['Equipment', 'Model', 'Serial Number', 'Calibration Date'])
            
            # Write placeholder data
            writer.writerow(['', '', '', ''])
        
    def generate_latex_files(self, data):
        """Generate LaTeX files from the form data"""
        try:
            # Parse all data fields
            parsed_data = self._parse_all_data(data)
            
            # Generate main LaTeX file
            self._create_main_latex_file(data, parsed_data)
            
            self.status_text.insert(tk.END, "Generated LaTeX files\n")
            
        except Exception as e:
            raise Exception(f"LaTeX generation failed: {str(e)}")
    
    def _create_main_latex_file(self, data, parsed_data):
        """Create the main LaTeX file for the test"""
        latex_path = os.path.join(self.latex_dir, 'test.tex')
        
        # Basic info
        test_name = data['basic_info']['test_name']
        test_category = data['basic_info']['category']
        test_description = data['basic_info']['description']
        
        # Generate LaTeX content
        latex_content = self._generate_latex_content(test_name, test_category, test_description, parsed_data)
        
        # Write to file
        with open(latex_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
    
    def _generate_latex_content(self, test_name, test_category, test_description, parsed_data):
        """Generate the complete LaTeX content"""
        
        latex_content = f"""\\documentclass{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{geometry}}
\\usepackage{{booktabs}}
\\usepackage{{longtable}}
\\usepackage{{array}}
\\usepackage{{amsmath}}
\\usepackage{{graphicx}}
\\usepackage{{float}}
\\usepackage{{caption}}

\\geometry{{margin=1in}}

\\title{{{test_name}}}
\\author{{Test Report Generator}}
\\date{{\\today}}

\\begin{{document}}

\\maketitle

\\section{{Test Information}}
\\begin{{itemize}}
    \\item \\textbf{{Test Name:}} {test_name}
    \\item \\textbf{{Category:}} {test_category}
    \\item \\textbf{{Description:}} {test_description}
\\end{{itemize}}

"""

        # Add sections based on available data
        if any(parsed_data['row_conditions'].values()):
            latex_content += self._generate_conditions_latex_section("Row Conditions", parsed_data['row_conditions'])
        
        if any(parsed_data['column_conditions'].values()):
            latex_content += self._generate_conditions_latex_section("Column Conditions", parsed_data['column_conditions'])
        
        if any(parsed_data['table_conditions'].values()):
            latex_content += self._generate_conditions_latex_section("Table Conditions", parsed_data['table_conditions'])
        
        if any(parsed_data['results'].values()):
            latex_content += self._generate_results_latex_section(parsed_data['results'])
        
        if any(parsed_data['specifications'].values()):
            latex_content += self._generate_specifications_latex_section(parsed_data['specifications'])
        
        if any(parsed_data['calculations'].values()):
            latex_content += self._generate_calculations_latex_section(parsed_data['calculations'])
        
        latex_content += """
\\end{document}
"""
        
        return latex_content
    
    def _generate_conditions_latex_section(self, section_title, conditions_data):
        """Generate LaTeX section for conditions"""
        names = conditions_data.get('names', [])
        units = conditions_data.get('units', [])
        values = conditions_data.get('values', [])
        
        # Ensure all are lists
        if not isinstance(names, list):
            names = [names] if names else []
        if not isinstance(units, list):
            units = [units] if units else []
        if not isinstance(values, list):
            values = [values] if values else []
        
        if not names and not units and not values:
            return ""
        
        latex_section = f"""
\\section{{{section_title}}}

\\begin{{longtable}}{{|l|l|l|}}
\\hline
\\textbf{{Name}} & \\textbf{{Unit}} & \\textbf{{Value}} \\\\
\\hline
\\endfirsthead

\\hline
\\textbf{{Name}} & \\textbf{{Unit}} & \\textbf{{Value}} \\\\
\\hline
\\endhead

\\hline
\\endfoot

\\hline
\\endlastfoot

"""
        
        # Add data rows
        max_len = max(len(names), len(units), len(values))
        for i in range(max_len):
            name = self._latex_escape(str(names[i])) if i < len(names) else ''
            unit = self._latex_escape(str(units[i])) if i < len(units) else ''
            value = self._latex_escape(str(values[i])) if i < len(values) else ''
            
            latex_section += f"{name} & {unit} & {value} \\\\\n\\hline\n"
        
        latex_section += """\\end{longtable}

"""
        
        return latex_section
    
    def _generate_results_latex_section(self, results_data):
        """Generate LaTeX section for results"""
        names = results_data.get('names', [])
        units = results_data.get('units', [])
        values = results_data.get('values', [])
        
        # Ensure all are lists
        if not isinstance(names, list):
            names = [names] if names else []
        if not isinstance(units, list):
            units = [units] if units else []
        if not isinstance(values, list):
            values = [values] if values else []
        
        if not names and not units and not values:
            return ""
        
        latex_section = f"""
\\section{{Test Results}}

\\begin{{longtable}}{{|l|l|l|}}
\\hline
\\textbf{{Parameter}} & \\textbf{{Unit}} & \\textbf{{Measured Value}} \\\\
\\hline
\\endfirsthead

\\hline
\\textbf{{Parameter}} & \\textbf{{Unit}} & \\textbf{{Measured Value}} \\\\
\\hline
\\endhead

\\hline
\\endfoot

\\hline
\\endlastfoot

"""
        
        # Add data rows
        max_len = max(len(names), len(units), len(values))
        for i in range(max_len):
            name = self._latex_escape(str(names[i])) if i < len(names) else ''
            unit = self._latex_escape(str(units[i])) if i < len(units) else ''
            value = self._latex_escape(str(values[i])) if i < len(values) else ''
            
            latex_section += f"{name} & {unit} & {value} \\\\\n\\hline\n"
        
        latex_section += """\\end{longtable}

"""
        
        return latex_section
    
    def _generate_specifications_latex_section(self, specs_data):
        """Generate LaTeX section for specifications"""
        names = specs_data.get('names', [])
        units = specs_data.get('units', [])
        values = specs_data.get('values', [])
        connections = specs_data.get('connection', [])
        types = specs_data.get('type', [])
        
        # Ensure all are lists
        for data_list in [names, units, values, connections, types]:
            if not isinstance(data_list, list):
                data_list = [data_list] if data_list else []
        
        if not names and not units and not values:
            return ""
        
        latex_section = f"""
\\section{{Test Specifications}}

\\begin{{longtable}}{{|l|l|l|l|l|}}
\\hline
\\textbf{{Parameter}} & \\textbf{{Unit}} & \\textbf{{Specification}} & \\textbf{{Connection}} & \\textbf{{Type}} \\\\
\\hline
\\endfirsthead

\\hline
\\textbf{{Parameter}} & \\textbf{{Unit}} & \\textbf{{Specification}} & \\textbf{{Connection}} & \\textbf{{Type}} \\\\
\\hline
\\endhead

\\hline
\\endfoot

\\hline
\\endlastfoot

"""
        
        # Add data rows
        max_len = max(len(names), len(units), len(values), len(connections), len(types))
        for i in range(max_len):
            name = self._latex_escape(str(names[i])) if i < len(names) else ''
            unit = self._latex_escape(str(units[i])) if i < len(units) else ''
            value = self._latex_escape(str(values[i])) if i < len(values) else ''
            connection = self._latex_escape(str(connections[i])) if i < len(connections) else ''
            spec_type = self._latex_escape(str(types[i])) if i < len(types) else ''
            
            latex_section += f"{name} & {unit} & {value} & {connection} & {spec_type} \\\\\n\\hline\n"
        
        latex_section += """\\end{longtable}

"""
        
        return latex_section
    
    def _generate_calculations_latex_section(self, calc_data):
        """Generate LaTeX section for calculations"""
        names = calc_data.get('names', [])
        units = calc_data.get('units', [])
        connections = calc_data.get('connection', [])
        equations = calc_data.get('equation', [])
        
        # Ensure all are lists
        for data_list in [names, units, connections, equations]:
            if not isinstance(data_list, list):
                data_list = [data_list] if data_list else []
        
        if not names and not units and not connections and not equations:
            return ""
        
        latex_section = f"""
\\section{{Test Calculations}}

\\begin{{longtable}}{{|l|l|l|l|}}
\\hline
\\textbf{{Parameter}} & \\textbf{{Unit}} & \\textbf{{Connection}} & \\textbf{{Equation}} \\\\
\\hline
\\endfirsthead

\\hline
\\textbf{{Parameter}} & \\textbf{{Unit}} & \\textbf{{Connection}} & \\textbf{{Equation}} \\\\
\\hline
\\endhead

\\hline
\\endfoot

\\hline
\\endlastfoot

"""
        
        # Add data rows
        max_len = max(len(names), len(units), len(connections), len(equations))
        for i in range(max_len):
            name = self._latex_escape(str(names[i])) if i < len(names) else ''
            unit = self._latex_escape(str(units[i])) if i < len(units) else ''
            connection = self._latex_escape(str(connections[i])) if i < len(connections) else ''
            equation = self._latex_escape(str(equations[i])) if i < len(equations) else ''
            
            latex_section += f"{name} & {unit} & {connection} & {equation} \\\\\n\\hline\n"
        
        latex_section += """\\end{longtable}

"""
        
        return latex_section
    
    def _latex_escape(self, text):
        """Escape special LaTeX characters"""
        if not text:
            return ""
        
        # Handle list representations
        if isinstance(text, list):
            text = str(text)
        
        text = str(text)
        
        # Escape special LaTeX characters
        replacements = {
            '\\': '\\textbackslash{}',
            '{': '\\{',
            '}': '\\}',
            '$': '\\$',
            '&': '\\&',
            '%': '\\%',
            '#': '\\#',
            '^': '\\textasciicircum{}',
            '_': '\\_',
            '~': '\\textasciitilde{}'
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        return text

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TestReportGenerator(root)
    root.mainloop()