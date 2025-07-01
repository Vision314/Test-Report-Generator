# ╭──────────────────────────────────────────────────────────────────────────╮
# │                    Engineering Test Report Generator                     │
# │                          Controller Component (MVC)                     │
# ├──────────────────────────────────────────────────────────────────────────┤
# │ CLASS: Controller                                                        │
# │   Purpose: Business logic coordinator between Model and View            │
# │                                                                          │
# │ INITIALIZATION METHODS:                                                  │
# │   __init__(model: Model, view: View) -> None                            │
# │     Purpose: Initialize controller and connect MVC components           │
# │     Inputs:  model - Model instance, view - View instance               │
# │     Outputs: None                                                        │
# │                                                                          │
# │   initialize_view() -> None                                              │
# │     Purpose: Initialize view with default data and populate tree        │
# │     Inputs:  None                                                        │
# │     Outputs: None                                                        │
# │                                                                          │
# │   run() -> None                                                          │
# │     Purpose: Start the application main loop                            │
# │     Inputs:  None                                                        │
# │     Outputs: None                                                        │
# │                                                                          │
# │ FILE OPERATION METHODS:                                                  │
# │   new_report() -> None                                                   │
# │     Purpose: Create new report with directory structure                 │
# │     Inputs:  None (prompts user for directory and name)                 │
# │     Outputs: None (creates report files and folders)                    │
# │                                                                          │
# │   open_report() -> None                                                  │
# │     Purpose: Open existing report from directory                        │
# │     Inputs:  None (prompts user for directory selection)                │
# │     Outputs: None (loads report data into model)                        │
# │                                                                          │
# │   save_current() -> None                                                 │
# │     Purpose: Save current sheet data to files                           │
# │     Inputs:  None                                                        │
# │     Outputs: None (saves data via model)                                │
# │                                                                          │
# │ TREE OPERATION METHODS:                                                  │
# │   on_tree_selection(item: str) -> None                                  │
# │     Purpose: Handle tree item selection and load appropriate content    │
# │     Inputs:  item - Tree item identifier                                │
# │     Outputs: None (updates view content)                                │
# │                                                                          │
# │   on_tree_click(item: str) -> None                                      │
# │     Purpose: Handle tree item clicks for checkbox functionality         │
# │     Inputs:  item - Tree item identifier                                │
# │     Outputs: None (toggles test selection)                              │
# │                                                                          │
# │ CONTENT LOADING METHODS:                                                 │
# │   load_cover_page() -> None                                              │
# │     Purpose: Load cover page sections into center view                  │
# │     Inputs:  None                                                        │
# │     Outputs: None (populates view with cover page data)                 │
# │                                                                          │
# │   load_category_tests(category: str) -> None                            │
# │     Purpose: Load all tests for a category                              │
# │     Inputs:  category - Category name                                   │
# │     Outputs: None (shows category overview)                             │
# │                                                                          │
# │   load_test_data(category: str, test_name: str) -> None                 │
# │     Purpose: Load data for specific test                                │
# │     Inputs:  category - Category name, test_name - Test identifier      │
# │     Outputs: None (loads test-specific data)                            │
# │                                                                          │
# │   load_equipment_for_current_test() -> None                             │
# │     Purpose: Load equipment list for current test/section               │
# │     Inputs:  None                                                        │
# │     Outputs: None (populates equipment pane)                            │
# │                                                                          │
# │ TEST MANAGEMENT METHODS:                                                 │
# │   add_test() -> None                                                     │
# │     Purpose: Add new test to category                                   │
# │     Inputs:  None (prompts user for category and test name)             │
# │     Outputs: None (creates test directory structure)                    │
# │                                                                          │
# │   delete_test() -> None                                                  │
# │     Purpose: Delete selected test with confirmation                     │
# │     Inputs:  None                                                        │
# │     Outputs: None (removes test files and folders)                      │
# │                                                                          │
# │   add_section() -> None                                                  │
# │     Purpose: Add new section to current test                            │
# │     Inputs:  None                                                        │
# │     Outputs: None (adds data section)                                   │
# │                                                                          │
# │ EQUIPMENT MANAGEMENT METHODS:                                            │
# │   on_equipment_toggle(equipment_id: str, is_selected: bool) -> None     │
# │     Purpose: Handle equipment checkbox toggle                           │
# │     Inputs:  equipment_id - Equipment identifier                        │
# │              is_selected - Selection state                              │
# │     Outputs: None (saves equipment selection state)                     │
# │                                                                          │
# │   refresh_equipment() -> None                                            │
# │     Purpose: Refresh equipment list display                             │
# │     Inputs:  None                                                        │
# │     Outputs: None (reloads equipment data)                              │
# │                                                                          │
# │   add_equipment() -> None                                                │
# │     Purpose: Add new equipment to database                              │
# │     Inputs:  None (prompts user for equipment details)                  │
# │     Outputs: None (saves equipment to database)                         │
# │                                                                          │
# │ REPORT GENERATION METHODS:                                               │
# │   generate_report() -> None                                              │
# │     Purpose: Generate final PDF report from selected tests              │
# │     Inputs:  None                                                        │
# │     Outputs: None (creates PDF via model)                               │
# │                                                                          │
# │   send_report() -> None                                                  │
# │     Purpose: Send or distribute generated report                        │
# │     Inputs:  None                                                        │
# │     Outputs: None (sends report via model)                              │
# │                                                                          │
# │ HELPER METHODS:                                                          │
# │   ensure_test_structure() -> None                                        │
# │     Purpose: Ensure test directory structure exists                     │
# │     Inputs:  None                                                        │
# │     Outputs: None (creates missing directories)                         │
# │                                                                          │
# │   create_test_structure(category: str, test_name: str) -> None          │
# │     Purpose: Create folder structure for a test                         │
# │     Inputs:  category - Test category, test_name - Test identifier      │
# │     Outputs: None (creates csv/, images/, latex/ folders and files)     │
# │                                                                          │
# │ ATTRIBUTES:                                                              │
# │   model: Model - Data management component                               │
# │   view: View - GUI component                                             │
# │   current_selection: Current selected item (category/test tuple)        │
# │   current_selection_type: Type of selection ('category'/'test'/'cover_page')│
# │   test_structure: Dict defining available test categories and tests     │
# │                                                                          │
# │ TEST STRUCTURE:                                                          │
# │   cover_page: Cover page sections                                       │
# │   input: Input characteristic tests (current, power, efficiency, etc.)  │
# │   output: Output characteristic tests (regulation, ripple, etc.)        │
# │   protections: Protection tests (overvoltage, overcurrent, etc.)        │
# │   safety: Safety tests (dielectric, leakage current, etc.)              │
# │   emc: EMC tests (emissions, immunity, etc.)                            │
# │                                                                          │
# │ WORKFLOW:                                                                │
# │   1. User creates/opens report                                           │
# │   2. User selects tests in file tree                                    │
# │   3. User edits data in center pane sheets                              │
# │   4. User selects equipment in bottom pane                              │
# │   5. Controller auto-saves data on navigation                           │
# │   6. User generates final report                                        │
# ╰──────────────────────────────────────────────────────────────────────────╯

from view import View
from model import Model
import os
import json

class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        
        # Set up bidirectional references
        self.view.set_controller(self)
        self.view.set_model(self.model)
        
        # Application state
        self.current_selection = None
        self.current_selection_type = None  # 'category', 'test', 'cover_page'
        
        # Test structure for file tree
        self.test_structure = {
            'cover_page': ['Cover Page'],
            'input': ['input_current', 'no_load_input_power', 'inrush_current', 'efficiency', 'power_factor'],
            'output': ['turn_on_delay', 'output_voltage_tolerance', 'load_regulation', 'line_regulation',
                      'ripple', 'transient_response', 'startup_overshoot', 'hold_up_time',
                      'aux_output_voltage_regulation', 'aux_output_current'],
            'protections': ['over_voltage_protection', 'over_current_protection', 'short_circuit_protection'],
            'safety': ['dielectric_withstand_voltage', 'output_touch_current', 'earth_leakage_current'],
            'emc': ['conducted_emissions', 'radiated_emissions', 'electrostatic_discharge_immunity',
                   'EFT_burst_immunity', 'line_surge_immunity', 'voltage_dip_immunity']
        }
        
        # Initialize the view
        self.initialize_view()

    def initialize_view(self):
        """Initialize the view with default data"""
        # Populate the file tree
        self.view.populate_tree(self.test_structure)
        
        # Show no report message if no model loaded
        if not self.model or not self.model.report_path:
            self.view.load_center_content('no_report', {})
            self.view.update_title()  # No report name
        else:
            # Load cover page by default
            self.load_cover_page()
            # Update title with report name
            report_name = os.path.basename(self.model.report_path)
            self.view.update_title(report_name)

    def run(self):
        """Start the application"""
        self.view.mainloop()

    # File operations
    def new_report(self):
        """Create a new report"""
        # Ask for parent directory
        parent_dir = self.view.ask_directory("Select parent directory for new report")
        if not parent_dir:
            return
        
        # Ask for report name
        report_name = self.view.ask_string("New Report", "Enter report name:")
        if not report_name:
            return
        
        # Create report directory
        report_path = os.path.join(parent_dir, report_name)
        try:
            os.makedirs(report_path, exist_ok=True)
            
            # Create new model with this path
            self.model = Model(report_path)
            self.view.set_model(self.model)
            
            # Initialize default structure
            self.model.initialize_default_cover_page()
            self.ensure_test_structure()
            
            # Refresh view
            self.load_cover_page()
            
            # Update title with report name
            self.view.update_title(report_name)
            
            self.view.show_message("Success", f"Report '{report_name}' created successfully!")
            
        except Exception as e:
            self.view.show_message("Error", f"Failed to create report: {str(e)}", "error")

    def open_report(self):
        """Open an existing report"""
        report_path = self.view.ask_directory("Select report directory")
        if not report_path:
            return
        
        try:
            # Load existing report
            self.model = Model(report_path)
            self.view.set_model(self.model)
            
            # Initialize if needed
            if not self.model.cover_page_data:
                self.model.initialize_default_cover_page()
            
            # Refresh view
            self.load_cover_page()
            
            # Update title with report name (extract folder name)
            report_name = os.path.basename(report_path)
            self.view.update_title(report_name)
            
            self.view.show_message("Success", "Report loaded successfully!")
            
        except Exception as e:
            self.view.show_message("Error", f"Failed to open report: {str(e)}", "error")

    def save_current(self):
        """Save current data"""
        if not self.model or not self.model.report_path:
            self.view.show_message("Warning", "No report loaded", "warning")
            return
        
        try:
            # Save all current sheet data
            for section_name in self.view.current_sheets:
                sheet_data = self.view.get_sheet_data(section_name)
                self.model.save_cover_page_section(section_name, sheet_data)
                
                # If equipment_used section was saved, refresh the equipment list
                if section_name == 'equipment_used':
                    self.load_equipment_for_current_test()
            
            self.view.show_message("Success", "Data saved successfully!")
            
        except Exception as e:
            self.view.show_message("Error", f"Failed to save: {str(e)}", "error")

    # Tree operations
    def on_tree_selection(self, item):
        """Handle tree item selection"""
        # Save current data before switching
        if self.current_selection:
            self.save_current()
        
        # Get item information
        item_text = self.view.tree.item(item, 'text')
        item_values = self.view.tree.item(item, 'values')
        parent = self.view.tree.parent(item)
        
        if parent == '':  # Category selected
            self.current_selection = item_values[0] if item_values else None
            self.current_selection_type = 'category'
            
            if self.current_selection == 'cover_page':
                self.load_cover_page()
            else:
                self.load_category_tests(self.current_selection)
                
        else:  # Test selected
            parent_values = self.view.tree.item(parent, 'values')
            category = parent_values[0] if parent_values else None
            test_name = item_values[0] if item_values else None
            
            self.current_selection = (category, test_name)
            self.current_selection_type = 'test'
            
            if category == 'cover_page':
                self.load_cover_page()
            else:
                self.load_test_data(category, test_name)

    def on_tree_click(self, item):
        """Handle tree item clicks (for checkbox functionality)"""
        # This could be used for enabling/disabling tests
        pass

    # Content loading
    def load_cover_page(self):
        """Load cover page sections"""
        if not self.model or not self.model.report_path:
            self.view.load_center_content('no_report', {})
            self.view.update_title()  # No report name
            return
        
        # Get all cover page sections
        sections = {}
        for section in ['product_information', 'general_specifications', 'testing_and_review', 'equipment_used']:
            sections[section] = self.model.get_cover_page_section(section)
        
        # Load into view
        self.view.load_center_content('cover_page', sections)
        
        # Load equipment list
        self.load_equipment_for_current_test()

    def load_category_tests(self, category):
        """Load all tests for a category"""
        # For now, just show a message
        # This could be expanded to show category overview
        pass

    def load_test_data(self, category, test_name):
        """Load data for a specific test"""
        if not self.model or not self.model.report_path:
            return
        
        # Load test data (implementation depends on test data structure)
        test_path = os.path.join(self.model.tests_path, category, test_name)
        
        # For now, just load equipment
        self.load_equipment_for_current_test()

    def load_equipment_for_current_test(self):
        """Load equipment list for current test/section"""
        equipment_data = []
        
        # If no model loaded, show empty equipment list
        if not self.model or not self.model.report_path:
            self.view.load_equipment_list(equipment_data)
            return
        
        try:
            # Equipment is always loaded from cover page equipment_used.json
            # regardless of whether we're viewing cover page or a specific test
            equipment_section = self.model.get_cover_page_section('equipment_used')
            print(f"DEBUG: Equipment section data: {equipment_section}")
            
            if equipment_section and len(equipment_section) > 1:  # Skip header row
                for i, row in enumerate(equipment_section[1:], 1):  # Skip header
                    print(f"DEBUG: Processing row {i}: {row}")
                    
                    if len(row) >= 7:  # Ensure row has all columns
                        # Convert all cells to strings and clean them
                        clean_row = [str(cell).strip() if cell else '' for cell in row]
                        print(f"DEBUG: Clean row: {clean_row}")
                        
                        # Only add if at least one field has meaningful data
                        if any(clean_row):
                            equipment_item = {
                                'id': f'equipment_{i}',
                                'equipment_type': clean_row[0],
                                'manufacturer': clean_row[1], 
                                'model': clean_row[2],
                                'description': clean_row[3],
                                'serial': clean_row[4],
                                'last_calibrated': clean_row[5],
                                'calibration_due': clean_row[6]
                            }
                            equipment_data.append(equipment_item)
                            print(f"DEBUG: Added equipment: {equipment_item}")
                    else:
                        print(f"DEBUG: Row {i} too short: {len(row)} columns")
        
        except Exception as e:
            print(f"Error loading equipment: {e}")
            # Show empty list on error
            equipment_data = []
        
        # Load equipment into view
        print(f"DEBUG: Final equipment_data being sent to view: {equipment_data}")
        self.view.load_equipment_list(equipment_data)

    # Test management
    def add_test(self):
        """Add a new test"""
        # Ask for category
        categories = list(self.test_structure.keys())
        categories.remove('cover_page')  # Can't add to cover page
        
        category = self.view.ask_string("Add Test", f"Enter category ({', '.join(categories)}):")
        if not category or category not in categories:
            return
        
        # Ask for test name
        test_name = self.view.ask_string("Add Test", "Enter test name:")
        if not test_name:
            return
        
        # Convert to folder name format
        folder_name = test_name.lower().replace(' ', '_')
        
        try:
            # Create test structure
            self.create_test_structure(category, folder_name)
            
            # Update tree structure
            self.test_structure[category].append(folder_name)
            self.view.populate_tree(self.test_structure)
            
            self.view.show_message("Success", f"Test '{test_name}' added successfully!")
            
        except Exception as e:
            self.view.show_message("Error", f"Failed to add test: {str(e)}", "error")

    def delete_test(self):
        """Delete selected test"""
        if self.current_selection_type != 'test':
            self.view.show_message("Warning", "Please select a test to delete", "warning")
            return
        
        category, test_name = self.current_selection
        
        # Confirm deletion
        result = self.view.show_message("Confirm", f"Delete test '{test_name}'?", "warning")
        # Note: messagebox doesn't return value in our current implementation
        # In a real implementation, you'd use askquestion
        
        # For now, just show a message
        self.view.show_message("Info", "Delete functionality would be implemented here")

    def add_section(self):
        """Add a new section to current test"""
        # Implementation for adding new data sections
        self.view.show_message("Info", "Add section functionality would be implemented here")

    # Equipment management
    def on_equipment_toggle(self, equipment_id, is_selected):
        """Handle equipment checkbox toggle"""
        # Save equipment selection state
        print(f"Equipment {equipment_id} {'selected' if is_selected else 'deselected'}")

    def refresh_equipment(self):
        """Refresh equipment list"""
        self.load_equipment_for_current_test()

    def add_equipment(self):
        """Add new equipment"""
        # Ask for equipment details
        name = self.view.ask_string("Add Equipment", "Equipment name:")
        if not name:
            return
        
        model = self.view.ask_string("Add Equipment", "Model:")
        if not model:
            return
        
        serial = self.view.ask_string("Add Equipment", "Serial number:")
        if not serial:
            return
        
        # In real implementation, this would be saved to equipment database
        self.view.show_message("Success", f"Equipment '{name}' would be added")

    # Report generation
    def generate_report(self):
        """Generate the final report"""
        if not self.model or not self.model.report_path:
            self.view.show_message("Warning", "No report loaded", "warning")
            return
        
        # Save current data first
        self.save_current()
        
        # Generate report (implementation would call model.create_report())
        try:
            self.model.create_report()
            self.view.show_message("Success", "Report generation started!")
        except Exception as e:
            self.view.show_message("Error", f"Failed to generate report: {str(e)}", "error")

    def send_report(self):
        """Send the report"""
        if not self.model or not self.model.report_path:
            self.view.show_message("Warning", "No report loaded", "warning")
            return
        
        try:
            self.model.send_report()
            self.view.show_message("Success", "Report sent successfully!")
        except Exception as e:
            self.view.show_message("Error", f"Failed to send report: {str(e)}", "error")

    # Helper methods
    def ensure_test_structure(self):
        """Ensure the test directory structure exists"""
        if not self.model.report_path:
            return
        
        # Create tests directory structure
        for category, tests in self.test_structure.items():
            if category == 'cover_page':
                continue
            
            category_path = os.path.join(self.model.tests_path, category)
            os.makedirs(category_path, exist_ok=True)
            
            for test in tests:
                self.create_test_structure(category, test)

    def create_test_structure(self, category, test_name):
        """Create the folder structure for a test"""
        if not self.model.report_path:
            return
        
        test_path = os.path.join(self.model.tests_path, category, test_name)
        
        # Create subdirectories
        subdirs = ['csv', 'images', 'latex']
        for subdir in subdirs:
            os.makedirs(os.path.join(test_path, subdir), exist_ok=True)
        
        # Create default CSV files
        csv_path = os.path.join(test_path, 'csv')
        
        # Create data.csv with headers
        import pandas as pd
        default_data = pd.DataFrame({
            'Parameter': [''],
            'Value': [''],
            'Unit': [''],
            'Notes': ['']
        })
        default_data.to_csv(os.path.join(csv_path, 'data.csv'), index=False)
        
        # Note: equipment_used is managed centrally through cover_page/equipment_used.json
        # No need to create individual equipment_used.csv files for each test
        
        # Create images.csv
        images_data = pd.DataFrame({
            'file_name': [''],
            'title': [''],
            'caption': ['']
        })
        images_data.to_csv(os.path.join(test_path, 'images', 'images.csv'), index=False)