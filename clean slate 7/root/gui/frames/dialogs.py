import tkinter as tk
from tkinter import ttk, messagebox

from pathlib import Path


class CCDialog(tk.Toplevel):
    def __init__(self, parent, on_submit, existing_name_var='', existing_values_var=''):
        super().__init__(parent)

        self.title("Add Column Condition")
        self.on_submit = on_submit

        # load logo.png from assets/
        logo_path = Path(__file__).parent.parent.parent / "assets" / "logo.png"
        logo_img = tk.PhotoImage(file=logo_path)
        # set it as window icon
        self.iconphoto(False, logo_img)
        self._icon_img = logo_img # prevent image from being garbage collected

        # self.existing_name_var = existing_name_var
        # self.existing_values_var = existing_values_var

        evv = ', '.join(existing_values_var)

        self.name_var = tk.StringVar()
        self.values_var = tk.StringVar()

        ttk.Label(self, text='Name *include units in parenthesis* :').pack(padx=10, pady=(10, 2))
        e1 = ttk.Entry(self, textvariable=self.name_var)
        e1.pack(padx=10)
        e1.insert(0, existing_name_var)

        ttk.Label(self, text="Values *comma separated* :").pack(padx=10, pady=(10, 2))
        e2 = ttk.Entry(self, textvariable=self.values_var)
        e2.pack(padx=10)
        e2.insert(0, evv)

        ttk.Button(self, text="Submit", command=self.submit).pack(pady=10)

        self.grab_set() # apart of tkinter toplevel events stuff

    def submit(self):
        name = self.name_var.get().strip()
        values_raw = self.values_var.get().strip()

        if not name or not values_raw:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        
        values = [v.strip() for v in values_raw.split(',') if v.strip()]
        self.on_submit(name, values)
        print('SUBMIT HIT!')
        self.destroy()