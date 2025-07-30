import tkinter as tk
from tkinter import ttk
import tksheet
import pandas as pd

from model.test_report import TestReport


class ImageViewer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        ttk.Label(self, text='IMAGE VIEWER CONSTRUCTED').pack()
        self.info_label = ttk.Label(self, text='Click a cell to view info')
        self.info_label.pack()

        self.report = None

        toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
        toolbar.pack(side=tk.TOP)

        add_image_button = ttk.Button(toolbar, text='ADD', command=self.add_image).pack(side=tk.RIGHT)
        replace_image_button = ttk.Button(toolbar, text='REPLACE', command=self.replace_image).pack(side=tk.RIGHT)
        remove_image_button = ttk.Button(toolbar, text='DEL', command=self.remove_image).pack(side=tk.RIGHT)
        expand_image_button = ttk.Button(toolbar, text='SAVE', command=self.expand_image).pack(side=tk.RIGHT)
        

    def add_image(self):
        pass

    def replace_image(self):
        pass

    def remove_image(self):
        pass

    def expand_image(self):
        pass

    def set_report(self, report: TestReport):
        self.report = report


    def update_cell_info(self, row, col, col_name, value):
        self.info_label.config(
            text=f"Row: {row}, Col: {col} ({col_name})\nValue: {value}"
        )
