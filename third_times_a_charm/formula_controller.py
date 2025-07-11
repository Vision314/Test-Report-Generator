# ╭──────────────────────────────────────────────────────────────────────────╮
# │                    Engineering Test Report Generator                     │
# │                 Controller Component (MVC) + FORMULA EDITOR             │
# │                         WITH CSV FORMULA SUPPORT                        │
# ╰──────────────────────────────────────────────────────────────────────────╯

import os
import json
import re
from tkinter import messagebox

class FormulaController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Set MVC references
        self.view.set_controller(self)
        self.view.set_model(model)
        
        # Current state
        self.current_category = None
        self.current_test = None
        self.current_section_id = None
        
        self.initialize_view()

    def initialize_view(self):
        """Initialize view with default state"""
        self.view.show_no_report_message()
        self.view.update_title()

    def run(self):
        """Start the application"""
        self.view.mainloop()

    # FILE OPERATIONS
    def new_report(self):
        """Create new report"""
        directory = self.view.ask_directory("Select Directory for New Report")
        if not directory:
            return
        
        report_name = self.view.ask_string("New Report", "Enter report name:")
        if not report_name:
            return
        
        report_path = os.path.join(directory, report_name)
        
        try:
            # Create directory structure
            os.makedirs(report_path, exist_ok=True)
            os.makedirs(os.path.join(report_path, 'tests'), exist_ok=True)
            os.makedirs(os.path.join(report_path, 'cover_page'), exist_ok=True)
            os.makedirs(os.path.join(report_path, 'report'), exist_ok=True)
            
            # Initialize model with new path
            self.model.report_path = report_path
            self.model._initialize_paths()
            self.model.initialize_default_cover_page()
            
            # Update view
            self.view.update_title(report_name)
            self.update_tree()
            self.load_cover_page()
            
        except Exception as e:
            self.view.show_message("Error", f"Failed to create report: {e}", "error")

    def open_report(self):
        """Open existing report"""
        directory = self.view.ask_directory("Select Report Directory")
        if not directory or not os.path.exists(directory):
            return
        
        try:
            # Initialize model with existing path
            self.model.report_path = directory
            self.model._initialize_paths()
            self.model._load_existing_data()
            
            # Update view
            report_name = os.path.basename(directory)
            self.view.update_title(report_name)
            self.update_tree()
            self.load_cover_page()
            
        except Exception as e:
            self.view.show_message("Error", f"Failed to open report: {e}", "error")

    def save_current(self, show_message=True):
        """Save current section data"""
        if not self.model.report_path:
            return
        
        try:
            # Save all current sheet data
            for section_name, sheet in self.view.current_sheets.items():
                data = sheet.get_sheet_data()
                
                if self.current_section_id and self.current_section_id.startswith('cover_'):
                    # Save cover page section
                    cover_section = self.current_section_id.replace('cover_', '')
                    self.model.save_cover_page_section(cover_section, data)
                elif self.current_category and self.current_test:
                    # Save test data section
                    self.model.save_test_data(self.current_category, self.current_test, section_name, data)
            
            if show_message:
                self.view.show_message("Save", "Data saved successfully!", "info")
                
        except Exception as e:
            self.view.show_message("Error", f"Failed to save data: {e}", "error")

    # TREE OPERATIONS
    def update_tree(self):
        """Update file tree display"""
        tree_data = {"cover_page": []}
        
        if self.model.tests_path and os.path.exists(self.model.tests_path):
            for category in os.listdir(self.model.tests_path):
                category_path = os.path.join(self.model.tests_path, category)
                if os.path.isdir(category_path) and category != 'test_selections.json':
                    tests = [test for test in os.listdir(category_path) 
                            if os.path.isdir(os.path.join(category_path, test))]
                    tree_data[category] = tests
        
        self.view.populate_tree(tree_data)

    def on_tree_selection(self, selection):
        """Handle tree selection"""
        if not selection:
            return
        
        # Save current data before switching
        self.save_current(show_message=False)
        
        item = selection[0]
        tags = self.view.tree.item(item, "tags")
        
        if not tags:
            return
        
        if tags[0] == "cover_page":
            self.load_cover_page()
        elif len(tags) == 1:
            # Category selected
            self.load_category_overview(tags[0])
        elif len(tags) == 2:
            # Test selected
            self.load_test_data(tags[0], tags[1])

    def on_tree_click(self, item):
        """Handle tree click events"""
        pass

    # CONTENT LOADING
    def load_cover_page(self):
        """Load cover page sections"""
        self.current_section_id = "cover_page"
        self.current_category = None
        self.current_test = None
        
        sections = {}
        for section_name in ['product_information', 'general_specifications', 'testing_and_review', 'equipment_used']:
            data = self.model.get_cover_page_section(section_name)
            sections[section_name] = data
            
            # Load formulas for this section
            self.model.load_formulas(f"cover_{section_name}")
        
        self.view.load_cover_page_sections(sections)
        self.load_equipment_list()

    def load_category_overview(self, category):
        """Load category overview"""
        self.view.clear_center_content()
        # Could show category summary here

    def load_test_data(self, category, test_name):
        """Load test data sections"""
        self.current_category = category
        self.current_test = test_name
        self.current_section_id = f"{category}_{test_name}"
        
        test_data = self.model.get_test_data(category, test_name)
        
        if not test_data:
            # Create default table if none exists
            default_data = [["Column 1", "Column 2", "Column 3"], ["", "", ""]]
            test_data = {"table1": default_data}
        
        self.view.clear_center_content()
        
        for section_name, data in test_data.items():
            title = section_name.replace('_', ' ').title()
            self.view.create_sheet_section(self.view.center_scrollable.scrollable_frame,
                                         title, f"Test: {test_name}", data, section_name)
            
            # Load and highlight formulas
            section_id = f"{category}_{test_name}_{section_name}"
            formula_cells = self.get_formula_cells(section_id)
            self.view.highlight_formula_cells(section_name, formula_cells)

    def load_equipment_list(self):
        """Load equipment list for current context"""
        equipment_data = self.model.get_cover_page_section('equipment_used')
        if equipment_data and len(equipment_data) > 1:
            # Skip header row
            self.view.load_equipment_list(equipment_data[1:])
        else:
            self.view.load_equipment_list([])

    # FORMULA EDITOR METHODS
    def set_cell_content(self, section_id, row, col, content):
        """Set cell content and handle formulas"""
        if isinstance(content, str) and content.startswith("="):
            # It's a formula
            self.model.set_formula(section_id, row, col, content)
            
            # Evaluate and set result
            result = self.evaluate_formula(section_id, row, col, content)
            
            # Find the sheet and update display
            sheet = self.get_sheet_for_section(section_id)
            if sheet:
                sheet.set_cell_data(row, col, str(result), redraw=True)
                sheet.highlight_cells(row, col, bg="#dae7f5")
                
            # Recalculate dependent cells
            self.recalculate_dependencies(section_id, row, col)
            
        else:
            # Regular value
            self.model.remove_formula(section_id, row, col)
            
            sheet = self.get_sheet_for_section(section_id)
            if sheet:
                sheet.set_cell_data(row, col, content)
                sheet.dehighlight_cells(row, col)
                
            # Recalculate dependent cells
            self.recalculate_dependencies(section_id, row, col)

    def get_formula(self, section_id, row, col):
        """Get formula for cell"""
        return self.model.get_formula(section_id, row, col)

    def clear_cell(self, section_id, row, col):
        """Clear cell content and formula"""
        self.model.remove_formula(section_id, row, col)
        
        sheet = self.get_sheet_for_section(section_id)
        if sheet:
            sheet.set_cell_data(row, col, "")
            sheet.dehighlight_cells(row, col)
            
        self.recalculate_dependencies(section_id, row, col)

    def evaluate_formula(self, section_id, row, col, formula):
        """Evaluate formula and return result"""
        if not formula.startswith("="):
            return formula
        
        expr = formula[1:]  # Remove '='
        refs = re.findall(r"[A-Z]+\d+", expr.upper())
        
        sheet = self.get_sheet_for_section(section_id)
        if not sheet:
            return "ERR"
        
        for ref in refs:
            r, c = self.model.cell_name_to_index(ref)
            val = sheet.get_cell_data(r, c)
            try:
                val = float(val) if val else 0
            except:
                val = 0
            expr = re.sub(ref, str(val), expr, flags=re.IGNORECASE)
        
        try:
            result = eval(expr)
            return result
        except:
            return "ERR"

    def recalculate_dependencies(self, section_id, row, col):
        """Recalculate cells that depend on this cell"""
        dep_key = (section_id, row, col)
        if dep_key in self.model.dependencies:
            for dep_cell in self.model.dependencies[dep_key]:
                dep_section, dep_row, dep_col = dep_cell
                formula = self.model.get_formula(dep_section, dep_row, dep_col)
                if formula:
                    result = self.evaluate_formula(dep_section, dep_row, dep_col, formula)
                    sheet = self.get_sheet_for_section(dep_section)
                    if sheet:
                        sheet.set_cell_data(dep_row, dep_col, str(result), redraw=True)

    def get_formula_cells(self, section_id):
        """Get list of cells with formulas for a section"""
        formula_cells = []
        for (sec_id, row, col), formula in self.model.formulas.items():
            if sec_id == section_id:
                formula_cells.append((row, col))
        return formula_cells

    def get_sheet_for_section(self, section_id):
        """Get sheet widget for section"""
        if section_id.startswith('cover_'):
            section_name = section_id.replace('cover_', '')
            return self.view.current_sheets.get(section_name)
        else:
            # Test data sheet
            parts = section_id.split('_')
            if len(parts) >= 3:
                table_name = '_'.join(parts[2:])
                return self.view.current_sheets.get(table_name)
        return None

    # TEST MANAGEMENT
    def add_test(self):
        """Add new test"""
        if not self.model.report_path:
            self.view.show_message("Error", "No report loaded", "error")
            return
        
        category = self.view.ask_string("Add Test", "Enter category name:")
        if not category:
            return
        
        test_name = self.view.ask_string("Add Test", "Enter test name:")
        if not test_name:
            return
        
        try:
            # Create test directory structure
            test_path = os.path.join(self.model.tests_path, category, test_name)
            os.makedirs(os.path.join(test_path, 'csv'), exist_ok=True)
            os.makedirs(os.path.join(test_path, 'images'), exist_ok=True)
            os.makedirs(os.path.join(test_path, 'latex'), exist_ok=True)
            
            # Create default table
            default_data = [["Column 1", "Column 2", "Column 3"], ["", "", ""]]
            self.model.save_test_data(category, test_name, "table1", default_data)
            
            self.update_tree()
            self.view.show_message("Success", f"Test '{test_name}' added to '{category}'", "info")
            
        except Exception as e:
            self.view.show_message("Error", f"Failed to add test: {e}", "error")

    def delete_test(self):
        """Delete selected test"""
        selection = self.view.tree.selection()
        if not selection:
            return
        
        item = selection[0]
        tags = self.view.tree.item(item, "tags")
        
        if len(tags) != 2:
            self.view.show_message("Error", "Please select a test to delete", "error")
            return
        
        category, test_name = tags
        
        result = messagebox.askyesno("Delete Test", 
                                   f"Are you sure you want to delete test '{test_name}' from category '{category}'?")
        if not result:
            return
        
        try:
            import shutil
            test_path = os.path.join(self.model.tests_path, category, test_name)
            if os.path.exists(test_path):
                shutil.rmtree(test_path)
            
            self.update_tree()
            self.view.show_no_report_message()
            self.view.show_message("Success", f"Test '{test_name}' deleted", "info")
            
        except Exception as e:
            self.view.show_message("Error", f"Failed to delete test: {e}", "error")

    # REPORT GENERATION
    def generate_report(self):
        """Generate report"""
        if not self.model.report_path:
            self.view.show_message("Error", "No report loaded", "error")
            return
        
        self.view.show_message("Info", "Report generation not yet implemented", "info")

    def send_report(self):
        """Send report"""
        if not self.model.report_path:
            self.view.show_message("Error", "No report loaded", "error")
            return
        
        self.view.show_message("Info", "Report sending not yet implemented", "info")

    def adjust_formula_references(self, formula, source_row, source_col, target_row, target_col):
        """Adjust formula references when copying (delegate to model)"""
        return self.model.adjust_formula_references(formula, source_row, source_col, target_row, target_col)
