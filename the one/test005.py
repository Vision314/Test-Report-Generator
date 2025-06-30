import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from tksheet import Sheet
import xlrd
import xlwt

# ------------------------------------------------------------------------------
# ------ Configuration ---------------------------------------------------------
# ------------------------------------------------------------------------------
STRUCTURE = {
    "cover_page": ["equipment_used", "general_specifications", "product_information", "testing_and_review"],
    "input": ["input_current", "no_load_input_power", "inrush_current", "efficiency", "power_factor"],
    "output": ["turn_on_delay", "output_voltage_tolerance", "load_regulation", "line_regulation",
               "ripple", "transient_response", "startup_overshoot", "hold_up_time",
               "aux_output_voltage_regulation", "aux_output_current"],
    "protections": ["over_voltage_protection", "over_current_protection", "short_circuit_protection"],
    "safety": ["dielectric_withstand_voltage", "output_touch_current", "earth_leakage_current"],
    "emc": ["conducted_emissions", "radiated_emissions", "electrostatic_discharge_immunity",
            "EFT_burst_immunity", "line_surge_immunity", "voltage_dip_immunity"]
}
SUBFOLDERS = ['xls', 'images', 'latex']

def display_name(name: str) -> str:
    """Convert folder_name like 'inrush_current' to 'Inrush Current'."""
    return name.replace('_', ' ').title()

def ensure_xls_file(path: str):
    """
    Ensure that 'data.xls' or 'equipment_used.xls' exists with a valid Excel sheet.
    Creates a new .xls with at least one empty sheet if the file is missing or empty.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        book = xlwt.Workbook()
        book.add_sheet('Sheet1')
        book.save(path)

def ensure_structure(base: str):
    """
    Create the full project folder structure inside 'base',
    including valid .xls files for all tests and cover pages.
    """
    for category, tests in STRUCTURE.items():
        for test in tests:
            test_dir = os.path.join(base, category, test)
            for sf in SUBFOLDERS:
                os.makedirs(os.path.join(test_dir, sf), exist_ok=True)
            for xls_file in ('data.xls', 'equipment_used.xls'):
                path = os.path.join(test_dir, 'xls', xls_file)
                ensure_xls_file(path)

# ------------------------------------------------------------------------------
# ------ Main Application ------------------------------------------------------
# ------------------------------------------------------------------------------
class TestEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Engineering Test Report Generator")
        self.geometry("1200x800")
        self.report_path = None        # Root directory of the open report
        self.current_test = None       # Path to the currently selected test folder

        self.create_menu()
        self.create_panes()
        self.load_report(None)

    # --------------------- Menu Creation ---------------------
    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Report", command=self.new_report)
        file_menu.add_command(label="Open Report", command=self.open_report)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=lambda: self.sheet.undo())
        edit_menu.add_command(label="Redo", command=lambda: self.sheet.redo())
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.config(menu=menubar)

    # --------------------- Pane Layout Creation ---------------------
    def create_panes(self):
        # Main horizontal layout: [File Explorer] | [Editor + Equipment]
        main_pane = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # -- Left Pane: File Explorer with toolbar
        left_frame = ttk.Frame(main_pane, width=250)
        fl_toolbar = ttk.Frame(left_frame)
        ttk.Label(fl_toolbar, text="File Manager").pack(side=tk.LEFT, padx=5)
        ttk.Button(fl_toolbar, text="+", command=self.add_test).pack(side=tk.LEFT)
        ttk.Button(fl_toolbar, text="–", command=self.delete_entry).pack(side=tk.LEFT)
        fl_toolbar.pack(fill=tk.X, pady=(0, 2))

        self.tree = ttk.Treeview(left_frame, show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        main_pane.add(left_frame)

        # -- Right Pane: vertical split [Editor] above [Equipment]
        right_pane = tk.PanedWindow(main_pane, orient=tk.VERTICAL)
        main_pane.add(right_pane)

        # Center Pane: Sheet editor with toolbar
        center_frame = ttk.Frame(right_pane)
        editor_toolbar = ttk.Frame(center_frame)
        ttk.Label(editor_toolbar, text="Editor").pack(side=tk.LEFT, padx=5)
        ttk.Button(editor_toolbar, text="Save", command=self.save_data).pack(side=tk.LEFT)
        ttk.Button(editor_toolbar, text="Add Image", command=self.add_image).pack(side=tk.LEFT)
        editor_toolbar.pack(fill=tk.X, pady=(0, 2))

        self.sheet = Sheet(center_frame, enable_bindings=('all',))
        self.sheet.pack(fill=tk.BOTH, expand=True)
        right_pane.add(center_frame, stretch="always")

        # Bottom Pane: Equipment Used with toolbar
        bottom_frame = ttk.Frame(right_pane, height=200)
        equip_toolbar = ttk.Frame(bottom_frame)
        ttk.Label(equip_toolbar, text="Equipment Used").pack(side=tk.LEFT, padx=5)
        ttk.Button(equip_toolbar, text="Refresh", command=self.load_equip).pack(side=tk.LEFT)
        equip_toolbar.pack(fill=tk.X, pady=(0, 2))

        self.equip_frame = ttk.Frame(bottom_frame)
        self.equip_frame.pack(fill=tk.BOTH, expand=True)
        right_pane.add(bottom_frame)

    # --------------------- Report Management ---------------------
    def new_report(self):
        """Prompt for a new report folder and initialize its structure."""
        dlg = tk.Toplevel(self); dlg.title("New Report")
        ttk.Label(dlg, text="Parent Folder:").pack()
        parent_entry = tk.Entry(dlg, width=50); parent_entry.pack()
        ttk.Button(dlg, text="Browse", command=lambda: self._browse(parent_entry)).pack()

        ttk.Label(dlg, text="Report Name:").pack()
        name_entry = tk.Entry(dlg); name_entry.pack()
        ttk.Button(dlg, text="Create",
                   command=lambda: self._create_report(parent_entry.get(), name_entry.get(), dlg)).pack()

    def _browse(self, entry):
        p = filedialog.askdirectory()
        if p: entry.delete(0, tk.END); entry.insert(0, p)

    def _create_report(self, parent, name, dlg):
        target = os.path.join(parent, name)
        if not parent or not name:
            return messagebox.showerror("Invalid input", "Please fill in both fields.")
        if os.path.exists(target):
            return messagebox.showerror("Exists", "The report folder already exists.")

        ensure_structure(target)
        self.load_report(target)
        dlg.destroy()

    def open_report(self):
        """Open an existing report folder."""
        path = filedialog.askdirectory()
        if path:
            self.load_report(path)

    def load_report(self, path):
        """
        Load the project tree from the selected report folder.
        Clears previous content and resets the editor and equipment panes.
        """
        self.report_path = path
        self.tree.delete(*self.tree.get_children())
        self.sheet.set_sheet_data([[""]])
        for widget in self.equip_frame.winfo_children():
            widget.destroy()

        if not path:
            return

        for cat, tests in STRUCTURE.items():
            cat_node = self.tree.insert("", "end", text=display_name(cat), open=True)
            for t in tests:
                folder = os.path.join(path, cat, t)
                self.tree.insert(cat_node, "end", text=display_name(t), values=(folder,))

    # --------------------- Sheet Data Handling ---------------------
    def on_select(self, event):
        """Called when a test (or subfolder) is selected in the tree."""
        sel = self.tree.selection()
        if not sel:
            return

        node = self.tree.item(sel[0])
        vals = node.get("values")
        if not vals:
            return  # Skip category nodes

        folder = vals[0]
        self.current_test = folder
        xls_path = os.path.join(folder, 'xls', 'data.xls')

        data = [[""]]  # default blank grid
        try:
            if os.path.exists(xls_path) and os.path.getsize(xls_path) > 0:
                wb = xlrd.open_workbook(xls_path)
                sh = wb.sheet_by_index(0)
                data = [sh.row_values(r) for r in range(sh.nrows)]
        except Exception as e:
            print(f"[Warning] Could not open data.xls: {e}")

        self.sheet.set_sheet_data(data)
        self.load_equip()

    def save_data(self):
        """Write current sheet data to the test’s data.xls file."""
        if not self.current_test:
            return messagebox.showwarning("No Test", "Please select a test to save.")

        data = self.sheet.get_sheet_data(return_copy=True)
        xls_path = os.path.join(self.current_test, 'xls', 'data.xls')

        book = xlwt.Workbook()
        ws = book.add_sheet('Sheet1')
        for r, row in enumerate(data):
            for c, val in enumerate(row):
                ws.write(r, c, val)

        book.save(xls_path)
        messagebox.showinfo("Saved", f"Data written to:\n{xls_path}")

    # --------------------- Image Insertion ---------------------
    def add_image(self):
        """Copy an image into the test's images folder."""
        if not self.current_test:
            return messagebox.showwarning("No Test", "Select a test to add an image.")

        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if not path:
            return

        caption = simpledialog.askstring("Caption", "Enter image caption:")
        dest = os.path.join(self.current_test, 'images', os.path.basename(path))
        shutil.copy(path, dest)
        messagebox.showinfo("Image Added", "Image copied to:\n" + dest)

    # --------------------- Test Entry Management ---------------------
    def add_test(self):
        """Prompt for new test and add it under a specified category."""
        dlg = tk.Toplevel(self); dlg.title("Add New Test")
        ttk.Label(dlg, text="Category:").pack()
        cat_entry = tk.Entry(dlg); cat_entry.pack()
        ttk.Label(dlg, text="Test Name:").pack()
        name_entry = tk.Entry(dlg); name_entry.pack()

        ttk.Button(dlg, text="Add",
                   command=lambda: self._confirm_add_test(cat_entry.get(), name_entry.get(), dlg)).pack()

    def _confirm_add_test(self, category: str, name: str, dialog):
        if not self.report_path:
            return messagebox.showerror("No Report", "Load or create a report first.")
        if not category or not name:
            return messagebox.showerror("Invalid", "Both fields are required.")

        test_dir = os.path.join(self.report_path, category, name)
        if os.path.exists(test_dir):
            return messagebox.showerror("Exists", "The test already exists.")

        for sub in SUBFOLDERS:
            os.makedirs(os.path.join(test_dir, sub), exist_ok=True)
        for file in ('data.xls', 'equipment_used.xls'):
            ensure_xls_file(os.path.join(test_dir, 'xls', file))

        self.load_report(self.report_path)
        dialog.destroy()

    def delete_entry(self):
        """Delete the selected test directory."""
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0]).get("values")
        if vals and messagebox.askyesno("Delete", "Delete this test folder?"):
            shutil.rmtree(vals[0])
            self.load_report(self.report_path)

    # --------------------- Equipment Pane Management ---------------------
    def load_equip(self):
        """
        Load master equipment list and reflect current test selections.
        Master list is in: cover_page/xls/equipment_used.xls
        """
        for w in self.equip_frame.winfo_children():
            w.destroy()

        if not self.report_path:
            return

        master_xls = os.path.join(self.report_path, 'cover_page', 'equipment_used', 'xls', 'equipment_used.xls')
        master = []

        try:
            if os.path.exists(master_xls) and os.path.getsize(master_xls) > 0:
                wb = xlrd.open_workbook(master_xls)
                sh = wb.sheet_by_index(0)
                master = [sh.row_values(r)[0] for r in range(sh.nrows)]
        except Exception as e:
            print(f"[Warning] Could not load master equipment list: {e}")

        self.e_vars = {}
        for item in master:
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(self.equip_frame, text=item, variable=var,
                                   command=lambda i=item, v=var: self.toggle_equip(i, v))
            chk.pack(anchor='w')
            self.e_vars[item] = var

        # Now load saved selections for the current test
        if not self.current_test:
            return

        sel_xls = os.path.join(self.current_test, 'xls', 'equipment_used.xls')
        used = set()

        try:
            if os.path.exists(sel_xls) and os.path.getsize(sel_xls) > 0:
                wb = xlrd.open_workbook(sel_xls)
                sh = wb.sheet_by_index(0)
                used = {sh.row_values(r)[0] for r in range(sh.nrows)}
        except Exception as e:
            print(f"[Warning] Could not load test's equipment: {e}")

        for eq in used:
            if eq in self.e_vars:
                self.e_vars[eq].set(True)

    def toggle_equip(self, item: str, var: tk.BooleanVar):
        """Update the current test’s equipment_used.xls when a checkbox is toggled."""
        if not self.current_test:
            return
        sel_xls = os.path.join(self.current_test, 'xls', 'equipment_used.xls')
        used = set()

        try:
            if os.path.exists(sel_xls) and os.path.getsize(sel_xls) > 0:
                wb = xlrd.open_workbook(sel_xls)
                sh = wb.sheet_by_index(0)
                used = {sh.row_values(r)[0] for r in range(sh.nrows)}
        except Exception:
            used = set()

        if var.get():
            used.add(item)
        else:
            used.discard(item)

        book = xlwt.Workbook()
        ws = book.add_sheet('Sheet1')
        for i, eq in enumerate(sorted(used)):
            ws.write(i, 0, eq)
        book.save(sel_xls)

# ------------------------------------------------------------------------------
# ------ Entry Point ----------------------------------------------------------
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app = TestEditorApp()
    app.mainloop()
