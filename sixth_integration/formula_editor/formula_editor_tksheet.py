import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import re
import json
import os
from tksheet import Sheet

class CSVFormulaEditor:
    def __init__(self, root):
        self.root = root
        root.title("CSV Formula Editor with tksheet")
        
        # Initialize data structures
        self.formulas = {}       # {(row,col): formula_string}
        self.dependencies = {}   # {(row,col): set of dependent (row,col)}
        self.filename = None
        self.selected_cell = None
        self.clipboard_data = None

        # Create UI
        self._setup_ui()
        self._load_initial_data()

    def _setup_ui(self):
        # Formula bar
        self.formula_bar = tk.Entry(self.root, font=("Consolas", 12))
        self.formula_bar.grid(row=0, column=0, sticky="ew")
        self.formula_bar.bind("<Return>", self.on_formula_bar_enter)

        # Sheet
        self.sheet = Sheet(self.root)
        self.sheet.grid(row=1, column=0, sticky="nsew")
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Configure sheet - disable default copy/paste for custom formula handling
        self.sheet.enable_bindings(("single_select", "arrowkeys", "edit_cell", "cell_select", 
                                    "rc_select", "cut", "delete", "undo", "drag_select"))
        self.sheet.extra_bindings("end_edit_cell", self.on_cell_edited)
        self.sheet.extra_bindings("cell_select", self.on_cell_selected)
        self.sheet.extra_bindings("delete_key", self.on_delete_key)
        
        # Custom copy/paste for formulas
        self.root.bind("<Control-c>", self.copy_cell)
        self.root.bind("<Control-v>", self.paste_cell)

        # Menu
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open CSV", command=self.open_csv)
        filemenu.add_command(label="Save CSV", command=self.save_csv)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

    def _load_initial_data(self):
        # Load dummy data
        self.data = [["" for _ in range(10)] for _ in range(20)]
        self.sheet.set_sheet_data(self.data)
        
        # Try loading formulas from default file
        self._load_formulas("formulas.json")

    def _load_formulas(self, filepath):
        """Load formulas from JSON file if it exists."""
        if os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    formulas_str_keys = json.load(f)
                self.formulas = {tuple(map(int, k.split(","))): v for k, v in formulas_str_keys.items()}
                # Highlight all formula cells after loading
                for (row, col) in self.formulas:
                    self.sheet.highlight_cells(row, col, bg="#dae7f5")
                self.recalculate_all()
            except Exception as e:
                print(f"Failed to load {filepath}: {e}")

#
    def open_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
            
        self.filename = path
        
        # Load CSV data
        with open(path, newline="", encoding="utf-8") as f:
            self.data = list(csv.reader(f))
        self.sheet.set_sheet_data(self.data)

        # Load formulas
        self.formulas.clear()
        self.dependencies.clear()
        self._load_formulas(path + ".formulas.json")

#
    def save_csv(self):
        if not self.filename:
            path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                filetypes=[("CSV files", "*.csv")])
            if not path:
                return
            self.filename = path

        # Save CSV
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerows(self.sheet.get_sheet_data())

        # Save formulas
        try:
            formulas_to_save = {f"{k[0]},{k[1]}": v for k, v in self.formulas.items()}
            formula_filename = self.filename.replace(".csv", ".json")
            with open(formula_filename, "w", encoding="utf-8") as f:
                json.dump(formulas_to_save, f, indent=2)
            messagebox.showinfo("Save CSV", f"Saved to {self.filename} and formulas")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save formulas:\n{e}")

    def on_cell_selected(self, event):
        selected = self.sheet.get_currently_selected()
        if not selected:
            return
            
        self.selected_cell = (selected.row, selected.column)
        row, col = self.selected_cell
        
        # Show formula or cell value in formula bar
        display_value = self.formulas.get((row, col), self.sheet.get_cell_data(row, col))
        self.formula_bar.delete(0, tk.END)
        self.formula_bar.insert(0, str(display_value))

    def on_formula_bar_enter(self, event):
        if not self.selected_cell:
            return
            
        self._set_cell_content(self.selected_cell, self.formula_bar.get())

    def on_cell_edited(self, event):
        row, col = event["row"], event["column"]
        val = self.sheet.get_cell_data(row, col)
        self._set_cell_content((row, col), val)

    def _set_cell_content(self, cell, content):
        """Set cell content and handle formula/value logic."""
        row, col = cell
        
        if isinstance(content, str) and content.startswith("="):
            self.formulas[(row, col)] = content
            self.update_dependencies(row, col, content)
            # Highlight formula cells
            self.sheet.highlight_cells(row, col, bg="#dae7f5")
        else:
            self.formulas.pop((row, col), None)
            self.clear_dependencies(row, col)
            self.sheet.set_cell_data(row, col, content)
            # Remove highlighting for non-formula cells
            self.sheet.dehighlight_cells(row, col)
        
        self.recalculate_all()

    def update_dependencies(self, row, col, formula):
        """Update dependency tracking for a formula cell."""
        self.clear_dependencies(row, col)
        refs = re.findall(r"[A-Z]+\d+", formula.upper())
        for ref in refs:
            r, c = self.cell_name_to_index(ref)
            self.dependencies.setdefault((r, c), set()).add((row, col))

    def clear_dependencies(self, row, col):
        """Remove cell from all dependency lists."""
        for dep_set in self.dependencies.values():
            dep_set.discard((row, col))

    def recalculate_all(self):
        """Recalculate all formula cells."""
        visited = set()
        for cell in self.formulas:
            self.evaluate_cell(cell[0], cell[1], visited)

    def evaluate_cell(self, row, col, visited):
        """Evaluate a single cell formula with dependency resolution."""
        if (row, col) in visited:
            return
        visited.add((row, col))

        formula = self.formulas.get((row, col))
        if not formula:
            return

        # Replace cell references with values
        expr = formula[1:]  # Remove '='
        refs = re.findall(r"[A-Z]+\d+", expr.upper())
        for ref in refs:
            r, c = self.cell_name_to_index(ref)
            self.evaluate_cell(r, c, visited)  # Ensure dependency is calculated first
            
            val = self.sheet.get_cell_data(r, c)
            try:
                val = float(val)
            except:
                val = 0
            expr = re.sub(ref, str(val), expr, flags=re.IGNORECASE)

        # Evaluate expression
        try:
            result = eval(expr)
        except Exception:
            result = "ERR"

        self.sheet.set_cell_data(row, col, str(result), redraw=True)

        # Update dependent cells
        for dep in self.dependencies.get((row, col), []):
            self.evaluate_cell(dep[0], dep[1], visited)

    def cell_name_to_index(self, name):
        """Convert cell name (e.g., 'A1') to (row, col) indices."""
        match = re.match(r"([A-Z]+)(\d+)", name.upper())
        if not match:
            return 0, 0
            
        col_letters, row_number = match.groups()
        col_number = 0
        for i, char in enumerate(reversed(col_letters)):
            col_number += (ord(char) - 65 + 1) * (26 ** i)
        return int(row_number) - 1, col_number - 1

    def copy_cell(self, event):
        """Copy cell content (formula if exists, otherwise value)."""
        selected = self.sheet.get_currently_selected()
        if not selected:
            return
            
        # Handle multiple cell selection
        if hasattr(selected, 'rows') and hasattr(selected, 'columns'):
            # Multiple cells selected
            self.clipboard_data = {
                'type': 'multi_cell',
                'data': {},
                'source_range': (selected.row, selected.column, selected.row + len(selected.rows) - 1, selected.column + len(selected.columns) - 1)
            }
            
            for i, row in enumerate(selected.rows):
                for j, col in enumerate(selected.columns):
                    actual_row = selected.row + i
                    actual_col = selected.column + j
                    
                    if (actual_row, actual_col) in self.formulas:
                        self.clipboard_data['data'][(i, j)] = {
                            'type': 'formula',
                            'content': self.formulas[(actual_row, actual_col)],
                            'source': (actual_row, actual_col)
                        }
                    else:
                        value = self.sheet.get_cell_data(actual_row, actual_col)
                        self.clipboard_data['data'][(i, j)] = {
                            'type': 'value',
                            'content': str(value) if value else ""
                        }
        else:
            # Single cell selected
            row, col = selected.row, selected.column
            self.selected_cell = (row, col)
            
            if (row, col) in self.formulas:
                self.clipboard_data = {
                    'type': 'formula',
                    'content': self.formulas[(row, col)],
                    'source': (row, col)
                }
            else:
                value = self.sheet.get_cell_data(row, col)
                self.clipboard_data = {
                    'type': 'value',
                    'content': str(value) if value else ""
                }
        
        return "break"

    def paste_cell(self, event):
        """Paste cell content (formula or value) to selected cell."""
        if not self.clipboard_data:
            return
            
        selected = self.sheet.get_currently_selected()
        if not selected:
            return
            
        target_row, target_col = selected.row, selected.column
        
        if self.clipboard_data['type'] == 'multi_cell':
            # Pasting multiple cells
            data = self.clipboard_data['data']
            
            # Check for overwrite warning
            overwrite_cells = []
            for (row_offset, col_offset), cell_data in data.items():
                paste_row = target_row + row_offset
                paste_col = target_col + col_offset
                
                existing_value = self.sheet.get_cell_data(paste_row, paste_col)
                existing_formula = (paste_row, paste_col) in self.formulas
                
                if existing_value or existing_formula:
                    overwrite_cells.append(f"{chr(65 + paste_col)}{paste_row + 1}")
            
            if overwrite_cells:
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
                    adjusted_formula = self.adjust_formula_references(
                        cell_data['content'], source_row, source_col, paste_row, paste_col
                    )
                    self.formulas[(paste_row, paste_col)] = adjusted_formula
                    self.update_dependencies(paste_row, paste_col, adjusted_formula)
                    self.sheet.highlight_cells(paste_row, paste_col, bg="#dae7f5")
                else:
                    self.formulas.pop((paste_row, paste_col), None)
                    self.clear_dependencies(paste_row, paste_col)
                    self.sheet.set_cell_data(paste_row, paste_col, cell_data['content'])
                    self.sheet.dehighlight_cells(paste_row, paste_col)
            
        elif self.clipboard_data['type'] == 'formula':
            # Single formula cell
            source_row, source_col = self.clipboard_data['source']
            adjusted_formula = self.adjust_formula_references(
                self.clipboard_data['content'], source_row, source_col, target_row, target_col
            )
            self.formulas[(target_row, target_col)] = adjusted_formula
            self.update_dependencies(target_row, target_col, adjusted_formula)
            self.sheet.highlight_cells(target_row, target_col, bg="#dae7f5")
            self.formula_bar.delete(0, tk.END)
            self.formula_bar.insert(0, adjusted_formula)
        else:
            # Single value cell
            content = self.clipboard_data['content']
            self.formulas.pop((target_row, target_col), None)
            self.clear_dependencies(target_row, target_col)
            self.sheet.set_cell_data(target_row, target_col, content)
            self.sheet.dehighlight_cells(target_row, target_col)
            self.formula_bar.delete(0, tk.END)
            self.formula_bar.insert(0, content)
        
        self.recalculate_all()
        return "break"

    def on_delete_key(self, event):
        """Handle delete key to clear cell contents and formulas."""
        selected = self.sheet.get_currently_selected()
        if not selected:
            return
            
        row, col = selected.row, selected.column
        
        # Clear formula if exists
        if (row, col) in self.formulas:
            del self.formulas[(row, col)]
            self.clear_dependencies(row, col)
            self.sheet.dehighlight_cells(row, col)
        
        # Clear cell content
        self.sheet.set_cell_data(row, col, "")
        
        # Update formula bar
        self.formula_bar.delete(0, tk.END)
        
        self.recalculate_all()

    def adjust_formula_references(self, formula, source_row, source_col, target_row, target_col):
        """Adjust cell references in formula when copying to different location."""
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

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVFormulaEditor(root)
    root.mainloop()
