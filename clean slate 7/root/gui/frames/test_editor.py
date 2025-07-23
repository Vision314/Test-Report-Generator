import tkinter as tk
from tkinter import ttk


from model.test_report import TestReport



# column 1, row 0
class TestEditor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        print("TEST EDITOR CONSTRUCTED")
        tk.Label(self, text='THIS IS THE TEST EDITOR!').pack()

        self.report = None
        # self.refresh_ui()
    
    def set_report(self, report: TestReport):
        self.report = report
        self.refresh_ui()

    def refresh_ui(self):
        pass
