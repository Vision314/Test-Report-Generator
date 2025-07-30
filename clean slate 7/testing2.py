from tksheet import (
    Sheet,
    num2alpha,
)
import tkinter as tk


class demo(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(0, weight = 1)
        self.sheet = Sheet(self.frame,
                           data = [[f"Row {r}, Column {c}\nnewline1\nnewline2" for c in range(50)] for r in range(500)])
        self.sheet.enable_bindings("all", "ctrl_select")
        self.sheet.extra_bindings([("all_select_events", self.sheet_select_event)])
        self.show_selections = tk.Label(self)
        self.frame.grid(row = 0, column = 0, sticky = "nswe")
        self.sheet.grid(row = 0, column = 0, sticky = "nswe")
        self.show_selections.grid(row = 1, column = 0, sticky = "nsw")

        # make sheet
        # enable bindings
        # set extra binding: self.sheet.extra_bindings([("all_select_events", self.sheet_select_event)])
        # 

    def sheet_select_event(self, event = None):
        if event.eventname == "select" and event.selection_boxes and event.selected:
            # get the most recently selected box in case there are multiple
            box = next(reversed(event.selection_boxes))
            type_ = event.selection_boxes[box]
            if type_ == "cells":
                self.show_selections.config(text=f"{type_.capitalize()}: {box.from_r + 1},{box.from_c + 1} : {box.upto_r},{box.upto_c}")
            elif type_ == "rows":
                self.show_selections.config(text=f"{type_.capitalize()}: {box.from_r + 1} : {box.upto_r}")
            elif type_ == "columns":
                self.show_selections.config(text=f"{type_.capitalize()}: {num2alpha(box.from_c)} : {num2alpha(box.upto_c - 1)}")
        else:
            self.show_selections.config(text="")


app = demo()
app.mainloop()