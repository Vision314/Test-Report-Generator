import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import csv
import pandas as pd


class ReportBuilder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Report Builder")
        self.geometry("1000x600")
        self.report_path = None
        self.current_test_path = None
        self.test_data = None

        self.create_menu()
        self.create_layout()

    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Report", command=self.new_report)
        file_menu.add_command(label="Open Report", command=self.open_report)
        file_menu.add_command(label="Save", command=self.save_current_test)
        file_menu.add_command(label="Save As", command=self.save_report_as)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

    def create_layout(self):
        self.paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=1)

        self.left_frame = ttk.Frame(self.paned_window, width=200)
        self.paned_window.add(self.left_frame, weight=1)

        self.test_listbox = tk.Listbox(self.left_frame)
        self.test_listbox.pack(fill=tk.BOTH, expand=True)
        self.test_listbox.bind("<<ListboxSelect>>", self.load_selected_test)

        self.new_test_button = ttk.Button(self.left_frame, text="New Test", command=self.new_test)
        self.new_test_button.pack(pady=5)

        self.notebook = ttk.Notebook(self.paned_window)
        self.paned_window.add(self.notebook, weight=4)

        self.test_editor_tab = ttk.Frame(self.notebook)
        self.cover_page_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.test_editor_tab, text="Test Editor")
        self.notebook.add(self.cover_page_tab, text="Cover Page")

        self.create_test_editor()

    def create_test_editor(self):
        self.table_frame = ttk.Frame(self.test_editor_tab)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        self.table_canvas = tk.Canvas(self.table_frame)
        self.table_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.table_canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = ttk.Frame(self.table_canvas)
        self.table_canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", lambda e: self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all")))

        self.entries = []

    def new_report(self):
        path = filedialog.askdirectory(title="Select New Report Directory")
        if path:
            self.report_path = path
            self.refresh_test_list()

    def open_report(self):
        path = filedialog.askdirectory(title="Select Existing Report Directory")
        if path:
            self.report_path = path
            self.refresh_test_list()

    def save_report_as(self):
        path = filedialog.askdirectory(title="Save Report As")
        if path:
            self.report_path = path
            self.save_current_test()

    def save_current_test(self):
        if self.current_test_path and self.test_data is not None:
            for r, row in enumerate(self.entries):
                for c, cell in enumerate(row):
                    self.test_data.iat[r, c] = cell.get()
            csv_path = os.path.join(self.current_test_path, "csv", "data.csv")
            self.test_data.to_csv(csv_path, index=False, header=False)

    def refresh_test_list(self):
        self.test_listbox.delete(0, tk.END)
        if self.report_path:
            for category in os.listdir(self.report_path):
                category_path = os.path.join(self.report_path, category)
                if os.path.isdir(category_path):
                    for test_name in os.listdir(category_path):
                        test_path = os.path.join(category_path, test_name)
                        csv_path = os.path.join(test_path, "csv", "data.csv")
                        if os.path.exists(csv_path):
                            display_name = f"{category}/{test_name}"
                            self.test_listbox.insert(tk.END, display_name)

    def load_selected_test(self, event):
        if not self.report_path:
            return
        selection = self.test_listbox.curselection()
        if not selection:
            return

        self.save_current_test()  # Auto-save before loading new

        selected = self.test_listbox.get(selection[0])
        category, test_name = selected.split("/")
        self.current_test_path = os.path.join(self.report_path, category, test_name)
        csv_path = os.path.join(self.current_test_path, "csv", "data.csv")

        if os.path.exists(csv_path):
            self.test_data = pd.read_csv(csv_path, header=None, dtype=str).fillna("")
            self.draw_table()

    def draw_table(self):
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
        self.entries = []

        for r, row in self.test_data.iterrows():
            entry_row = []
            for c, val in enumerate(row):
                e = tk.Entry(self.inner_frame, width=15)
                e.grid(row=r, column=c, padx=1, pady=1)
                e.insert(0, val)
                entry_row.append(e)
            self.entries.append(entry_row)

    def new_test(self):
        popup = tk.Toplevel(self)
        popup.title("Create New Test")
        popup.geometry("300x150+{}+{}".format(self.winfo_x() + 100, self.winfo_y() + 100))
        popup.transient(self)
        popup.grab_set()

        tk.Label(popup, text="Category:").pack(pady=5)
        cat_entry = tk.Entry(popup)
        cat_entry.pack()
        cat_entry.focus_set()

        tk.Label(popup, text="Test Name:").pack(pady=5)
        name_entry = tk.Entry(popup)
        name_entry.pack()

        def create():
            category = cat_entry.get().strip()
            test_name = name_entry.get().strip()
            if not category or not test_name:
                messagebox.showwarning("Input Error", "Both fields are required.")
                return

            category_folder = os.path.join(self.report_path, category)
            test_folder = os.path.join(category_folder, test_name)
            os.makedirs(os.path.join(test_folder, "csv"), exist_ok=True)
            os.makedirs(os.path.join(test_folder, "latex"), exist_ok=True)
            os.makedirs(os.path.join(test_folder, "images"), exist_ok=True)

            # Create basic CSV
            csv_path = os.path.join(test_folder, "csv", "data.csv")
            with open(csv_path, "w", newline='') as f:
                writer = csv.writer(f)
                writer.writerow([category, test_name])  # A1, B1
                writer.writerow(["", "", "", ""])  # initial data row

            popup.destroy()
            self.refresh_test_list()

        popup.bind("<Return>", lambda event: create())
        ttk.Button(popup, text="Create Test", command=create).pack(pady=10)


if __name__ == "__main__":
    app = ReportBuilder()
    app.mainloop()

