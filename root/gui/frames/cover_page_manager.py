import tkinter as tk
from tkinter import ttk


from model.test_report import TestReport


class CoverPageManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.report = None

        title_bar = ttk.Frame(self, relief='solid')
        title_bar.pack(side=tk.TOP, fill='x')
        title = ttk.Label(title_bar, text="Cover Page Manager")
        title.pack(pady=5, padx=5, anchor='w')

        


    def add_


    def set_report(self, report: TestReport):
        self.report = report
        self.refresh_ui()

    def refresh_ui(self):

        tk.Label(self, text='THIS IS A LABEL!').pack()