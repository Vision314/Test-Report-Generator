import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv
from tksheet import Sheet

class CSVEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Tkinter CSV Editor (Excel-like)")

        self.tabs = {}  # Stores sheet widgets per tab

        # Setup menu bar
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        self._create_menus()

        # Toolbar
        self.toolbar = tk.Frame(root)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        tk.Button(self.toolbar, text="New Tab", command=self.new_tab).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(self.toolbar, text="Open CSV", command=self.open_csv).pack(side=tk.LEFT, padx=2, pady=2)
        tk.Button(self.toolbar, text="Save CSV", command=self.save_csv).pack(side=tk.LEFT, padx=2, pady=2)

        # Notebook for multiple tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create an initial blank tab
        self.new_tab()

    def _create_menus(self):
        # File menu
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="New Tab", command=self.new_tab)
        file_menu.add_command(label="Open CSV", command=self.open_csv)
        file_menu.add_command(label="Save CSV", command=self.save_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(self.menu, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.edit_undo)
        edit_menu.add_command(label="Redo", command=self.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.edit_cut)
        edit_menu.add_command(label="Copy", command=self.edit_copy)
        edit_menu.add_command(label="Paste", command=self.edit_paste)
        self.menu.add_cascade(label="Edit", menu=edit_menu)

        # View menu
        view_menu = tk.Menu(self.menu, tearoff=0)
        view_menu.add_command(label="Toggle Grid Lines", command=self.toggle_grid_lines)
        self.menu.add_cascade(label="View", menu=view_menu)

    def new_tab(self, csv_data=None, title="Untitled"):
        frame = tk.Frame(self.notebook)
        frame.pack(fill=tk.BOTH, expand=True)

        sheet = Sheet(frame)
        sheet.enable_bindings((
            "single_select",
            "arrowkeys",
            "edit_cell",
            "undo",
            "copy",
            "cut",
            "paste"
        ))
        sheet.pack(fill=tk.BOTH, expand=True)

        if csv_data:
            sheet.set_sheet_data(csv_data)
        else:
            sheet.set_sheet_data([["" for _ in range(5)] for _ in range(10)])

        self.notebook.add(frame, text=title)
        self.tabs[frame] = sheet
        self.notebook.select(frame)

    def open_csv(self):
        path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv")]
        )
        if not path:
            return
        try:
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                data = list(reader)
            self.new_tab(csv_data=data, title=path.split("/")[-1])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV:\n{e}")

    def save_csv(self):
        current_tab = self.notebook.select()
        if not current_tab:
            return

        sheet = self.tabs[self.notebook.nametowidget(current_tab)]
        data = sheet.get_sheet_data()

        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                            filetypes=[("CSV Files", "*.csv")])
        if not path:
            return
        try:
            with open(path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerows(data)
            messagebox.showinfo("Saved", f"CSV saved successfully to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save CSV:\n{e}")

    # Edit menu commands
    def get_current_sheet(self):
        current_tab = self.notebook.select()
        if not current_tab:
            return None
        return self.tabs[self.notebook.nametowidget(current_tab)]

    def edit_undo(self):
        sheet = self.get_current_sheet()
        if sheet:
            sheet.undo()

    def edit_redo(self):
        sheet = self.get_current_sheet()
        if sheet:
            sheet.redo()

    def edit_cut(self):
        sheet = self.get_current_sheet()
        if sheet:
            sheet.cut()

    def edit_copy(self):
        sheet = self.get_current_sheet()
        if sheet:
            sheet.copy()

    def edit_paste(self):
        sheet = self.get_current_sheet()
        if sheet:
            sheet.paste()

    # View menu commands
    def toggle_grid_lines(self):
        sheet = self.get_current_sheet()
        if sheet:
            current = sheet.options("show_grid")
            sheet.show_grid(not current)

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVEditor(root)
    root.mainloop()
