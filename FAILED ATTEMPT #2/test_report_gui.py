import tkinter as tk
from tkinter import ttk, messagebox
import json

report_data = {
    "cover": {
        "model_number": "",
        "model_name": "",
        "specifications": [],
        "tested_by": {
            "name": "",
            "start_date": "",
            "end_date": ""
        },
        "reviewed_by": {
            "name": "",
            "start_date": "",
            "end_date": ""
        }
    },
    "tests": {
        "input": [],
        "output": [],
        "protections": [],
        "safety": [],
        "emc": []
    }
}

class ReportBuilder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Engineering Test Report Builder")
        
        icon_image = tk.PhotoImage(file="globtek_logo_large.png")
        self.iconphoto(True, icon_image)

        self.geometry("900x700")
        self.selected_test_index = None
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # ======== COVER TAB =========
        cover_tab = ttk.Frame(notebook)
        notebook.add(cover_tab, text="Cover Page")

        info_frame = ttk.LabelFrame(cover_tab, text="Model Info", padding=10)
        info_frame.pack(fill="x", padx=10, pady=5)

        self.cover_entries = {}

        self._add_labeled_entry(info_frame, "Model Number", "model_number", 0)
        self._add_labeled_entry(info_frame, "Model Name", "model_name", 1)

        tested_frame = ttk.LabelFrame(cover_tab, text="Tested By", padding=10)
        tested_frame.pack(fill="x", padx=10, pady=5)

        self._add_labeled_entry(tested_frame, "Name", "tested_by_name", 0)
        self._add_labeled_entry(tested_frame, "Start Date", "test_start", 1)
        self._add_labeled_entry(tested_frame, "End Date", "test_end", 2)

        reviewed_frame = ttk.LabelFrame(cover_tab, text="Reviewed By", padding=10)
        reviewed_frame.pack(fill="x", padx=10, pady=5)

        self._add_labeled_entry(reviewed_frame, "Name", "reviewed_by_name", 0)
        self._add_labeled_entry(reviewed_frame, "Start Date", "review_start", 1)
        self._add_labeled_entry(reviewed_frame, "End Date", "review_end", 2)

        # ======== TESTS TAB =========
        tests_tab = ttk.Frame(notebook)
        notebook.add(tests_tab, text="Tests")

        input_frame = ttk.Frame(tests_tab)
        input_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(input_frame, text="Category:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(input_frame, textvariable=self.category_var, width=15)
        self.category_menu['values'] = list(report_data["tests"].keys())
        self.category_menu.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        ttk.Label(input_frame, text="Test Name:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.test_name = tk.Entry(input_frame, width=50)
        self.test_name.grid(row=1, column=1, columnspan=3, padx=5, pady=2)

        # Specifications
        specs_frame = ttk.LabelFrame(tests_tab, text="Specification", padding=10)
        specs_frame.pack(fill="x", padx=10, pady=5)

        self.spec_type = self._create_entry_with_label(specs_frame, "Type", 0, 0)
        self.spec_val = self._create_entry_with_label(specs_frame, "Value", 0, 1)
        self.spec_unit = self._create_entry_with_label(specs_frame, "Unit", 0, 2)
        self.spec_note = self._create_entry_with_label(specs_frame, "Notes", 0, 3)

        # Conditions
        conds_frame = ttk.LabelFrame(tests_tab, text="Conditions", padding=10)
        conds_frame.pack(fill="x", padx=10, pady=5)

        self.cond_type = self._create_entry_with_label(conds_frame, "Type", 0, 0)
        self.cond_val = self._create_entry_with_label(conds_frame, "Value", 0, 1)
        self.cond_unit = self._create_entry_with_label(conds_frame, "Unit", 0, 2)
        self.cond_note = self._create_entry_with_label(conds_frame, "Notes", 0, 3)

        # Notes
        ttk.Label(tests_tab, text="General Notes:").pack(anchor="w", padx=15, pady=(10, 2))
        self.general_notes = tk.Entry(tests_tab, width=100)
        self.general_notes.pack(fill="x", padx=15)

        # Buttons
        btn_frame = ttk.Frame(tests_tab)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Add", command=self.add_test).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_test).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Delete", command=self.delete_test).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear_fields).grid(row=0, column=3, padx=5)

        # Test list with scrollbar
        list_frame = ttk.LabelFrame(tests_tab, text="Current Tests", padding=5)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.test_listbox = tk.Listbox(list_frame, width=100, height=10)
        self.test_listbox.pack(side="left", fill="both", expand=True)
        self.test_listbox.bind("<<ListboxSelect>>", self.load_selected_test)

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.test_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.test_listbox.config(yscrollcommand=scrollbar.set)

        # Save button
        ttk.Button(self, text="💾 Save JSON File", command=self.save_json).pack(pady=10)

    def _add_labeled_entry(self, parent, label, key, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="e", padx=5, pady=2)
        entry = tk.Entry(parent, width=40)
        entry.grid(row=row, column=1, sticky="w", pady=2)
        self.cover_entries[key] = entry

    def _create_entry_with_label(self, parent, label, row, col):
        ttk.Label(parent, text=label).grid(row=row, column=col * 2, sticky="w", padx=5)
        entry = tk.Entry(parent, width=20)
        entry.grid(row=row, column=col * 2 + 1, padx=5)
        return entry

    def get_test_data(self):
        return {
            "name": self.test_name.get(),
            "specifications": [{
                "type": self.spec_type.get(),
                "values": [self.spec_val.get()],
                "unit": self.spec_unit.get(),
                "notes": self.spec_note.get()
            }],
            "conditions": [{
                "type": self.cond_type.get(),
                "values": [self.cond_val.get()],
                "unit": self.cond_unit.get(),
                "notes": self.cond_note.get()
            }],
            "results": [],
            "notes": self.general_notes.get()
        }

    def add_test(self):
        category = self.category_var.get()
        if not category:
            messagebox.showerror("Error", "Select a test category.")
            return
        report_data["tests"][category].append(self.get_test_data())
        self.refresh_listbox(category)
        self.clear_fields()

    def update_test(self):
        category = self.category_var.get()
        if self.selected_test_index is not None:
            report_data["tests"][category][self.selected_test_index] = self.get_test_data()
            self.refresh_listbox(category)
            self.clear_fields()

    def delete_test(self):
        category = self.category_var.get()
        if self.selected_test_index is not None:
            del report_data["tests"][category][self.selected_test_index]
            self.refresh_listbox(category)
            self.clear_fields()

    def clear_fields(self):
        self.test_name.delete(0, tk.END)
        self.spec_type.delete(0, tk.END)
        self.spec_val.delete(0, tk.END)
        self.spec_unit.delete(0, tk.END)
        self.spec_note.delete(0, tk.END)
        self.cond_type.delete(0, tk.END)
        self.cond_val.delete(0, tk.END)
        self.cond_unit.delete(0, tk.END)
        self.cond_note.delete(0, tk.END)
        self.general_notes.delete(0, tk.END)
        self.selected_test_index = None
        self.test_listbox.selection_clear(0, tk.END)

    def refresh_listbox(self, category):
        self.test_listbox.delete(0, tk.END)
        for test in report_data["tests"][category]:
            self.test_listbox.insert(tk.END, test["name"])

    def load_selected_test(self, event):
        category = self.category_var.get()
        if not category:
            return
        index = self.test_listbox.curselection()
        if index:
            self.selected_test_index = index[0]
            test = report_data["tests"][category][self.selected_test_index]
            self.test_name.delete(0, tk.END)
            self.test_name.insert(0, test["name"])
            spec = test["specifications"][0]
            self.spec_type.delete(0, tk.END)
            self.spec_type.insert(0, spec["type"])
            self.spec_val.delete(0, tk.END)
            self.spec_val.insert(0, spec["values"][0])
            self.spec_unit.delete(0, tk.END)
            self.spec_unit.insert(0, spec["unit"])
            self.spec_note.delete(0, tk.END)
            self.spec_note.insert(0, spec["notes"])
            cond = test["conditions"][0]
            self.cond_type.delete(0, tk.END)
            self.cond_type.insert(0, cond["type"])
            self.cond_val.delete(0, tk.END)
            self.cond_val.insert(0, cond["values"][0])
            self.cond_unit.delete(0, tk.END)
            self.cond_unit.insert(0, cond["unit"])
            self.cond_note.delete(0, tk.END)
            self.cond_note.insert(0, cond["notes"])
            self.general_notes.delete(0, tk.END)
            self.general_notes.insert(0, test["notes"])

    def save_json(self):
        c = self.cover_entries
        report_data["cover"]["model_number"] = c["model_number"].get()
        report_data["cover"]["model_name"] = c["model_name"].get()
        report_data["cover"]["tested_by"]["name"] = c["tested_by_name"].get()
        report_data["cover"]["tested_by"]["start_date"] = c["test_start"].get()
        report_data["cover"]["tested_by"]["end_date"] = c["test_end"].get()
        report_data["cover"]["reviewed_by"]["name"] = c["reviewed_by_name"].get()
        report_data["cover"]["reviewed_by"]["start_date"] = c["review_start"].get()
        report_data["cover"]["reviewed_by"]["end_date"] = c["review_end"].get()

        with open("test_report.json", "w") as f:
            json.dump(report_data, f, indent=2)

        messagebox.showinfo("Success", "Saved to test_report.json")


if __name__ == "__main__":
    app = ReportBuilder()
    app.mainloop()
