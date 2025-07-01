# ╭──────────────────────────────────────────────────────────────────────────╮
# │                    Engineering Test Report Generator                     │
# │                            Model Component (MVC)                        │
# ├──────────────────────────────────────────────────────────────────────────┤
# │ CLASS: Model                                                             │
# │   Purpose: Data management and file operations for test reports         │
# │                                                                          │
# │ METHODS:                                                                 │
# │   __init__(report_path: str = None) -> None                             │
# │     Purpose: Initialize model with optional report path                 │
# │     Inputs:  report_path - Path to existing report directory            │
# │     Outputs: None                                                        │
# │                                                                          │
# │   _initialize_paths() -> None                                            │
# │     Purpose: Set up file paths based on report structure                │
# │     Inputs:  None (uses self.report_path)                               │
# │     Outputs: None (sets self.tests_path, cover_page_path, etc.)         │
# │                                                                          │
# │   _load_existing_data() -> None                                          │
# │     Purpose: Load existing data from report structure                   │
# │     Inputs:  None                                                        │
# │     Outputs: None (populates self.test_selections, cover_page_data)     │
# │                                                                          │
# │   _load_cover_page_data() -> None                                        │
# │     Purpose: Load cover page JSON files into data structures            │
# │     Inputs:  None                                                        │
# │     Outputs: None (populates self.cover_page_data)                      │
# │                                                                          │
# │   get_cover_page_section(section_name: str) -> list                     │
# │     Purpose: Get cover page section data for tksheet display            │
# │     Inputs:  section_name - Name of cover page section                  │
# │     Outputs: List of lists (tksheet format data)                        │
# │                                                                          │
# │   save_cover_page_section(section_name: str, tksheet_data: list) -> None│
# │     Purpose: Save tksheet data to cover page section                    │
# │     Inputs:  section_name - Section identifier                          │
# │              tksheet_data - Data in tksheet format                      │
# │     Outputs: None (saves to JSON file)                                  │
# │                                                                          │
# │   get_cover_page_dataframe(section_name: str) -> pd.DataFrame           │
# │     Purpose: Convert cover page section to pandas DataFrame             │
# │     Inputs:  section_name - Section identifier                          │
# │     Outputs: pandas DataFrame for LaTeX generation                      │
# │                                                                          │
# │   initialize_default_cover_page() -> None                               │
# │     Purpose: Initialize default cover page structure with headers       │
# │     Inputs:  None                                                        │
# │     Outputs: None (creates default JSON files)                          │
# │                                                                          │
# │   create_report() -> None                                                │
# │     Purpose: Generate the complete report from selected tests           │
# │     Inputs:  None                                                        │
# │     Outputs: None (creates PDF report)                                  │
# │                                                                          │
# │   send_report() -> None                                                  │
# │     Purpose: Send or distribute the generated report                    │
# │     Inputs:  None                                                        │
# │     Outputs: None                                                        │
# │                                                                          │
# │ ATTRIBUTES:                                                              │
# │   report_path: str - Base path for the report project                   │
# │   test_selections: dict - Selected tests from test_selections.json      │
# │   cover_page_data: dict - Cover page information                        │
# │   test_data: dict - All test data organized by category/test            │
# │   tests_path: str - Path to tests directory                             │
# │   cover_page_path: str - Path to cover_page directory                   │
# │   report_output_path: str - Path to report output directory             │
# │                                                                          │
# │ FILE STRUCTURE MANAGED:                                                  │
# │   tests/[category]/[test]/csv/ - Test data and equipment files          │
# │   tests/[category]/[test]/images/ - Test images and metadata            │
# │   tests/[category]/[test]/latex/ - Generated LaTeX files                │
# │   cover_page/ - JSON files for cover page sections                      │
# │   report/ - Final generated PDF and LaTeX source                        │
# ╰──────────────────────────────────────────────────────────────────────────╯

# ╭──────────────────────────────────────────────────────────────────────────╮
# │ Test Report Model Structure                                              │
# ├──────────────────────────────────────────────────────────────────────────┤
# │ This model holds all data for a selected test report.                    │
# │ The data is organized in a specific folder structure as follows:         │
# ╰──────────────────────────────────────────────────────────────────────────╯

# tests/
# ├── input/                    # Category (e.g. input, output, safety, etc.)
# │   ├── input_current/        # Individual test
# │   │   ├── csv/
# │   │   │   ├── data1.csv             # data table #1 for the test
# │   │   │   ├── data2.csv             # data table #2 for the test
# │   │   │   └── equipment_used.csv   # Equipment used in the test
# │   │   ├── images/
# │   │   │   ├── *.png, *.jpg         # Test images
# │   │   │   └── images.csv           # file_name, title, caption
# │   │   └── latex/
# │   │       └── test.tex             # Generated LaTeX file for the test
# │   └── ...
# ├── output/
# │   └── ...
# ├── safety/
# │   └── ...
# └── test_selections.json     # Selected tests (checkbox states)

# cover_page/
# ├── equipment_used.json
# ├── general_specifications.json
# ├── product_information.json
# ├── testing_and_review.json
# └── logo.png

# report/
# ├── report.pdf                      # Final generated PDF report
# └── latex_report/                   # LaTeX source for the report
#     ├── main.tex
#     ├── *.tex, *.sty, *.bib
#     └── images/, tables/, etc.


import pandas as pd

class Model:
    def __init__(self, report_path: str = None) -> None:
        # Base path for the report project
        self.report_path = report_path
        
        # Main data containers
        self.test_selections = {}  # Selected tests from test_selections.json
        self.cover_page_data = {}  # Cover page information
        self.test_data = {}        # All test data organized by category/test
        
        # File paths
        self.tests_path = None
        self.cover_page_path = None
        self.report_output_path = None
        
        # Initialize paths if report_path is provided
        if self.report_path:
            self._initialize_paths()
            self._load_existing_data()
    
    def _initialize_paths(self):
        """Set up the file paths based on the report structure"""
        import os
        self.tests_path = os.path.join(self.report_path, 'tests')
        self.cover_page_path = os.path.join(self.report_path, 'cover_page')
        self.report_output_path = os.path.join(self.report_path, 'report')
    
    def _load_existing_data(self):
        """Load existing data from the report structure"""
        import json
        import os
        
        # Load test selections if they exist
        selections_file = os.path.join(self.tests_path, 'test_selections.json')
        if os.path.exists(selections_file):
            with open(selections_file, 'r') as f:
                self.test_selections = json.load(f)
        
        # Load cover page data if it exists
        if os.path.exists(self.cover_page_path):
            self._load_cover_page_data()
    
    def _load_cover_page_data(self):
        """Load cover page JSON files into data structures"""
        import os
        import json
        
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

    def get_cover_page_section(self, section_name: str):
        """Get cover page section data for tksheet display"""
        return self.cover_page_data.get(section_name, [])
    
    def save_cover_page_section(self, section_name: str, tksheet_data: list):
        """Save tksheet data to cover page section"""
        import json
        import os
        
        # Update in-memory data
        self.cover_page_data[section_name] = tksheet_data
        
        # Save to file
        if self.cover_page_path:
            os.makedirs(self.cover_page_path, exist_ok=True)
            file_path = os.path.join(self.cover_page_path, f"{section_name}.json")
            with open(file_path, 'w') as f:
                json.dump(tksheet_data, f, indent=2)
    
    def get_cover_page_dataframe(self, section_name: str):
        """Convert cover page section to pandas DataFrame"""
        data = self.cover_page_data.get(section_name, [])
        if not data:
            return pd.DataFrame()
        
        # If data has headers (first row), use them as column names
        if len(data) > 1:
            headers = data[0]
            rows = data[1:]
            return pd.DataFrame(rows, columns=headers)
        else:
            return pd.DataFrame(data)
    
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

    def create_report(self):
        """Generate the complete report from selected tests and cover page data"""
        pass

    def send_report(self):
        """Send or distribute the generated report"""
        pass
