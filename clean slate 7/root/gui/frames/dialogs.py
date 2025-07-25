import tkinter as tk
from tkinter import ttk, messagebox

from pathlib import Path


class CCDialog(tk.Toplevel):
    def __init__(self, parent, on_submit, col_tag, existing_name_var='', existing_values_var=''):
        super().__init__(parent)

        #------------------------------------
        # set stuff for window popup
        self.title("Add Column Condition")
        self.on_submit = on_submit
        self.col_tag = col_tag

        # load logo.png from assets/
        logo_path = Path(__file__).parent.parent.parent / "assets" / "logo.png"
        logo_img = tk.PhotoImage(file=logo_path)
        # set it as window icon
        self.iconphoto(False, logo_img)
        self._icon_img = logo_img # prevent image from being garbage collected

        # self.existing_name_var = existing_name_var
        # self.existing_values_var = existing_values_var

        # -------------------------------------------------

        # put the list of existing values into a string separated by values
        evv = ', '.join(existing_values_var)

        self.name_var = tk.StringVar()
        self.values_var = tk.StringVar()

        # create your labels and entries and insert the existing lames
        ttk.Label(self, text='Name *include units in parenthesis* :').pack(padx=10, pady=(10, 2))
        e1 = ttk.Entry(self, textvariable=self.name_var)
        e1.pack(padx=10)
        e1.insert(0, existing_name_var)

        ttk.Label(self, text="Values *comma separated* :").pack(padx=10, pady=(10, 2))
        e2 = ttk.Entry(self, textvariable=self.values_var)
        e2.pack(padx=10)
        e2.insert(0, evv)
        #--------------------------------------------
        # make your button
        ttk.Button(self, text="Submit", command=self.submit).pack(pady=10, padx=20, side=tk.RIGHT)

        # if you are editing then put the delete button in window
        if col_tag != '':
            ttk.Button(self, text='DELETE', command=self.delete).pack(pady=10, padx=20, side=tk.RIGHT)

        self.grab_set() # apart of tkinter toplevel events stuff

    def submit(self):
        name = self.name_var.get().strip()
        values_raw = self.values_var.get().strip()

        if not name or not values_raw:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        
        values = [v.strip() for v in values_raw.split(',') if v.strip()]
        
        if self.col_tag == '':
            self.on_submit(name, values)
        else:
            self.on_submit(self.col_tag, name, values)
        print('SUBMIT HIT!')
        self.destroy()

    def delete(self):
        pass



class ReDialog(tk.Toplevel):
    def __init__(self, parent, on_submit, col_tag, existing_name_var=''):
        super().__init__(parent)

        #------------------------------------
        # set stuff for window popup
        self.title("Add Resilt Column")
        self.on_submit = on_submit
        self.col_tag = col_tag

        # load logo.png from assets/
        logo_path = Path(__file__).parent.parent.parent / "assets" / "logo.png"
        logo_img = tk.PhotoImage(file=logo_path)
        # set it as window icon
        self.iconphoto(False, logo_img)
        self._icon_img = logo_img # prevent image from being garbage collected

        # -------------------------------------------------

        self.name_var = tk.StringVar()

        # create your labels and entries and insert the existing lames
        ttk.Label(self, text='Name *include units in parenthesis* :').pack(padx=10, pady=(10, 2))
        e1 = ttk.Entry(self, textvariable=self.name_var)
        e1.pack(padx=10)
        e1.insert(0, existing_name_var)

        #--------------------------------------------
        # make your button
        ttk.Button(self, text="Submit", command=self.submit).pack(pady=10, padx=20, side=tk.RIGHT)

        # if you are editing then put the delete button in window
        if col_tag != '':
            ttk.Button(self, text='DELETE', command=self.delete).pack(pady=10, padx=20, side=tk.RIGHT)

        self.grab_set() # apart of tkinter toplevel events stuff

    def submit(self):
        name = self.name_var.get().strip()

        if not name:
            messagebox.showerror("Input Error", "All fields are required.")
            return
                
        if self.col_tag == '':
            self.on_submit(name)
        else:
            self.on_submit(self.col_tag, name, '')

        self.destroy()