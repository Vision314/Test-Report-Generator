import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
import pandas as pd

# Utility to format display names from folder names
def format_display_name(name):
    return name.replace("_", " ").title()

class TestReportApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Report Builder")
        self.geometry("1200x700")

        self.report_path = None
        self.selected_test_path = None
        self.selected_item = None

        self.create_menu()
        self.create_layout()

    def create_menu(self):
        menubar = tk.Menu(self)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Report", command=self.new_report)
        file_menu.add_command(label="Open Report", command=self.open_report)
        file_menu.add_command(label="Save", command=self.save_current_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.config(menu=menubar)



    def create_layout(self):
        # Create paned window as the main container
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        # Left frame for treeview and header
        self.left_frame = tk.Frame(self.paned_window, width=250)  # you can adjust default width
        self.paned_window.add(self.left_frame, minsize=150)  # minsize prevents collapsing too small

        # Header in left frame
        header_frame = tk.Frame(self.left_frame)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="Tests", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Button(header_frame, text="+", command=self.create_new_test).pack(side=tk.RIGHT, padx=5)

        # Treeview in left frame, fills remaining space
        self.tree = ttk.Treeview(self.left_frame)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_test_select)

        # Right frame for test content
        self.right_frame = tk.Frame(self.paned_window)
        self.paned_window.add(self.right_frame, minsize=400)

        # Content inside right frame
        self.test_label = tk.Label(self.right_frame, text="", font=("Arial", 14, "bold"))
        self.test_label.pack(pady=10)

        self.table_frame = tk.Frame(self.right_frame)
        self.table_frame.pack(pady=5)

        self.cell_entries = []



    def new_report(self):
        path = filedialog.askdirectory(title="Select Directory for New Report")
        if path:
            self.report_path = path
            self.refresh_tree()

    def open_report(self):
        path = filedialog.askdirectory(title="Select Existing Report Directory")
        if path:
            self.report_path = path
            self.refresh_tree()

    def refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        if not self.report_path:
            return

        for category in sorted(os.listdir(self.report_path)):
            category_path = os.path.join(self.report_path, category)
            if os.path.isdir(category_path):
                cat_node = self.tree.insert("", "end", text=format_display_name(category), open=True)
                for test in sorted(os.listdir(category_path)):
                    test_path = os.path.join(category_path, test)
                    if os.path.isdir(test_path):
                        self.tree.insert(cat_node, "end", text="    " + format_display_name(test),
                                         values=[os.path.join(category_path, test)])

    def on_test_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        item = self.tree.item(selected[0])
        path = self.tree.item(selected[0], "values")
        if not path:
            return

        self.selected_test_path = path[0]
        self.selected_item = selected[0]
        self.load_csv()

    def load_csv(self):
        self.save_current_csv()  # Save previous

        self.clear_table()

        csv_path = os.path.join(self.selected_test_path, "csv", "data.csv")
        if not os.path.exists(csv_path):
            return

        df = pd.read_csv(csv_path, header=None)
        category = os.path.basename(os.path.dirname(self.selected_test_path))
        test = os.path.basename(self.selected_test_path)
        self.test_label.config(text=f"{format_display_name(category)} – {format_display_name(test)}")

        for r, row in df.iterrows():
            row_entries = []
            for c, val in enumerate(row):
                entry = tk.Entry(self.table_frame, width=20)
                entry.grid(row=r, column=c, padx=2, pady=2)
                if pd.notna(val):
                    entry.insert(0, str(val))
                row_entries.append(entry)
            self.cell_entries.append(row_entries)

    def save_current_csv(self):
        if not self.selected_test_path or not self.cell_entries:
            return

        data = []
        for row in self.cell_entries:
            data.append([entry.get().strip() for entry in row])

        df = pd.DataFrame(data)
        csv_path = os.path.join(self.selected_test_path, "csv", "data.csv")
        df.to_csv(csv_path, index=False, header=False)

    def clear_table(self):
        for row in self.cell_entries:
            for entry in row:
                entry.destroy()
        self.cell_entries = []

    def create_new_test(self):
        def submit():
            category = category_entry.get().strip().lower().replace(" ", "_")
            test = test_entry.get().strip().lower().replace(" ", "_")
            if not category or not test:
                return

            test_path = os.path.join(self.report_path, category, test)
            os.makedirs(os.path.join(test_path, "csv"), exist_ok=True)
            os.makedirs(os.path.join(test_path, "images"), exist_ok=True)
            os.makedirs(os.path.join(test_path, "latex"), exist_ok=True)

            df = pd.DataFrame([
                [category, test],
                ["", ""],
                ["", ""]
            ])
            df.to_csv(os.path.join(test_path, "csv", "data.csv"), index=False, header=False)

            popup.destroy()
            self.refresh_tree()

        popup = tk.Toplevel(self)
        popup.title("New Test")
        popup.geometry("+{}+{}".format(self.winfo_rootx() + 200, self.winfo_rooty() + 200))
        popup.grab_set()

        tk.Label(popup, text="Category:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        category_entry = tk.Entry(popup)
        category_entry.grid(row=0, column=1, padx=10, pady=5)
        category_entry.focus()

        tk.Label(popup, text="Test Name:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        test_entry = tk.Entry(popup)
        test_entry.grid(row=1, column=1, padx=10, pady=5)

        submit_btn = tk.Button(popup, text="Create", command=submit)
        submit_btn.grid(row=2, column=0, columnspan=2, pady=10)

        popup.bind("<Return>", lambda event: submit())

if __name__ == "__main__":
    app = TestReportApp()
    app.mainloop()
