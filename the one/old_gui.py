import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd

class ReportEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Report Generator")
        self.geometry("1200x700")

        self.report_path = None
        self.current_csv_path = None
        self.table_data = pd.DataFrame()

        self.create_menu()
        self.create_file_pane()
        self.create_table_editor()
        self.populate_file_pane()

    def create_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="New Report", command=self.new_report)
        filemenu.add_command(label="Open Report", command=self.open_report)
        filemenu.add_command(label="Save", command=self.save_report)
        filemenu.add_command(label="Save As", command=self.save_as_report)
        filemenu.add_separator()
        filemenu.add_command(label="Quit", command=self.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.config(menu=menubar)

    def create_file_pane(self):
        left_frame = tk.Frame(self, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(left_frame, text="Tests").pack(anchor='nw')
        self.tree = ttk.Treeview(left_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.load_csv_from_tree)

        tk.Button(left_frame, text="New Test", command=self.create_new_test).pack(fill=tk.X)

    def create_table_editor(self):
        self.editor_frame = tk.Frame(self)
        self.editor_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.table_frame = tk.Frame(self.editor_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        self.toolbar = tk.Frame(self.editor_frame)
        self.toolbar.pack(fill=tk.X)
        tk.Button(self.toolbar, text="Add Row", command=self.add_row).pack(side=tk.LEFT)
        tk.Button(self.toolbar, text="Add Column", command=self.add_column).pack(side=tk.LEFT)
        tk.Button(self.toolbar, text="Delete Row", command=self.delete_row).pack(side=tk.LEFT)
        tk.Button(self.toolbar, text="Delete Column", command=self.delete_column).pack(side=tk.LEFT)

        self.nameplate_var = tk.BooleanVar()
        self.specified_var = tk.BooleanVar()
        tk.Checkbutton(self.toolbar, text="Nameplate", variable=self.nameplate_var).pack(side=tk.LEFT)
        tk.Checkbutton(self.toolbar, text="Specified", variable=self.specified_var).pack(side=tk.LEFT)

    def populate_file_pane(self):
        if not self.report_path:
            return
        self.tree.delete(*self.tree.get_children())
        for root, dirs, files in os.walk(os.path.join(self.report_path, "files")):
            for file in files:
                if file.endswith(".csv"):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, self.report_path)
                    parts = rel_path.split(os.sep)
                    category = parts[1] if len(parts) > 2 else "Uncategorized"
                    test_name = parts[-1][:-4]  # Remove .csv
                    self.tree.insert("", "end", text=f"{category} - {test_name}", values=(full_path,))

    def load_csv_from_tree(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        csv_path = self.tree.item(selected[0], "values")[0]
        if os.path.exists(csv_path):
            self.table_data = pd.read_csv(csv_path, header=None)
            self.current_csv_path = csv_path
            self.render_table()

    def render_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.entries = []
        for r, row in self.table_data.iterrows():
            row_entries = []
            for c, val in enumerate(row):
                e = tk.Entry(self.table_frame, width=15)
                e.grid(row=r, column=c)
                e.insert(0, val)
                row_entries.append(e)
            self.entries.append(row_entries)

    def update_table_data(self):
        self.table_data = pd.DataFrame([[entry.get() for entry in row] for row in self.entries])

    def add_row(self):
        self.update_table_data()
        empty_row = ["" for _ in range(len(self.table_data.columns))]
        self.table_data.loc[len(self.table_data)] = empty_row
        self.render_table()

    def add_column(self):
        self.update_table_data()
        self.table_data[len(self.table_data.columns)] = ""
        self.render_table()

    def delete_row(self):
        self.update_table_data()
        if len(self.table_data) > 0:
            self.table_data = self.table_data.iloc[:-1]
        self.render_table()

    def delete_column(self):
        self.update_table_data()
        if len(self.table_data.columns) > 0:
            self.table_data = self.table_data.drop(columns=self.table_data.columns[-1])
        self.render_table()

    def new_report(self):
        path = filedialog.askdirectory(title="Select New Report Folder")
        if path:
            self.report_path = path
            os.makedirs(os.path.join(path, "files"), exist_ok=True)
            os.makedirs(os.path.join(path, "cover_page/csv"), exist_ok=True)
            os.makedirs(os.path.join(path, "cover_page/images"), exist_ok=True)
            os.makedirs(os.path.join(path, "cover_page/latex"), exist_ok=True)
            self.populate_file_pane()

    def open_report(self):
        path = filedialog.askdirectory(title="Select Report Folder")
        if path and os.path.exists(path):
            self.report_path = path
            self.populate_file_pane()

    def save_report(self):
        if self.current_csv_path:
            self.update_table_data()
            self.table_data.to_csv(self.current_csv_path, index=False, header=False)
            messagebox.showinfo("Saved", f"Saved: {self.current_csv_path}")

    def save_as_report(self):
        if not self.report_path:
            return
        save_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if save_path:
            self.update_table_data()
            self.table_data.to_csv(save_path, index=False, header=False)
            self.populate_file_pane()

    def create_new_test(self):
        if not self.report_path:
            messagebox.showerror("Error", "You must create or open a report first.")
            return

        category = simpledialog.askstring("New Test", "Enter category (e.g. 'Input'):")
        test_name = simpledialog.askstring("New Test", "Enter test name (e.g. 'Inrush Current'):")

        if not category or not test_name:
            messagebox.showwarning("Incomplete", "Both category and test name must be provided.")
            return

        base_path = os.path.join(self.report_path, "files", category, test_name)
        os.makedirs(os.path.join(base_path, "csv"), exist_ok=True)
        os.makedirs(os.path.join(base_path, "images"), exist_ok=True)
        os.makedirs(os.path.join(base_path, "latex"), exist_ok=True)

        csv_path = os.path.join(base_path, "csv", "data.csv")
        df = pd.DataFrame([["" for _ in range(4)] for _ in range(5)])
        df.iloc[0, 0] = category
        df.iloc[1, 0] = test_name
        df.to_csv(csv_path, index=False, header=False)

        self.populate_file_pane()
        messagebox.showinfo("New Test Created", f"Test '{test_name}' created in category '{category}'.")

if __name__ == "__main__":
    app = ReportEditor()
    app.mainloop()
