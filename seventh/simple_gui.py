import tkinter as tk
from tksheet import Sheet
import pandas as pd

def edit_test(test):
    root = tk.Tk()
    root.title(f"Edit Test: {test.name}")

    df = test.root_table.copy()

    sheet = Sheet(root,
                  data=df.values.tolist(),
                  headers=list(df.columns),
                  show_x_scrollbar=True,
                  show_y_scrollbar=True,
                  width=900,
                  height=500)
    sheet.grid(row=0, column=0, sticky="nsew")

    # Enable all necessary bindings including editing
    sheet.enable_bindings((
        "single_select",
        "row_select",
        "column_select",
        "column_width_resize",
        "arrowkeys",
        "right_click_popup_menu",
        "rc_select",
        "copy",
        "cut",
        "paste",
        "delete",
        "undo",
        "edit_cell"
    ))

    # Lock only CC columns
    cc_cols = [test.metadata[k] for k in test.metadata if k.startswith('CC')]
    cc_indices = [df.columns.get_loc(col) for col in cc_cols]
    sheet.readonly_columns(cc_indices)

    def on_close():
        # Pull edited data back from the sheet
        edited_data = sheet.get_sheet_data(return_copy=True)
        new_df = pd.DataFrame(edited_data, columns=df.columns)

        # Update results dictionary (non-CC columns only)
        for col in new_df.columns:
            if col not in cc_cols and col in test.results:
                test.results[col] = new_df[col].tolist()

        # Update root_table
        test.root_table = new_df

        root.destroy()

    save_btn = tk.Button(root, text="Save and Close", command=on_close)
    save_btn.grid(row=1, column=0, pady=10)

    root.mainloop()
