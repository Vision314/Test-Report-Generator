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

        self.canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Bind mouse wheel events to canvas
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)  # Linux
        self.canvas.bind("<Button-5>", self._on_mousewheel)  # Linux
        
        # Make canvas focusable and bind focus events
        self.canvas.focus_set()
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())
        
        # Bind mouse wheel to the scrollable frame itself
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<Button-4>", self._on_mousewheel)
        self.scrollable_frame.bind("<Button-5>", self._on_mousewheel)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        # Windows and MacOS
        if hasattr(event, 'delta'):
            delta = event.delta
        else:
            # Linux
            if event.num == 4:
                delta = 120
            elif event.num == 5:
                delta = -120
            else:
                return
        
        self.canvas.yview_scroll(int(-1 * (delta / 120)), "units")
    
    def bind_mousewheel_to_children(self, widget):
        """Recursively bind mouse wheel events to all child widgets"""
        try:
            widget.bind("<MouseWheel>", self._on_mousewheel)
            widget.bind("<Button-4>", self._on_mousewheel)  # Linux
            widget.bind("<Button-5>", self._on_mousewheel)  # Linux
        except:
            pass  # Some widgets might not support binding
        
        for child in widget.winfo_children():
            self.bind_mousewheel_to_children(child)

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
        ttk.Button(toolbar, text="Add Table", command=self.add_section).pack(side=tk.RIGHT, padx=2)
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
        # Title frame with buttons
        title_frame = tk.Frame(parent)
        title_frame.pack(fill=tk.X, pady=(10, 2), padx=5)  # Reduced padding
        
        # Title label on the left
        title_label = tk.Label(title_frame, text=title, font=("Arial", 12, "bold"))
        title_label.pack(side=tk.LEFT)
        
        # Buttons on the right
        button_frame = tk.Frame(title_frame)
        button_frame.pack(side=tk.RIGHT)
        
        # Auto-size button (leftmost)
        autosize_button = tk.Button(
            button_frame,
            text="Auto-size",
            font=("Arial", 8),
            bg="#d4e6f1",
            relief=tk.FLAT,
            command=lambda: self.resize_sheet_to_content(section_name)
        )
        autosize_button.pack(side=tk.RIGHT, padx=(5, 5))
        
        # Add Column button
        col_button = tk.Button(
            button_frame, 
            text="+ Column", 
            font=("Arial", 8), 
            bg="#e1e1e1", 
            relief=tk.FLAT,
            command=lambda: self.add_column_to_sheet(section_name)
        )
        col_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Add Row button
        row_button = tk.Button(
            button_frame, 
            text="+ Row", 
            font=("Arial", 8), 
            bg="#e1e1e1", 
            relief=tk.FLAT,
            command=lambda: self.add_row_to_sheet(section_name)
        )
        row_button.pack(side=tk.RIGHT, padx=(5, 5))
        
        # Subtitle
        if subtitle:
            subtitle_label = tk.Label(parent, text=subtitle, font=("Arial", 9, "italic"), fg="gray")
            subtitle_label.pack(anchor="w", pady=(0, 3), padx=5)  # Reduced padding
        
        # Sheet with calculated dimensions
        sheet_width, sheet_height = self.calculate_sheet_dimensions(data)
        print(f"DEBUG: Creating sheet '{section_name}' with dimensions {sheet_width}x{sheet_height}")
        sheet = Sheet(parent, data=data, width=sheet_width, height=sheet_height)
        sheet.enable_bindings()
        
        # Configure sheet to be more compact
        try:
            sheet.hide_vertical_scrollbar()
            sheet.hide_horizontal_scrollbar()
            # Set tighter internal padding if available
            if hasattr(sheet, 'set_options'):
                sheet.set_options(show_vertical_grid=True, show_horizontal_grid=True)
        except:
            pass  # Some versions might not have these methods
        
        sheet.pack(pady=(0, 5), padx=5, anchor="w")  # Reduced padding from (0,10), padx=10
        
        # After sheet is created, recalculate with actual dimensions
        self.after(100, lambda: self.refine_sheet_dimensions(section_name))
        
        # Bind mouse wheel to sheet
        try:
            sheet.bind("<MouseWheel>", self.center_scrollable._on_mousewheel)
            sheet.bind("<Button-4>", self.center_scrollable._on_mousewheel)  # Linux
            sheet.bind("<Button-5>", self.center_scrollable._on_mousewheel)  # Linux
        except:
            pass
        
        # Store reference and bind save event
        self.current_sheets[section_name] = sheet
        
        # Bind automatic resizing events
        self.bind_sheet_resize_events(sheet, section_name)
        
        # Bind sheet edit events to refresh equipment if this is equipment_used section
        if section_name == 'equipment_used':
            sheet.bind("<<SheetModified>>", lambda e: self.on_equipment_sheet_changed())
            # Also bind common edit events
            sheet.bind("<Return>", lambda e: self.on_equipment_sheet_changed())
            sheet.bind("<Tab>", lambda e: self.on_equipment_sheet_changed())
            sheet.bind("<FocusOut>", lambda e: self.on_equipment_sheet_changed())
        
        # Bind events for automatic resizing
        self.bind_sheet_resize_events(sheet, section_name)
        
        return sheet

    def add_row_to_sheet(self, section_name):
        """Add a row to the specified sheet"""
        if section_name in self.current_sheets:
            sheet = self.current_sheets[section_name]
            # Insert a new empty row at the end
            sheet.insert_row()
            # Resize the sheet to fit new content
            self.resize_sheet_to_content(section_name)
            print(f"DEBUG: Added row to {section_name}")

    def add_column_to_sheet(self, section_name):
        """Add a column to the specified sheet"""
        if section_name in self.current_sheets:
            sheet = self.current_sheets[section_name]
            # Insert a new empty column at the end
            sheet.insert_column()
            # Resize the sheet to fit new content
            self.resize_sheet_to_content(section_name)
            print(f"DEBUG: Added column to {section_name}")

    def resize_sheet_to_content(self, section_name):
        """Resize a sheet based on its current content"""
        if section_name in self.current_sheets:
            sheet = self.current_sheets[section_name]
            
            # First, auto-size columns and rows to fit content
            try:
                # Use tksheet's built-in method to size cells to text
                sheet.set_all_cell_sizes_to_text()
                print(f"DEBUG: Auto-sized cells to text for {section_name}")
            except Exception as e:
                print(f"DEBUG: Could not auto-size cells: {e}")
            
            # Get current data from the sheet
            current_data = sheet.get_sheet_data()
            # Calculate new dimensions using actual sheet measurements
            new_width, new_height = self.calculate_sheet_dimensions_from_sheet(sheet, current_data)
            # Apply new dimensions
            sheet.config(width=new_width, height=new_height)
            print(f"DEBUG: Resized {section_name} to {new_width}x{new_height}")

    def calculate_sheet_dimensions_from_sheet(self, sheet, data):
        """Calculate sheet dimensions using actual column widths and row heights"""
        try:
            if not data:
                print("DEBUG: No data, using default size")
                return 400, 150
            
            # Handle empty or all-empty rows
            non_empty_rows = [row for row in data if row and any(str(cell).strip() for cell in row)]
            if not non_empty_rows:
                print("DEBUG: No non-empty rows, using minimal size")
                return 300, 100
            
            num_rows = len(data)
            num_cols = max(len(row) for row in data if row) if data else 1
            
            # Get actual column widths using proper tksheet methods
            total_width = 0
            try:
                # Try to get all column widths at once
                column_widths = sheet.get_column_widths()
                if column_widths and len(column_widths) >= num_cols:
                    total_width = sum(column_widths[:num_cols])
                    print(f"DEBUG: Got column widths from get_column_widths(): {column_widths[:num_cols]}")
                else:
                    # Fall back to individual column width calls
                    for col in range(num_cols):
                        try:
                            col_width = sheet.column_width(col)
                            actual_width = col_width if col_width and col_width > 0 else 120
                            total_width += actual_width
                        except:
                            total_width += 120  # Default width
                    print(f"DEBUG: Got column widths individually, total: {total_width}")
                
                # Add minimal space for row index (reduce padding)
                total_width += 40  # Reduced from 60 to 40
            except Exception as e:
                print(f"DEBUG: Error getting column widths: {e}")
                # Fallback to estimated width
                total_width = num_cols * 120 + 40
            
            # Get actual row heights using proper tksheet methods
            total_height = 0
            try:
                # Try to get all row heights at once
                row_heights = sheet.get_row_heights()
                if row_heights and len(row_heights) >= num_rows:
                    total_height = sum(row_heights[:num_rows])
                    print(f"DEBUG: Got row heights from get_row_heights(): {row_heights[:num_rows]}")
                else:
                    # Fall back to individual row height calls
                    for row in range(num_rows):
                        try:
                            r_height = sheet.row_height(row)
                            actual_height = r_height if r_height and r_height > 0 else 20
                            total_height += actual_height
                        except:
                            total_height += 20  # Default height
                    print(f"DEBUG: Got row heights individually, total: {total_height}")
                
                # Add header height and padding
                try:
                    header_height = sheet.default_header_height if hasattr(sheet, 'default_header_height') else 25
                    total_height += header_height
                except:
                    total_height += 25
                
                # Add minimal padding for borders (reduce padding)
                total_height += 15  # Reduced from 30 to 15
            except Exception as e:
                print(f"DEBUG: Error getting row heights: {e}")
                # Fallback to estimated height
                total_height = (num_rows * 20) + 25 + 15
            
            # Apply reasonable limits with tighter bounds to prevent scrollbars
            sheet_width = max(min(total_width, 1400), 150)  # Reduced min from 200 to 150
            sheet_height = max(min(total_height, 500), 50)   # Reduced min from 70 to 50
            
            print(f"DEBUG: Calculated from sheet: {sheet_width}x{sheet_height} (cols: {num_cols}, rows: {num_rows})")
            return sheet_width, sheet_height
            
        except Exception as e:
            print(f"DEBUG: Error calculating from sheet, using fallback: {e}")
            return self.calculate_sheet_dimensions(data)

    def calculate_sheet_dimensions(self, data):
        """Calculate appropriate sheet dimensions based on data"""
        print(f"DEBUG: Calculating dimensions for data: {data}")
        
        if not data:
            print("DEBUG: No data, using default size")
            return 400, 150
        
        # Handle case where data is empty list or list of empty lists
        non_empty_rows = [row for row in data if row and any(str(cell).strip() for cell in row)]
        if not non_empty_rows:
            print("DEBUG: Empty rows, using minimal size")
            return 300, 100
        
        # Find the maximum number of columns across all rows
        num_rows = len(data)
        num_cols = max(len(row) for row in data if row) if data else 1
        
        print(f"DEBUG: Found {num_rows} rows, {num_cols} columns")
        
        # Calculate width based on columns (more generous sizing)
        col_width = 120  # Increased from 80 to make columns wider
        calculated_width = num_cols * col_width + 40  # Reduced padding from 80 to 40
        sheet_width = max(min(calculated_width, 1400), 150)  # Tighter bounds
        
        # Calculate height based on rows (more compact sizing)
        row_height = 20  # Reduced from 25 to make rows shorter
        header_height = 30  # Header row height
        calculated_height = (num_rows * row_height) + header_height + 5  # Reduced padding from 10 to 5
        sheet_height = max(min(calculated_height, 500), 50)  # Tighter bounds
        
        print(f"DEBUG: Calculated dimensions: {sheet_width}x{sheet_height}")
        return sheet_width, sheet_height

    def bind_sheet_resize_events(self, sheet, section_name):
        """Bind events to automatically resize sheet when content changes"""
        # Bind to various sheet modification events
        try:
            # These events should trigger when the sheet structure changes
            sheet.bind("<<SheetModified>>", lambda e: self.on_sheet_modified(section_name))
            sheet.bind("<KeyPress-Delete>", lambda e: self.after(50, lambda: self.resize_sheet_to_content(section_name)))
            sheet.bind("<Control-x>", lambda e: self.after(50, lambda: self.resize_sheet_to_content(section_name)))
            sheet.bind("<Control-v>", lambda e: self.after(50, lambda: self.resize_sheet_to_content(section_name)))
            
            # Bind to column/row resize events (if available)
            sheet.bind("<ButtonRelease-1>", lambda e: self.after(100, lambda: self.on_potential_resize(section_name, e)))
            
        except Exception as e:
            print(f"DEBUG: Could not bind resize events: {e}")

    def on_potential_resize(self, section_name, event):
        """Handle potential column/row resize operations"""
        # Check if the user may have resized columns or rows
        # This is called after mouse release, so we check if dimensions changed
        try:
            if section_name in self.current_sheets:
                sheet = self.current_sheets[section_name]
                # Get current data and recalculate
                current_data = sheet.get_sheet_data()
                if current_data:
                    new_width, new_height = self.calculate_sheet_dimensions_from_sheet(sheet, current_data)
                    current_width = sheet.winfo_width()
                    current_height = sheet.winfo_height()
                    
                    # Only resize if dimensions changed significantly (more than 10 pixels)
                    if abs(new_width - current_width) > 10 or abs(new_height - current_height) > 10:
                        sheet.config(width=new_width, height=new_height)
                        print(f"DEBUG: Adjusted {section_name} after potential resize: {new_width}x{new_height}")
        except Exception as e:
            print(f"DEBUG: Error in potential resize handler: {e}")

    def on_sheet_modified(self, section_name):
        """Handle sheet modification events"""
        # Delay resize slightly to allow the modification to complete
        self.after(50, lambda: self.resize_sheet_to_content(section_name))

    def refine_sheet_dimensions(self, section_name):
        """Refine sheet dimensions after initial creation using actual measurements"""
        if section_name in self.current_sheets:
            sheet = self.current_sheets[section_name]
            
            # Auto-size columns and rows to fit content first
            try:
                sheet.set_all_cell_sizes_to_text()
                print(f"DEBUG: Auto-sized cells to text for {section_name}")
            except Exception as e:
                print(f"DEBUG: Could not auto-size cells during refinement: {e}")
            
            current_data = sheet.get_sheet_data()
            # Use the more accurate calculation method
            new_width, new_height = self.calculate_sheet_dimensions_from_sheet(sheet, current_data)
            sheet.config(width=new_width, height=new_height)
            print(f"DEBUG: Refined {section_name} dimensions to {new_width}x{new_height}")

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
        
        # Bind mouse wheel events to all new child widgets
        self.center_scrollable.bind_mousewheel_to_children(self.center_scrollable.scrollable_frame)

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
        if not data:
            # Show message when no data files found
            message_label = tk.Label(
                self.center_scrollable.scrollable_frame,
                text="No data files found for this test",
                font=("Arial", 14),
                fg="gray"
            )
            message_label.pack(pady=50)
            return
        
        # Load each table file as a separate section
        for section_name, section_data in data.items():
            # Create a readable title from filename
            title = section_name.replace('_', ' ').title()
            subtitle = f"Data from {section_name}.csv"
            
            # Create sheet section
            sheet = self.create_sheet_section(
                self.center_scrollable.scrollable_frame,
                title,
                subtitle,
                section_data,
                section_name
            )
            
            self.current_sheets[section_name] = sheet

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