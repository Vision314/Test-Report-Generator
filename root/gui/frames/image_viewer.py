import tkinter as tk
from tkinter import ttk
import tksheet
import pandas as pd

from model.test_report import TestReport


class ImageViewer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Header area (like a group label)
        self.header = ttk.Label(
            self, 
            text="📷 Image Viewer", 
            anchor="w",
            font=("Segoe UI", 10, "bold"),
            background="#e0e0e0",
            relief="raised"
        )
        self.header.pack(fill=tk.X)

        self.report = None

        toolbar = ttk.Frame(self)
        toolbar.pack(side=tk.TOP, fill='x')
        toolbar.configure(style="Toolbar.TFrame")

        add_image_button = ttk.Button(toolbar, text='ADD', command=self.add_image).pack(side=tk.LEFT, pady=2, padx=2)
        replace_image_button = ttk.Button(toolbar, text='REPLACE', command=self.replace_image).pack(side=tk.LEFT, pady=2, padx=2)
        remove_image_button = ttk.Button(toolbar, text='DEL', command=self.remove_image).pack(side=tk.LEFT, pady=2, padx=2)
        expand_image_button = ttk.Button(toolbar, text='SAVE', command=self.expand_image).pack(side=tk.LEFT, pady=2, padx=2)
        
        ttk.Label(self, text='IMAGE VIEWER CONSTRUCTED').pack()
        self.info_label = ttk.Label(self, text='Click a cell to view info')
        self.info_label.pack()


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
