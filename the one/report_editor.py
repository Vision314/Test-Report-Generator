import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import pandas as pd

class TestReportApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Report Builder")
        self.geometry("1100x600")

        self.report_path = None
        self.current_test_path = None
        self.current_df = None

        self.setup_menu()
        self.setup_layout()

    def setup_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Report", command=self.new_report)
        file_menu.add_command(label="Open Report", command=self.open_report)
        file_menu.add_command(label="Save", command=self.save_csv)
        file_menu.add_command(label="Save As", command=self.save_csv_as)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)

    def setup_layout(self):
        self.left_frame = tk.Frame(self, width=250)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.test_listbox = tk.Listbox(self.left_frame)
        self.test_listbox.pack(fill=tk.BOTH, expand=True)
        self.test_listbox.bind('<<ListboxSelect>>', self.load_selected_test)

        self.new_test_btn = tk.Button(self.left_frame, text="New Test", command=self.new_test_popup)
        self.new_test_btn.pack(pady=5)

        # Buttons to manage table structure
        tk.Button(self.left_frame, text="Add Row", command=self.add_row).pack(pady=2)
        tk.Button(self.left_frame, text="Add Column", command=self.add_column).pack(pady=2)
        tk.Button(self.left_frame, text="Delete Last Row", command=self.delete_row).pack(pady=2)
        tk.Button(self.left_frame, text="Delete Last Column", command=self.delete_column).pack(pady=2)

        self.right_frame = tk.Frame(self)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.table_frame = tk.Frame(self.right_frame)
        self.table_frame.pack(fill=tk.BOTH, expand=True)

    def new_report(self):
        path = filedialog.askdirectory(title="Select Directory for New Report")
        if path:
            self.report_path = path
            self.refresh_test_list()

    def open_report(self):
        path = filedialog.askdirectory(title="Open Report Directory")
        if path:
            self.report_path = path
            self.refresh_test_list()

    def refresh_test_list(self):
        self.test_listbox.delete(0, tk.END)
        if not self.report_path:
            return
        for folder in os.listdir(self.report_path):
            test_dir = os.path.join(self.report_path, folder)
            if os.path.isdir(test_dir):
                csv_path = os.path.join(test_dir, "csv", "data.csv")
                if os.path.exists(csv_path):
                    try:
                        df = pd.read_csv(csv_path, dtype=str).fillna("")
                        display_name = df.columns[1] if df.shape[1] > 1 else folder
                        self.test_listbox.insert(tk.END, f"{folder} - {display_name}")
                    except Exception:
                        self.test_listbox.insert(tk.END, folder)

    def new_test_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Create New Test")
        popup.geometry("300x150")
        popup.transient(self)
        popup.grab_set()
        popup.focus_force()

        tk.Label(popup, text="Category:").pack(pady=5)
        category_entry = tk.Entry(popup)
        category_entry.pack()

        tk.Label(popup, text="Display Name:").pack(pady=5)
        name_entry = tk.Entry(popup)
        name_entry.pack()

        def submit():
            category = category_entry.get().strip()
            display_name = name_entry.get().strip()
            if category and display_name:
                popup.destroy()
                self.create_new_test(category, display_name)

        tk.Button(popup, text="Create Test", command=submit).pack(pady=10)
        self.wait_window(popup)

    def create_new_test(self, category, display_name):
        if not self.report_path:
            messagebox.showerror("No Report", "Please create or open a report first.")
            return

        folder_name = display_name.replace(" ", "_")
        test_path = os.path.join(self.report_path, folder_name)
        os.makedirs(os.path.join(test_path, "csv"), exist_ok=True)
        os.makedirs(os.path.join(test_path, "images"), exist_ok=True)
        os.makedirs(os.path.join(test_path, "latex"), exist_ok=True)

        csv_path = os.path.join(test_path, "csv", "data.csv")
        df = pd.DataFrame([["", ""]], columns=[category, display_name])
        df.to_csv(csv_path, index=False)

        self.refresh_test_list()

    def load_selected_test(self, event=None):
        selection = self.test_listbox.curselection()
        if not selection:
            return
        test_label = self.test_listbox.get(selection[0])
        folder_name = test_label.split(" - ")[0]
        self.current_test_path = os.path.join(self.report_path, folder_name)
        csv_path = os.path.join(self.current_test_path, "csv", "data.csv")

        try:
            df = pd.read_csv(csv_path, dtype=str).fillna("")
            self.current_df = df
            self.display_table(df)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load CSV: {e}")

    def display_table(self, df):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        rows, cols = df.shape
        self.entries = []

        for r in range(rows):
            row_entries = []
            for c in range(cols):
                val = df.iat[r, c]
                entry = tk.Entry(self.table_frame, width=15)
                entry.insert(0, val)
                entry.grid(row=r, column=c, padx=1, pady=1)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def save_csv(self):
        if not self.current_test_path or not self.entries:
            return
        data = [[cell.get() for cell in row] for row in self.entries]
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(self.current_test_path, "csv", "data.csv"), index=False)

    def save_csv_as(self):
        if not self.entries:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            data = [[cell.get() for cell in row] for row in self.entries]
            df = pd.DataFrame(data)
            df.to_csv(file_path, index=False)

    def add_row(self):
        if not self.entries:
            return
        cols = len(self.entries[0])
        new_row = [tk.Entry(self.table_frame, width=15) for _ in range(cols)]
        for c, entry in enumerate(new_row):
            entry.grid(row=len(self.entries), column=c, padx=1, pady=1)
        self.entries.append(new_row)

    def delete_row(self):
        if self.entries:
            row = self.entries.pop()
            for cell in row:
                cell.destroy()

    def add_column(self):
        if not self.entries:
            return
        for r, row in enumerate(self.entries):
            entry = tk.Entry(self.table_frame, width=15)
            entry.grid(row=r, column=len(row), padx=1, pady=1)
            row.append(entry)

    def delete_column(self):
        if self.entries and self.entries[0]:
            for row in self.entries:
                cell = row.pop()
                cell.destroy()

if __name__ == "__main__":
    app = TestReportApp()
    app.mainloop()
