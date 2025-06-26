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
        self.title("Test Report JSON Builder")
        self.geometry("700x600")
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # Cover Page Tab
        cover_tab = ttk.Frame(notebook)
        notebook.add(cover_tab, text="Cover Page")

        tk.Label(cover_tab, text="Model Number").grid(row=0, column=0, sticky="w")
        self.model_number = tk.Entry(cover_tab, width=40)
        self.model_number.grid(row=0, column=1)

        tk.Label(cover_tab, text="Model Name").grid(row=1, column=0, sticky="w")
        self.model_name = tk.Entry(cover_tab, width=40)
        self.model_name.grid(row=1, column=1)

        tk.Label(cover_tab, text="Tested By Name").grid(row=2, column=0, sticky="w")
        self.tested_by_name = tk.Entry(cover_tab, width=40)
        self.tested_by_name.grid(row=2, column=1)
        tk.Label(cover_tab, text="Test Start Date").grid(row=3, column=0, sticky="w")
        self.test_start = tk.Entry(cover_tab, width=40)
        self.test_start.grid(row=3, column=1)
        tk.Label(cover_tab, text="Test End Date").grid(row=4, column=0, sticky="w")
        self.test_end = tk.Entry(cover_tab, width=40)
        self.test_end.grid(row=4, column=1)

        tk.Label(cover_tab, text="Reviewed By Name").grid(row=5, column=0, sticky="w")
        self.reviewed_by_name = tk.Entry(cover_tab, width=40)
        self.reviewed_by_name.grid(row=5, column=1)
        tk.Label(cover_tab, text="Review Start Date").grid(row=6, column=0, sticky="w")
        self.review_start = tk.Entry(cover_tab, width=40)
        self.review_start.grid(row=6, column=1)
        tk.Label(cover_tab, text="Review End Date").grid(row=7, column=0, sticky="w")
        self.review_end = tk.Entry(cover_tab, width=40)
        self.review_end.grid(row=7, column=1)

        # Tests Tab
        tests_tab = ttk.Frame(notebook)
        notebook.add(tests_tab, text="Add Test")

        self.test_category = tk.StringVar()
        tk.Label(tests_tab, text="Category").grid(row=0, column=0, sticky="w")
        category_menu = ttk.Combobox(tests_tab, textvariable=self.test_category, values=["input", "output", "protections", "safety", "emc"])
        category_menu.grid(row=0, column=1)

        tk.Label(tests_tab, text="Test Name").grid(row=1, column=0, sticky="w")
        self.test_name = tk.Entry(tests_tab, width=40)
        self.test_name.grid(row=1, column=1)

        # Specifications
        self.spec_type = tk.Entry(tests_tab, width=15)
        self.spec_val = tk.Entry(tests_tab, width=15)
        self.spec_unit = tk.Entry(tests_tab, width=10)
        self.spec_note = tk.Entry(tests_tab, width=25)
        tk.Label(tests_tab, text="Spec Type").grid(row=2, column=0)
        self.spec_type.grid(row=2, column=1)
        tk.Label(tests_tab, text="Value").grid(row=2, column=2)
        self.spec_val.grid(row=2, column=3)
        tk.Label(tests_tab, text="Unit").grid(row=2, column=4)
        self.spec_unit.grid(row=2, column=5)
        tk.Label(tests_tab, text="Notes").grid(row=2, column=6)
        self.spec_note.grid(row=2, column=7)

        # Conditions
        self.cond_type = tk.Entry(tests_tab, width=15)
        self.cond_val = tk.Entry(tests_tab, width=15)
        self.cond_unit = tk.Entry(tests_tab, width=10)
        self.cond_note = tk.Entry(tests_tab, width=25)
        tk.Label(tests_tab, text="Cond Type").grid(row=3, column=0)
        self.cond_type.grid(row=3, column=1)
        tk.Label(tests_tab, text="Value").grid(row=3, column=2)
        self.cond_val.grid(row=3, column=3)
        tk.Label(tests_tab, text="Unit").grid(row=3, column=4)
        self.cond_unit.grid(row=3, column=5)
        tk.Label(tests_tab, text="Notes").grid(row=3, column=6)
        self.cond_note.grid(row=3, column=7)

        # Notes
        tk.Label(tests_tab, text="General Notes").grid(row=4, column=0, sticky="w")
        self.general_notes = tk.Entry(tests_tab, width=50)
        self.general_notes.grid(row=4, column=1, columnspan=4)

        tk.Button(tests_tab, text="Add Test Entry", command=self.add_test).grid(row=5, column=0, columnspan=2, pady=10)

        # Save button
        tk.Button(self, text="Save JSON to File", command=self.save_json).pack(pady=10)

    def add_test(self):
        category = self.test_category.get()
        if category not in report_data["tests"]:
            messagebox.showerror("Error", "Invalid category selected.")
            return

        test_entry = {
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

        report_data["tests"][category].append(test_entry)
        messagebox.showinfo("Added", f"Test added to category '{category}'.")

    def save_json(self):
        report_data["cover"]["model_number"] = self.model_number.get()
        report_data["cover"]["model_name"] = self.model_name.get()
        report_data["cover"]["tested_by"] = {
            "name": self.tested_by_name.get(),
            "start_date": self.test_start.get(),
            "end_date": self.test_end.get()
        }
        report_data["cover"]["reviewed_by"] = {
            "name": self.reviewed_by_name.get(),
            "start_date": self.review_start.get(),
            "end_date": self.review_end.get()
        }

        with open("test_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        messagebox.showinfo("Saved", "test_report.json saved successfully.")

if __name__ == "__main__":
    app = ReportBuilder()
    app.mainloop()
