import tkinter as tk
from tksheet import Sheet


class Demo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("tksheet Edit Validation Example")
        self.geometry("600x400")

        # Frame to contain the Sheet
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)

        # Initialize Sheet with sample data
        self.sheet = Sheet(
            frame,
            data=[[f"Row {r}, Col {c}" for c in range(3)] for r in range(5)],
            headers=["Col A", "Col B", "Col C"]
        )

        # enable bindings
        # pack sheet
        # set up bulk edit validation callback
        # make validate_bulk_edits function

        self.sheet.enable_bindings()
        self.sheet.pack(fill="both", expand=True)

        # Set up bulk edit validation callback
        self.sheet.bulk_table_edit_validation(self.validate_bulk_edits)

    def validate_bulk_edits(self, event: dict):
        """
        Called after user attempts any edit (typing, paste, cut, etc).
        Only changes left in event['data'] will be committed.
        """

        print("🔧 Validation triggered.")
        for (row, col), new_value in event["data"].items():
            old_value = self.sheet.get_cell_data(row, col)
            print(f"📌 Cell ({row}, {col}) changed: '{old_value}' ➜ '{new_value}'")

        # Example: block any edits that include "block"
        event["data"] = {
            k: v for k, v in event["data"].items()
            if "block" not in v
        }


if __name__ == "__main__":
    app = Demo()
    app.mainloop()
