import tkinter as tk
from tkinter import ttk


from model.test_report import TestReport


class CoverPageManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.report = None

        # Header area (like a group label)
        header = ttk.Label(
            self, 
            text="📃 Cover Page Manager", 
            anchor="w",
            font=("Segoe UI", 10, "bold"),
            background="#e0e0e0",
            relief="raised"
        )
        header.pack(fill=tk.X)





    def add_spec(self):
        pass
    def rem_spec(self):
        pass


    def set_report(self, report: TestReport):
        self.report = report
        self.refresh_ui()

    def refresh_ui(self):

        tk.Label(self, text='THIS IS A LABEL!').pack()