# ╭──────────────────────────────────────────────────────────────────────────╮
# │                    Engineering Test Re# │   ask_string(title: str, prompt: str) -> str                             │
# │     Purpose: Show string input dialog                                    │
# │     Inputs:  title - Dialog title, prompt - Input prompt                 │
# │     Outputs: User input string or None                                   │
# │                                                                          │
# │   update_title(report_name: str = None) -> None                          │
# │     Purpose: Update application title with report name                   │
# │     Inputs:  report_name - Name of current report (optional)             │
# │     Outputs: None (updates window title)                                 │
# │                                                                          │Generator                     │
# │                             View Component (MVC)                         │
# ├──────────────────────────────────────────────────────────────────────────┤
# │ CLASSES:                                                                 │
# │                                                                          │
# │ ScrollableFrame(tk.Frame)                                                │
# │   Purpose: Scrollable frame widget for center pane content               │
# │   Inputs:  container - Parent widget                                     │
# │   Outputs: Scrollable frame with canvas and scrollbar                    │
# │   Attributes: scrollable_frame - Inner frame for content                 │
# │                                                                          │
# │ View(tk.Tk)                                                              │
# │   Purpose: Main GUI interface with VS Code-like three-pane layout        │
# │                                                                          │
# │ INITIALIZATION METHODS:                                                  │
# │   __init__(model_class=None) -> None                                     │
# │     Purpose: Initialize main window and create GUI components            │
# │     Inputs:  model_class - Optional model class reference                │
# │     Outputs: None                                                        │
# │                                                                          │
# │   create_menu() -> None                                                  │
# │     Purpose: Create the main menu bar with File, Edit, Report menus      │
# │     Inputs:  None                                                        │
# │     Outputs: None                                                        │
# │                                                                          │
# │   create_panes() -> None                                                 │
# │     Purpose: Create the three-pane VS Code-like layout                   │
# │     Inputs:  None                                                        │
# │     Outputs: None                                                        │
# │                                                                          │
# │   create_file_manager_pane(parent) -> None                               │
# │     Purpose: Create left file manager pane with tree view                │
# │     Inputs:  parent - Parent widget                                      │
# │     Outputs: None                                                        │
# │                                                                          │
# │   create_center_editor_pane(parent) -> None                              │
# │     Purpose: Create center scrollable editor pane                        │
# │     Inputs:  parent - Parent widget                                      │
# │     Outputs: None                                                        │
# │                                                                          │
# │   create_equipment_manager_pane(parent) -> None                          │
# │     Purpose: Create bottom equipment manager pane                        │
# │     Inputs:  parent - Parent widget                                      │
# │     Outputs: None                                                        │
# │                                                                          │
# │ CONTENT MANAGEMENT METHODS:                                              │
# │   create_sheet_section(parent, title, subtitle, data, section_name) -> Sheet│
# │     Purpose: Create a titled sheet section in scrollable area            │
# │     Inputs:  parent - Parent widget, title - Section title               │
# │              subtitle - Section subtitle, data - Sheet data              │
# │              section_name - Unique section identifier                    │
# │     Outputs: Sheet widget reference                                      │
# │                                                                          │
# │   populate_tree(tree_data: dict) -> None                                 │
# │     Purpose: Populate file tree with category and test data              │
# │     Inputs:  tree_data - Dict of categories and their tests              │
# │     Outputs: None                                                        │
# │                                                                          │
# │   load_center_content(content_type: str, data: dict) -> None             │
# │     Purpose: Load content in center pane (cover_page or test_data)       │
# │     Inputs:  content_type - Type of content to load                      │
# │              data - Content data                                         │
# │     Outputs: None                                                        │
# │                                                                          │
# │   load_cover_page_sections(sections: dict) -> None                       │
# │     Purpose: Load cover page sections into scrollable sheets             │
# │     Inputs:  sections - Dict of section names and data                   │
# │     Outputs: None                                                        │
# │                                                                          │
# │   load_equipment_list(equipment_data: list) -> None                      │
# │     Purpose: Load equipment checkboxes in bottom pane                    │
# │     Inputs:  equipment_data - List of equipment dicts                    │
# │     Outputs: None                                                        │
# │                                                                          │
# │ EVENT HANDLER METHODS:                                                   │
# │   on_tree_select(event) -> None                                          │
# │     Purpose: Handle tree selection events                                │
# │     Inputs:  event - Tkinter event object                                │
# │     Outputs: None (delegates to controller)                              │
# │                                                                          │
# │   on_tree_click(event) -> None                                           │
# │     Purpose: Handle tree click events for checkbox functionality         │
# │     Inputs:  event - Tkinter event object                                │
# │     Outputs: None (delegates to controller)                              │
# │                                                                          │
# │   on_equipment_toggle(equipment_id: str) -> None                         │
# │     Purpose: Handle equipment checkbox toggle events                     │
# │     Inputs:  equipment_id - Unique equipment identifier                  │
# │     Outputs: None (delegates to controller)                              │
# │                                                                          │
# │ MENU COMMAND METHODS:                                                    │
# │   new_report(), open_report(), save_current() -> None                    │
# │   add_test(), delete_test(), add_section() -> None                       │
# │   generate_report(), send_report() -> None                               │
# │   refresh_equipment(), add_equipment() -> None                           │
# │     Purpose: Menu command handlers (all delegate to controller)          │
# │     Inputs:  None                                                        │
# │     Outputs: None                                                        │
# │                                                                          │
# │ UTILITY METHODS:                                                         │
# │   set_controller(controller), set_model(model) -> None                   │
# │     Purpose: Set MVC component references                                │
# │     Inputs:  controller/model - Component instances                      │
# │     Outputs: None                                                        │
# │                                                                          │
# │   get_sheet_data(section_name: str) -> list                              │
# │     Purpose: Get data from specific sheet                                │
# │     Inputs:  section_name - Section identifier                           │
# │     Outputs: List of lists (sheet data)                                  │
# │                                                                          │
# │   show_message(title: str, message: str, msg_type: str) -> None          │
# │     Purpose: Show message dialog                                         │
# │     Inputs:  title - Dialog title, message - Message text                │
# │              msg_type - "info", "warning", or "error"                    │
# │     Outputs: None                                                        │
# │                                                                          │
# │   ask_directory(title: str) -> str                                       │
# │     Purpose: Ask user to select directory                                │
# │     Inputs:  title - Dialog title                                        │
# │     Outputs: Selected directory path or empty string                     │
# │                                                                          │
# │   ask_string(title: str, prompt: str) -> str                             │
# │     Purpose: Ask user for string input                                   │
# │     Inputs:  title - Dialog title, prompt - Input prompt                 │
# │     Outputs: User input string or None                                   │
# │                                                                          │
# │ ATTRIBUTES:                                                              │
# │   model, controller: MVC component references                            │
# │   report_path, current_test, current_section: Application state          │
# │   tree: File manager tree widget                                         │
# │   center_scrollable: Scrollable frame for center content                 │
# │   current_sheets: Dict of active tksheet widgets                         │
# │   equipment_frame: Frame containing equipment checkboxes                 │
# │   equipment_vars: Dict of equipment checkbox variables                   │
# │                                                                          │
# │ GUI LAYOUT:                                                              │
# │   ├── File Manager (Left)   │ Center Editor (Top Right)     │            │
# │   │  - Tree view            │  - Scrollable tksheets        │            │
# │   │  - Add/Delete buttons   │  - Section titles/subtitles   │            │
# │   │                         ├────────────────────────────────│           │
# │   │                         │ Equipment Manager (Bottom)    │            │
# │   │                         │  - Scrollable checkboxes      │            │
# ╰──────────────────────────────────────────────────────────────────────────╯

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tksheet import Sheet
import os

class ScrollableFrame(tk.Frame):
    """Scrollable frame for the center pane"""
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

class View(tk.Tk):
    def __init__(self, model_class=None):
        super().__init__()
        self.title("Engineering Test Report Generator")
        self.geometry("1400x900")
        
        # References to be set by controller
        self.model = None
        self.controller = None
        
        # Current state
        self.report_path = None
        self.current_test = None
        self.current_section = None
        
        # GUI Components
        self.tree = None
        self.center_scrollable = None
        self.current_sheets = {}  # Track active tksheets
        self.equipment_frame = None
        self.equipment_vars = {}  # Checkbox variables for equipment
        
        self.create_menu()
        self.create_panes()

    def create_menu(self):
        """Create the main menu bar"""
        menubar = tk.Menu(self)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Report", command=self.new_report)
        file_menu.add_command(label="Open Report", command=self.open_report)
        file_menu.add_command(label="Save", command=self.save_current)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Add Test", command=self.add_test)
        edit_menu.add_command(label="Delete Test", command=self.delete_test)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # Report menu
        report_menu = tk.Menu(menubar, tearoff=0)
        report_menu.add_command(label="Generate Report", command=self.generate_report)
        report_menu.add_command(label="Send Report", command=self.send_report)
        menubar.add_cascade(label="Report", menu=report_menu)
        
        self.config(menu=menubar)

    def create_panes(self):
        """Create the three-pane VS Code-like layout"""
        # Main horizontal pane: [File Manager] | [Center + Equipment]
        main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)
        
        # Left Pane: File Manager (like VS Code Explorer)
        self.create_file_manager_pane(main_pane)
        
        # Right side: Vertical split [Center Editor] above [Equipment Manager]  
        right_pane = tk.PanedWindow(main_pane, orient=tk.VERTICAL)
        main_pane.add(right_pane)
        
        # Center Pane: Scrollable sheets editor
        self.create_center_editor_pane(right_pane)
        
        # Bottom Pane: Equipment manager
        self.create_equipment_manager_pane(right_pane)

    def create_file_manager_pane(self, parent):
        """Create the left file manager pane"""
        file_frame = ttk.Frame(parent, width=300)
        
        # Toolbar
        toolbar = ttk.Frame(file_frame)
        ttk.Label(toolbar, text="File Manager", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="+ Test", command=self.add_test, width=8).pack(side=tk.RIGHT, padx=2)
        ttk.Button(toolbar, text="- Del", command=self.delete_test, width=8).pack(side=tk.RIGHT, padx=2)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        # Treeview for file structure
        self.tree = ttk.Treeview(file_frame, show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Button-1>", self.on_tree_click)
        
        parent.add(file_frame)

    def create_center_editor_pane(self, parent):
        """Create the center scrollable editor pane"""
        center_frame = ttk.Frame(parent)
        
        # Toolbar
        toolbar = ttk.Frame(center_frame)
        ttk.Label(toolbar, text="Test Data Editor", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Save", command=self.save_current).pack(side=tk.RIGHT, padx=2)
        ttk.Button(toolbar, text="Add Section", command=self.add_section).pack(side=tk.RIGHT, padx=2)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        # Scrollable frame for multiple sheets
        self.center_scrollable = ScrollableFrame(center_frame)
        self.center_scrollable.pack(fill=tk.BOTH, expand=True)
        
        parent.add(center_frame, stretch="always")

    def create_equipment_manager_pane(self, parent):
        """Create the bottom equipment manager pane"""
        equip_frame = ttk.Frame(parent, height=200)
        
        # Toolbar
        toolbar = ttk.Frame(equip_frame)
        ttk.Label(toolbar, text="Equipment Used", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Refresh", command=self.refresh_equipment).pack(side=tk.RIGHT, padx=2)
        ttk.Button(toolbar, text="Add Equipment", command=self.add_equipment).pack(side=tk.RIGHT, padx=2)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        # Scrollable frame for equipment checkboxes
        equipment_scroll = tk.Frame(equip_frame)
        canvas = tk.Canvas(equipment_scroll)
        scrollbar = tk.Scrollbar(equipment_scroll, orient="vertical", command=canvas.yview)
        self.equipment_frame = tk.Frame(canvas)
        
        self.equipment_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.equipment_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        equipment_scroll.pack(fill=tk.BOTH, expand=True)
        
        parent.add(equip_frame)

    def create_sheet_section(self, parent, title, subtitle, data, section_name):
        """Create a titled sheet section in the scrollable area"""
        # Title
        title_label = tk.Label(parent, text=title, font=("Arial", 12, "bold"))
        title_label.pack(anchor="w", pady=(15, 2), padx=10)
        
        # Subtitle
        if subtitle:
            subtitle_label = tk.Label(parent, text=subtitle, font=("Arial", 9, "italic"), fg="gray")
            subtitle_label.pack(anchor="w", pady=(0, 5), padx=10)
        
        # Sheet
        sheet = Sheet(parent, data=data, width=800, height=200)
        sheet.enable_bindings()
        sheet.pack(pady=(0, 10), padx=10, fill=tk.X)
        
        # Store reference and bind save event
        self.current_sheets[section_name] = sheet
        
        # Bind sheet edit events to refresh equipment if this is equipment_used section
        if section_name == 'equipment_used':
            sheet.bind("<<SheetModified>>", lambda e: self.on_equipment_sheet_changed())
            # Also bind common edit events
            sheet.bind("<Return>", lambda e: self.on_equipment_sheet_changed())
            sheet.bind("<Tab>", lambda e: self.on_equipment_sheet_changed())
            sheet.bind("<FocusOut>", lambda e: self.on_equipment_sheet_changed())
        
        return sheet

    # Event handlers
    def on_tree_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection and self.controller:
            item = selection[0]
            self.controller.on_tree_selection(item)

    def on_tree_click(self, event):
        """Handle tree clicks for checkbox functionality"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "tree" and self.controller:
            item = self.tree.identify_row(event.y)
            if item:
                self.controller.on_tree_click(item)

    def on_equipment_sheet_changed(self):
        """Handle equipment sheet changes and refresh equipment list"""
        if self.controller:
            # Delay the refresh slightly to allow the edit to complete
            self.after(100, self.controller.refresh_equipment)

    # Menu command handlers
    def new_report(self):
        """Create new report"""
        if self.controller:
            self.controller.new_report()

    def open_report(self):
        """Open existing report"""
        if self.controller:
            self.controller.open_report()

    def save_current(self):
        """Save current data"""
        if self.controller:
            self.controller.save_current()

    def add_test(self):
        """Add new test"""
        if self.controller:
            self.controller.add_test()

    def delete_test(self):
        """Delete selected test"""
        if self.controller:
            self.controller.delete_test()

    def add_section(self):
        """Add new section to current test"""
        if self.controller:
            self.controller.add_section()

    def generate_report(self):
        """Generate the final report"""
        if self.controller:
            self.controller.generate_report()

    def send_report(self):
        """Send the report"""
        if self.controller:
            self.controller.send_report()

    def refresh_equipment(self):
        """Refresh equipment list"""
        if self.controller:
            self.controller.refresh_equipment()

    def add_equipment(self):
        """Add new equipment"""
        if self.controller:
            self.controller.add_equipment()

    # Public interface methods for controller
    def set_controller(self, controller):
        """Set the controller reference"""
        self.controller = controller

    def set_model(self, model):
        """Set the model reference"""
        self.model = model

    def populate_tree(self, tree_data):
        """Populate the file tree with data"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add new items
        for category, tests in tree_data.items():
            cat_id = self.tree.insert('', 'end', text=f"📁 {category.replace('_', ' ').title()}", 
                                    values=(category,), tags=('category',))
            
            for test in tests:
                test_id = self.tree.insert(cat_id, 'end', text=f"📄 {test.replace('_', ' ').title()}", 
                                         values=(test,), tags=('test',))

    def load_center_content(self, content_type, data):
        """Load content in the center pane"""
        # Clear existing content
        for widget in self.center_scrollable.scrollable_frame.winfo_children():
            widget.destroy()
        self.current_sheets.clear()
        
        if content_type == "cover_page":
            self.load_cover_page_sections(data)
        elif content_type == "test_data":
            self.load_test_data_sections(data)
        elif content_type == "no_report":
            self.show_no_report_message()

    def show_no_report_message(self):
        """Show message when no report is loaded"""
        # Create centered message
        message_frame = tk.Frame(self.center_scrollable.scrollable_frame)
        message_frame.pack(expand=True, fill=tk.BOTH)
        
        # Center the message
        center_frame = tk.Frame(message_frame)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Main message
        message_label = tk.Label(
            center_frame, 
            text="Open/Create a Report", 
            font=("Arial", 18, "bold"), 
            fg="gray"
        )
        message_label.pack(pady=20)
        
        # Instructions
        instruction_label = tk.Label(
            center_frame,
            text="Use File menu to create a new report or open an existing one",
            font=("Arial", 12),
            fg="gray"
        )
        instruction_label.pack(pady=10)

    def load_cover_page_sections(self, sections):
        """Load cover page sections"""
        section_titles = {
            'product_information': ('Product Information', 'Basic product details and specifications'),
            'general_specifications': ('General Specifications', 'Technical specifications and parameters'),
            'testing_and_review': ('Testing and Review', 'Testing personnel and dates'),
            'equipment_used': ('Equipment Used', 'Test equipment and calibration information')
        }
        
        for section_name, section_data in sections.items():
            title, subtitle = section_titles.get(section_name, (section_name.title(), ''))
            self.create_sheet_section(
                self.center_scrollable.scrollable_frame,
                title, subtitle, section_data, section_name
            )

    def load_test_data_sections(self, data):
        """Load test data sections"""
        # Implementation for test data display
        pass

    def load_equipment_list(self, equipment_data):
        """Load equipment checkboxes"""
        print(f"DEBUG: Loading equipment list with {len(equipment_data)} items")
        print(f"DEBUG: Equipment data: {equipment_data}")
        
        # Clear existing equipment
        for widget in self.equipment_frame.winfo_children():
            widget.destroy()
        self.equipment_vars.clear()
        
        # Add equipment checkboxes
        for idx, equipment in enumerate(equipment_data):
            var = tk.BooleanVar()
            self.equipment_vars[equipment['id']] = var
            
            # Create checkbox with equipment info using new structure
            equipment_type = equipment.get('equipment_type', '')
            manufacturer = equipment.get('manufacturer', '')
            model = equipment.get('model', '')
            description = equipment.get('description', '')
            serial = equipment.get('serial', '')
            
            # Format: Equipment Type - manufacturer - model - description - s/n
            # Only include non-empty fields to avoid extra dashes
            parts = []
            if equipment_type: parts.append(equipment_type)
            if manufacturer: parts.append(manufacturer)
            if model: parts.append(model)
            if description: parts.append(description)
            if serial: parts.append(serial)
            
            text = ' - '.join(parts) if parts else 'Empty Equipment Entry'
            print(f"DEBUG: Creating checkbox with text: '{text}'")
            
            checkbox = tk.Checkbutton(
                self.equipment_frame, 
                text=text, 
                variable=var,
                command=lambda eq_id=equipment['id']: self.on_equipment_toggle(eq_id)
            )
            checkbox.pack(anchor='w', padx=5, pady=2)

    def on_equipment_toggle(self, equipment_id):
        """Handle equipment checkbox toggle"""
        if self.controller:
            self.controller.on_equipment_toggle(equipment_id, self.equipment_vars[equipment_id].get())

    def get_sheet_data(self, section_name):
        """Get data from a specific sheet"""
        if section_name in self.current_sheets:
            return self.current_sheets[section_name].get_sheet_data()
        return []

    def show_message(self, title, message, msg_type="info"):
        """Show message dialog"""
        if msg_type == "info":
            messagebox.showinfo(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        elif msg_type == "error":
            messagebox.showerror(title, message)

    def ask_directory(self, title="Select Directory"):
        """Ask for directory selection"""
        return filedialog.askdirectory(title=title)

    def ask_string(self, title, prompt):
        """Ask for string input"""
        return simpledialog.askstring(title, prompt)

    def update_title(self, report_name=None):
        """Update the application title with report name"""
        base_title = "Engineering Test Report Generator"
        if report_name:
            self.title(f"{base_title} - [{report_name}]")
        else:
            self.title(base_title)