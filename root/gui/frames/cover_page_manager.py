import tkinter as tk
from tkinter import ttk


from model.test_report import TestReport


class CoverPageManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        print("COVER PAGE MANAGER CONSTRUCTED")
        self.report = None

        ttk.Label(self, text="THIS IS THE COVER PAGE MANAGER!").pack()
        

    
    def set_report(self, report: TestReport):
        self.report = report
        self.refresh_ui()

    def refresh_ui(self):

        tk.Label(self, text='THIS IS A LABEL!').pack()