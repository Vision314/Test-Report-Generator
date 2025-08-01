import tkinter as tk
from tkinter import ttk
import pandas as pd

from model.test_report import TestReport


class EquipmentManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.report = None  # This is a TestReport object
        # self.equipment_used = self.report.cover_page.equipment_used
        # self.checkbox_vars = []
        self.equipment_used = None
        self.checkbox_vars = []

        # Header area (like a group label)
        self.header = ttk.Label(
            self, 
            text="🛠 Equipment Manager", 
            anchor="w",
            font=("Segoe UI", 10, "bold"),
            background="#e0e0e0",
            relief="raised"
        )
        self.header.pack(fill=tk.X)

        self.configure(bg="#f0f0f0", padx=5, pady=5)

        # Canvas and Scrollbar
        self.canvas = tk.Canvas(self, borderwidth=0, background="#f0f0f0")
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = ttk.Frame(self.canvas, style="EquipList.TFrame")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set, background="#f0f0f0")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        add_button = ttk.Button(self.header, text="➕ Add Equipment", command=self.add_equipment_dialog)
        add_button.pack(anchor="e", pady=(0, 5))

        # self.build_equipment_list()

    def set_report(self, report: TestReport):
        self.report = report
        self.build_equipment_list()
        self.refresh_ui()

    def add_equipment_dialog(self):
        editor = tk.Toplevel(self)
        editor.title("Add Equipment")
        editor.grab_set()

        entries = {}
        fields = ['Equipment Type', 'Manufacturer', 'Model', 'Description', 'S/N', 'Last Calibrated', 'Calibration Due']

        for i, field in enumerate(fields):
            tk.Label(editor, text=field).grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(editor, width=40)
            entry.grid(row=i, column=1, padx=5, pady=2)
            entries[field] = entry

        def save():
            values = [entries[field].get() for field in fields]
            new_row = pd.DataFrame([values], columns=fields)
            self.report.cover_page.equipment_used = pd.concat([self.report.cover_page.equipment_used, new_row], ignore_index=True)
            editor.destroy()
            self.refresh_ui()

        ttk.Button(editor, text="Add", command=save).grid(row=len(fields), column=0, columnspan=2, pady=10)

    def build_equipment_list(self):
        header_font = ("Segoe UI", 9, "bold")
        cell_font = ("Segoe UI", 9)
        bg_even = "#ffffff"
        bg_odd = "#f7f7f7"

        headers = ["✓", "Type", "Manufacturer", "Model", "Description", "S/N", "Last Cal.", "Due"]
        for col, text in enumerate(headers):
            label = tk.Label(self.scroll_frame, text=text, font=header_font, bg="#e0e0e0", padx=6, pady=4, borderwidth=1, relief="groove")
            label.grid(row=0, column=col, sticky="nsew")

        selected_indexes = self.report.selected_test.checkbox_vars if self.report.selected_test else []

        for row_index, row in self.report.cover_page.equipment_used.iterrows():
            var = tk.BooleanVar(value=(row_index in selected_indexes))
            self.checkbox_vars.append(var)

            bg_color = bg_even if row_index % 2 == 0 else bg_odd

            cb = tk.Checkbutton(self.scroll_frame, variable=var, command=lambda i=row_index, v=var: self.checkbox_toggled(i, v), bg=bg_color)
            cb.grid(row=row_index + 1, column=0, sticky='w', padx=4)

            fields = [
                row['Equipment Type'],
                row['Manufacturer'],
                row['Model'],
                row['Description'],
                row['S/N'],
                row['Last Calibrated'],
                row['Calibration Due']
            ]

            for col, val in enumerate(fields, start=1):
                label = tk.Label(self.scroll_frame, text=val, font=cell_font, anchor="w", bg=bg_color, padx=6, pady=2)
                label.grid(row=row_index + 1, column=col, sticky="nsew")
                label.bind("<Double-1>", lambda e, i=row_index: self.edit_equipment_dialog(i))

        for i in range(len(headers)):
            self.scroll_frame.grid_columnconfigure(i, weight=1)

    def checkbox_toggled(self, index, var):
        if not self.report.selected_test:
            return

        if var.get():
            if index not in self.report.selected_test.checkbox_vars:
                self.report.selected_test.checkbox_vars.append(index)
                print(f"[+] Selected equipment index {index}")
        else:
            if index in self.report.selected_test.checkbox_vars:
                self.report.selected_test.checkbox_vars.remove(index)
                print(f"[-] Deselected equipment index {index}")

    def edit_equipment_dialog(self, index):
        row_data = self.equipment_used.iloc[index]
        editor = tk.Toplevel(self)
        editor.title("Edit Equipment")
        editor.grab_set()

        entries = {}
        fields = ['Equipment Type', 'Manufacturer', 'Model', 'Description', 'S/N', 'Last Calibrated', 'Calibration Due']

        for i, field in enumerate(fields):
            tk.Label(editor, text=field).grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(editor, width=40)
            entry.insert(0, str(row_data[field]))
            entry.grid(row=i, column=1, padx=5, pady=2)
            entries[field] = entry

        def save():
            for field in fields:
                self.equipment_used.at[index, field] = entries[field].get()
            editor.destroy()
            self.refresh_ui()

        def delete():
            self.equipment_used.drop(self.equipment_used.index[index], inplace=True)
            self.equipment_used.reset_index(drop=True, inplace=True)
            # Clean checkbox_vars for all tests
            for test in self.report.tests:
                test.checkbox_vars = [i if i < index else i - 1 for i in test.checkbox_vars if i != index]
            editor.destroy()
            self.refresh_ui()

        ttk.Button(editor, text="Save", command=save).grid(row=len(fields), column=0, pady=10)
        ttk.Button(editor, text="Delete", command=delete).grid(row=len(fields), column=1, pady=10)

    def refresh_ui(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        self.checkbox_vars.clear()
        self.equipment_used = self.report.cover_page.equipment_used  # Refresh pointer
        self.build_equipment_list()
