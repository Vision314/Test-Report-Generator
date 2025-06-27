import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd


class TableEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Custom Table to LaTeX Generator")
        self.geometry("800x600")

        self.entries = []  # Will hold the Entry widgets for table cells

        # Controls to define table size
        control_frame = ttk.Frame(self)
        control_frame.pack(pady=10)

        ttk.Label(control_frame, text="Rows:").grid(row=0, column=0)
        self.rows_var = tk.IntVar(value=5)
        ttk.Entry(control_frame, textvariable=self.rows_var, width=5).grid(row=0, column=1)

        ttk.Label(control_frame, text="Columns:").grid(row=0, column=2)
        self.cols_var = tk.IntVar(value=5)
        ttk.Entry(control_frame, textvariable=self.cols_var, width=5).grid(row=0, column=3)

        ttk.Button(control_frame, text="Generate Table", command=self.generate_table).grid(row=0, column=4, padx=10)
        ttk.Button(control_frame, text="Export to LaTeX", command=self.export_latex).grid(row=0, column=5)

        # Frame to hold the editable table
        self.table_frame = ttk.Frame(self)
        self.table_frame.pack(pady=20)

        # Output text area
        self.output_box = tk.Text(self, height=10)
        self.output_box.pack(padx=10, pady=10, fill="both", expand=True)

    def generate_table(self):
        # Clear previous table
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        self.entries = []

        rows = self.rows_var.get()
        cols = self.cols_var.get()

        for i in range(rows):
            row_entries = []
            for j in range(cols):
                entry = tk.Entry(self.table_frame, width=15)
                entry.grid(row=i, column=j, padx=1, pady=1)
                row_entries.append(entry)
            self.entries.append(row_entries)

    def export_latex(self):
        if not self.entries:
            messagebox.showwarning("No Table", "Please generate a table first.")
            return

        # Collect the data
        data = []
        for row in self.entries:
            data.append([cell.get() for cell in row])

        num_cols = len(data[0])
        col_format = 'c' * num_cols  # All columns centered
        lines = []

        lines.append("\\begin{center}")
        lines.append(f"\\begin{{tabular}}{{{col_format}}}")
        lines.append("\\toprule")

        for i, row in enumerate(data):
            processed_row = []
            for col_index, cell in enumerate(row):
                text = cell.strip()

                # Highlight Result column (last column)
                if i > 0 and col_index == num_cols - 1:
                    if text.upper() == "PASS":
                        text = "\\textcolor{green}{PASS}"
                    elif text.upper() == "FAIL":
                        text = "\\textcolor{red}{FAIL}"
                elif text == "":
                    # Add blank fillable box for empty cells
                    text = "\\framebox[2cm][c]{\\rule{0pt}{1.5ex}}"

                processed_row.append(text)

            line = " & ".join(processed_row) + " \\\\"

            if i == 0:
                lines.append(line)
                lines.append("\\midrule")
            else:
                lines.append(line)

        lines.append("\\bottomrule")
        lines.append("\\end{tabular}")
        lines.append("\\end{center}")

        latex_code = "\n".join(lines)
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, latex_code)




if __name__ == "__main__":
    app = TableEditor()
    app.mainloop()
