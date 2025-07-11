# ╭──────────────────────────────────────────────────────────────────────────╮
# │                    Engineering Test Report Generator                     │
# │                    View Component (MVC) + FORMULA EDITOR                │
# │                         WITH CSV FORMULA SUPPORT                        │
# ╰──────────────────────────────────────────────────────────────────────────╯

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tksheet import Sheet
import os

class ScrollableFrame(tk.Frame):
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
        
        # Mouse wheel support
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind("<Button-4>", self._on_mousewheel)
        self.canvas.bind("<Button-5>", self._on_mousewheel)
        self.canvas.focus_set()
        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())
        
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _on_mousewheel(self, event):
        if hasattr(event, 'delta'):
            delta = event.delta
        else:
            delta = 120 if event.num == 4 else -120 if event.num == 5 else 0
        self.canvas.yview_scroll(int(-1 * (delta / 120)), "units")

class FormulaView(tk.Tk):
    def __init__(self, model_class=None):
        super().__init__()
        self.title("Engineering Test Report Generator - Formula Editor")
        self.geometry("1600x1000")
        
        # MVC references
        self.model = None
        self.controller = None
        
        # State
        self.report_path = None
        self.current_test = None
        self.current_section = None
        self.current_section_id = None
        
        # GUI Components
        self.tree = None
        self.center_scrollable = None
        self.current_sheets = {}
        self.equipment_frame = None
        self.equipment_vars = {}
        
        # Formula editor components
        self.formula_bar = None
        self.selected_cell = None
        self.clipboard_data = None
        
        self.create_menu()
        self.create_panes()

    def create_menu(self):
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
        # Create formula bar at top
        self.create_formula_bar()
        
        # Main horizontal pane
        main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)
        
        # Left: File Manager
        self.create_file_manager_pane(main_pane)
        
        # Right: Vertical split [Center Editor] above [Equipment Manager]
        right_pane = tk.PanedWindow(main_pane, orient=tk.VERTICAL)
        main_pane.add(right_pane)
        
        # Center: Editor pane
        self.create_center_editor_pane(right_pane)
        
        # Bottom: Equipment Manager
        self.create_equipment_manager_pane(right_pane)

    def create_formula_bar(self):
        """Create formula bar for formula editing"""
        formula_frame = tk.Frame(self, height=30, bg='#f0f0f0')
        formula_frame.pack(fill=tk.X, padx=5, pady=2)
        formula_frame.pack_propagate(False)
        
        tk.Label(formula_frame, text="fx", bg='#f0f0f0', font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(5, 10))
        
        self.formula_bar = tk.Entry(formula_frame, font=("Consolas", 11))
        self.formula_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.formula_bar.bind("<Return>", self.on_formula_bar_enter)

    def create_file_manager_pane(self, parent):
        """Create left file manager pane"""
        file_frame = tk.Frame(parent, width=300, bg='#2d2d30')
        file_frame.pack_propagate(False)
        parent.add(file_frame, minsize=250)
        
        # File Manager Header
        header_frame = tk.Frame(file_frame, bg='#2d2d30', height=30)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="EXPLORER", bg='#2d2d30', fg='white', 
                font=("Arial", 9, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Tree View
        tree_frame = tk.Frame(file_frame, bg='#1e1e1e')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tree = ttk.Treeview(tree_frame, style="Custom.Treeview")
        tree_scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        tree_scrollbar.pack(side="right", fill="y")
        
        # Bind events
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Button-1>", self.on_tree_click)

    def create_center_editor_pane(self, parent):
        """Create center editor pane with scrollable content"""
        center_frame = tk.Frame(parent, bg='white')
        parent.add(center_frame, minsize=500)
        
        # Header
        header_frame = tk.Frame(center_frame, bg='#007acc', height=35)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        self.center_title = tk.Label(header_frame, text="Select a section to edit", 
                                   bg='#007acc', fg='white', font=("Arial", 11, "bold"))
        self.center_title.pack(side=tk.LEFT, padx=15, pady=8)
        
        # Scrollable content area
        self.center_scrollable = ScrollableFrame(center_frame, bg='white')
        self.center_scrollable.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.show_no_report_message()

    def create_equipment_manager_pane(self, parent):
        """Create bottom equipment manager pane"""
        equipment_main_frame = tk.Frame(parent, height=200, bg='#f8f8f8')
        equipment_main_frame.pack_propagate(False)
        parent.add(equipment_main_frame, minsize=150)
        
        # Header
        header_frame = tk.Frame(equipment_main_frame, bg='#e1e1e1', height=30)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        tk.Label(header_frame, text="Equipment Used", bg='#e1e1e1', 
                font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Scrollable equipment list
        equipment_scroll_frame = tk.Frame(equipment_main_frame)
        equipment_scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        equipment_canvas = tk.Canvas(equipment_scroll_frame, bg='white')
        equipment_scrollbar = tk.Scrollbar(equipment_scroll_frame, orient="vertical", 
                                         command=equipment_canvas.yview)
        self.equipment_frame = tk.Frame(equipment_canvas, bg='white')
        
        self.equipment_frame.bind(
            "<Configure>",
            lambda e: equipment_canvas.configure(scrollregion=equipment_canvas.bbox("all"))
        )
        
        equipment_canvas.create_window((0, 0), window=self.equipment_frame, anchor="nw")
        equipment_canvas.configure(yscrollcommand=equipment_scrollbar.set)
        
        equipment_canvas.pack(side="left", fill="both", expand=True)
        equipment_scrollbar.pack(side="right", fill="y")

    def create_sheet_section(self, parent, title, subtitle, data, section_name):
        """Create a titled sheet section with formula support"""
        section_frame = tk.Frame(parent, bg='white', relief='solid', bd=1)
        section_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Title frame
        title_frame = tk.Frame(section_frame, bg='#f0f0f0', height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(title_frame, text=title, bg='#f0f0f0', 
                font=("Arial", 14, "bold")).pack(anchor=tk.W, padx=15, pady=(10, 2))
        
        if subtitle:
            tk.Label(title_frame, text=subtitle, bg='#f0f0f0', 
                    font=("Arial", 10), fg='#666').pack(anchor=tk.W, padx=15, pady=(0, 8))
        
        # Sheet frame
        sheet_frame = tk.Frame(section_frame, bg='white')
        sheet_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create sheet with formula support
        sheet = Sheet(sheet_frame, 
                     data=data if data else [[""] * 5 for _ in range(10)],
                     headers=data[0] if data and len(data) > 0 else None)
        
        # Configure sheet bindings - disable default copy/paste for formula handling
        sheet.enable_bindings(("single_select", "arrowkeys", "edit_cell", "cell_select", 
                              "rc_select", "cut", "delete", "undo", "drag_select"))
        
        # Bind formula editor events
        sheet.extra_bindings("end_edit_cell", lambda event: self.on_cell_edited(event, section_name))
        sheet.extra_bindings("cell_select", lambda event: self.on_cell_selected(event, section_name))
        sheet.extra_bindings("delete_key", lambda event: self.on_delete_key(event, section_name))
        
        # Custom copy/paste for formulas
        self.bind("<Control-c>", lambda event: self.copy_cells(section_name))
        self.bind("<Control-v>", lambda event: self.paste_cells(section_name))
        
        sheet.pack(fill=tk.BOTH, expand=True)
        
        # Store sheet reference
        self.current_sheets[section_name] = sheet
        
        # Auto-size sheet
        try:
            sheet.set_all_cell_sizes_to_text()
        except:
            pass
        
        return sheet

    def on_formula_bar_enter(self, event):
        """Handle formula bar enter key"""
        if self.controller and self.selected_cell and self.current_section_id:
            row, col, section_name = self.selected_cell
            content = self.formula_bar.get()
            self.controller.set_cell_content(self.current_section_id, row, col, content)

    def on_cell_selected(self, event, section_name):
        """Handle cell selection"""
        if not self.controller:
            return
        
        sheet = self.current_sheets.get(section_name)
        if not sheet:
            return
        
        selected = sheet.get_currently_selected()
        if not selected:
            return
        
        row, col = selected.row, selected.column
        self.selected_cell = (row, col, section_name)
        
        # Update formula bar
        if self.current_section_id:
            formula = self.controller.get_formula(self.current_section_id, row, col)
            if formula:
                display_value = formula
            else:
                display_value = sheet.get_cell_data(row, col) or ""
            
            self.formula_bar.delete(0, tk.END)
            self.formula_bar.insert(0, str(display_value))

    def on_cell_edited(self, event, section_name):
        """Handle cell editing"""
        if not self.controller:
            return
        
        row, col = event["row"], event["column"]
        sheet = self.current_sheets.get(section_name)
        if sheet and self.current_section_id:
            val = sheet.get_cell_data(row, col)
            self.controller.set_cell_content(self.current_section_id, row, col, val)

    def on_delete_key(self, event, section_name):
        """Handle delete key"""
        if not self.controller:
            return
        
        sheet = self.current_sheets.get(section_name)
        if not sheet:
            return
        
        selected = sheet.get_currently_selected()
        if not selected:
            return
        
        row, col = selected.row, selected.column
        
        if self.current_section_id:
            self.controller.clear_cell(self.current_section_id, row, col)
            
        # Update formula bar
        self.formula_bar.delete(0, tk.END)

    def highlight_formula_cells(self, section_name, formula_cells):
        """Highlight cells that contain formulas"""
        sheet = self.current_sheets.get(section_name)
        if not sheet:
            return
        
        for (row, col) in formula_cells:
            try:
                sheet.highlight_cells(row, col, bg="#dae7f5")
            except:
                pass

    def set_sheet_data(self, section_name, data):
        """Set data for a specific sheet"""
        sheet = self.current_sheets.get(section_name)
        if sheet and data:
            sheet.set_sheet_data(data)
            try:
                sheet.set_all_cell_sizes_to_text()
            except:
                pass

    def get_sheet_data(self, section_name):
        """Get data from a specific sheet"""
        sheet = self.current_sheets.get(section_name)
        if sheet:
            return sheet.get_sheet_data()
        return []

    def load_cover_page_sections(self, sections):
        """Load cover page sections into scrollable sheets"""
        self.clear_center_content()
        self.current_section_id = "cover_page"
        
        for widget in self.center_scrollable.scrollable_frame.winfo_children():
            widget.destroy()
        
        for section_name, data in sections.items():
            title = section_name.replace('_', ' ').title()
            sheet = self.create_sheet_section(self.center_scrollable.scrollable_frame, 
                                            title, "", data, section_name)
            
            # Load formulas for this section
            if self.controller:
                formula_cells = self.controller.get_formula_cells(f"cover_{section_name}")
                self.highlight_formula_cells(section_name, formula_cells)

    def clear_center_content(self):
        """Clear all content from center pane"""
        for widget in self.center_scrollable.scrollable_frame.winfo_children():
            widget.destroy()
        self.current_sheets.clear()

    def show_no_report_message(self):
        """Show message when no report is loaded"""
        self.clear_center_content()
        message_frame = tk.Frame(self.center_scrollable.scrollable_frame, bg='white')
        message_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(message_frame, text="Open or Create a Report to Begin", 
                bg='white', font=("Arial", 16), fg='#999').pack(expand=True)

    def populate_tree(self, tree_data):
        """Populate file tree with data"""
        self.tree.delete(*self.tree.get_children())
        
        # Add cover page
        cover_id = self.tree.insert("", "end", text="Cover Page", tags=("cover_page",))
        
        # Add test categories
        for category, tests in tree_data.items():
            if category != "cover_page":
                cat_id = self.tree.insert("", "end", text=category.title(), tags=(category,))
                for test_name in tests:
                    self.tree.insert(cat_id, "end", text=test_name, tags=(category, test_name))

    def load_equipment_list(self, equipment_data):
        """Load equipment checkboxes"""
        for widget in self.equipment_frame.winfo_children():
            widget.destroy()
        self.equipment_vars.clear()
        
        for i, equipment in enumerate(equipment_data):
            if not equipment or len(equipment) < 7:
                continue
            
            # Format equipment display
            parts = [str(part).strip() for part in equipment[:5] if str(part).strip()]
            display_text = " - ".join(parts) if parts else f"Equipment {i+1}"
            
            var = tk.BooleanVar()
            cb = tk.Checkbutton(self.equipment_frame, text=display_text, variable=var,
                              bg='white', anchor='w', justify='left')
            cb.pack(fill=tk.X, padx=5, pady=1)
            
            self.equipment_vars[str(i)] = var

    def update_title(self, report_name=None):
        """Update window title"""
        base_title = "Engineering Test Report Generator - Formula Editor"
        if report_name:
            self.title(f"{base_title} - {report_name}")
        else:
            self.title(base_title)

    # Menu command delegates
    def new_report(self):
        if self.controller: self.controller.new_report()
    
    def open_report(self):
        if self.controller: self.controller.open_report()
    
    def save_current(self):
        if self.controller: self.controller.save_current()
    
    def add_test(self):
        if self.controller: self.controller.add_test()
    
    def delete_test(self):
        if self.controller: self.controller.delete_test()
    
    def generate_report(self):
        if self.controller: self.controller.generate_report()
    
    def send_report(self):
        if self.controller: self.controller.send_report()
    
    def on_tree_select(self, event):
        if self.controller: self.controller.on_tree_selection(self.tree.selection())
    
    def on_tree_click(self, event):
        if self.controller: self.controller.on_tree_click(self.tree.identify_row(event.y))

    # Utility methods
    def set_controller(self, controller):
        self.controller = controller
    
    def set_model(self, model):
        self.model = model
    
    def show_message(self, title, message, msg_type="info"):
        if msg_type == "info":
            messagebox.showinfo(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        elif msg_type == "error":
            messagebox.showerror(title, message)
    
    def ask_directory(self, title):
        return filedialog.askdirectory(title=title)
    
    def ask_string(self, title, prompt):
        return simpledialog.askstring(title, prompt)

    def copy_cells(self, section_name):
        """Copy cells with formula support"""
        if not self.controller:
            return "break"
        
        sheet = self.current_sheets.get(section_name)
        if not sheet:
            return "break"
        
        selected = sheet.get_currently_selected()
        if not selected:
            return "break"
        
        # Handle multiple cell selection
        if hasattr(selected, 'rows') and hasattr(selected, 'columns'):
            # Multiple cells selected
            self.clipboard_data = {
                'type': 'multi_cell',
                'data': {},
                'section_name': section_name
            }
            
            for i, row in enumerate(selected.rows):
                for j, col in enumerate(selected.columns):
                    actual_row = selected.row + i
                    actual_col = selected.column + j
                    
                    formula = self.controller.get_formula(self.current_section_id, actual_row, actual_col)
                    if formula:
                        self.clipboard_data['data'][(i, j)] = {
                            'type': 'formula',
                            'content': formula,
                            'source': (actual_row, actual_col)
                        }
                    else:
                        value = sheet.get_cell_data(actual_row, actual_col)
                        self.clipboard_data['data'][(i, j)] = {
                            'type': 'value',
                            'content': str(value) if value else ""
                        }
        else:
            # Single cell selected
            row, col = selected.row, selected.column
            
            formula = self.controller.get_formula(self.current_section_id, row, col)
            if formula:
                self.clipboard_data = {
                    'type': 'formula',
                    'content': formula,
                    'source': (row, col),
                    'section_name': section_name
                }
            else:
                value = sheet.get_cell_data(row, col)
                self.clipboard_data = {
                    'type': 'value',
                    'content': str(value) if value else "",
                    'section_name': section_name
                }
        
        return "break"

    def paste_cells(self, section_name):
        """Paste cells with formula adjustment support"""
        if not self.controller or not self.clipboard_data:
            return "break"
        
        sheet = self.current_sheets.get(section_name)
        if not sheet:
            return "break"
        
        selected = sheet.get_currently_selected()
        if not selected:
            return "break"
        
        target_row, target_col = selected.row, selected.column
        
        if self.clipboard_data['type'] == 'multi_cell':
            # Pasting multiple cells
            data = self.clipboard_data['data']
            
            # Check for overwrite warning
            overwrite_cells = []
            for (row_offset, col_offset), cell_data in data.items():
                paste_row = target_row + row_offset
                paste_col = target_col + col_offset
                
                existing_value = sheet.get_cell_data(paste_row, paste_col)
                existing_formula = self.controller.get_formula(self.current_section_id, paste_row, paste_col)
                
                if existing_value or existing_formula:
                    overwrite_cells.append(f"{chr(65 + paste_col)}{paste_row + 1}")
            
            if overwrite_cells:
                from tkinter import messagebox
                response = messagebox.askyesno(
                    "Overwrite Warning",
                    f"This will overwrite data in cells: {', '.join(overwrite_cells[:5])}{'...' if len(overwrite_cells) > 5 else ''}\n\nDo you want to continue?"
                )
                if not response:
                    return "break"
            
            # Paste all cells
            for (row_offset, col_offset), cell_data in data.items():
                paste_row = target_row + row_offset
                paste_col = target_col + col_offset
                
                if cell_data['type'] == 'formula':
                    source_row, source_col = cell_data['source']
                    adjusted_formula = self.controller.adjust_formula_references(
                        cell_data['content'], source_row, source_col, paste_row, paste_col
                    )
                    self.controller.set_cell_content(self.current_section_id, paste_row, paste_col, adjusted_formula)
                else:
                    self.controller.set_cell_content(self.current_section_id, paste_row, paste_col, cell_data['content'])
            
        elif self.clipboard_data['type'] == 'formula':
            # Single formula cell
            source_row, source_col = self.clipboard_data['source']
            adjusted_formula = self.controller.adjust_formula_references(
                self.clipboard_data['content'], source_row, source_col, target_row, target_col
            )
            self.controller.set_cell_content(self.current_section_id, target_row, target_col, adjusted_formula)
            
            # Update formula bar
            self.formula_bar.delete(0, tk.END)
            self.formula_bar.insert(0, adjusted_formula)
        else:
            # Single value cell
            content = self.clipboard_data['content']
            self.controller.set_cell_content(self.current_section_id, target_row, target_col, content)
            
            # Update formula bar
            self.formula_bar.delete(0, tk.END)
            self.formula_bar.insert(0, content)
        
        return "break"
