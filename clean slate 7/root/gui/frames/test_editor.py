import tkinter as tk
from tkinter import ttk
import tksheet
import pandas as pd

from tksheet import (
    Sheet,
    num2alpha,
)

from model.test_report import TestReport
from gui.frames.dialogs import CCDialog, ReDialog


# column 1, row 0
class TestEditor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        print("TEST EDITOR CONSTRUCTED")

        self.report = None


        toolbar = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        col_cond_button = ttk.Button(toolbar, text='CC', width=5, command=self.add_CC)
        col_cond_button.pack(side=tk.LEFT, padx=2, pady=2)

        res_button = ttk.Button(toolbar, text='Re', width=5, command=self.add_Re)
        res_button.pack(side=tk.LEFT, padx=2, pady=2)

        calc_button = ttk.Button(toolbar, text='Ca', width=5, command=self.add_Ca)
        calc_button.pack(side=tk.LEFT, padx=2, pady=2)

        spec_button = ttk.Button(toolbar, text='Sp', width=5, command=self.add_Sp)
        spec_button.pack(side=tk.LEFT, padx=2, pady=2)

        open_report_button = ttk.Button(toolbar, text='OPEN REPORT', width=20, command=self.master.menu.open_report)
        open_report_button.pack(side=tk.RIGHT)

        new_report_button = ttk.Button(toolbar, text='NEW REPORT', width=20, command=self.master.menu.new_report)
        new_report_button.pack(side=tk.RIGHT)


        
        self.test_name_label = ttk.Label(self, text="Please create or open a test report.")
        self.test_name_label.pack(side=tk.TOP, padx=5, pady=5)





        self.metadata_bar = ttk.Frame(self, relief=tk.RAISED, width=300, height=25)
        self.metadata_bar.pack(side=tk.TOP, pady=10)

        self.metadata_button_dict = {}

        

        self.sheet = tksheet.Sheet(self)
        
        


        self.sheet.enable_bindings()
        
        self.sheet.bulk_table_edit_validation(self.validate_bulk_edits)
        self.sheet.extra_bindings([("all_select_events", self.sheet_select_event)])

        
    def validate_bulk_edits(self, event: dict):
        """
        Called after user attempts any edit (typing, paste, cut, etc).
        Only changes left in event['data'] will be committed.
        """

        print("🔧 Validation triggered.")
        for (row, col), new_value in event["data"].items():
            old_value = self.sheet.get_cell_data(row, col)
            print(f"📌 Cell ({row}, {col}) changed: '{old_value}' ➜ '{new_value}'")

            name = self.report.get_root_table().columns[col]

            self.report.edit_Re_val(name, row, new_value)

        # Example: block any edits that include "block"
        event["data"] = {
            k: v for k, v in event["data"].items()
            if "block" not in v
        }

    def sheet_select_event(self, event = None):
        if event.eventname == "select" and event.selection_boxes and event.selected:
            # get the most recently selected box in case there are multiple
            box = next(reversed(event.selection_boxes))
            type_ = event.selection_boxes[box]
            if type_ == "cells":
                self.master.status_label.config(text=f"{type_.capitalize()}: {box.from_r + 1},{box.from_c + 1} : {box.upto_r},{box.upto_c}")
                r = box.from_r
                c = box.from_c



            elif type_ == "rows":
                self.master.status_label.config(text=f"{type_.capitalize()}: {box.from_r + 1} : {box.upto_r}")
            elif type_ == "columns":
                self.master.status_label.config(text=f"{type_.capitalize()}: {num2alpha(box.from_c)} : {num2alpha(box.upto_c - 1)}")
        else:
            self.master.status_label.config(text="")

    def add_CC(self):
        if not self.report or self.report.tests == []:
            return
        
        def on_submit(name, values):
            self.report.add_CC(name, values)
            self.refresh_ui()

        CCDialog(self, on_submit, 
                 col_tag='', 
                 existing_name_var='', 
                 existing_values_var='')

        print("HIT!")
        print(self.report.get_CC())
        print(self.report.get_metadata())


    def add_Re(self):
        if not self.report or self.report.tests == []:
            return
        
        def on_submit(name):
            self.report.add_Re(name)
            self.refresh_ui()

        ReDialog(self, on_submit, col_tag='')

        print("HIT!")
        print(self.report.get_CC())
        print(self.report.get_metadata())

    def add_Ca(self):
        pass

    def add_Sp(self):
        pass


    def edit_column(self, col_tag):
        print(col_tag)
        print(self.report.get_metadata()[col_tag])
        print("EDITING COLUMN")

        if 'CC' in col_tag:

            def on_submit(col_tag, new_name, new_values):
                self.report.edit_CC(col_tag, new_name, new_values)
                self.refresh_ui()

            def on_delete(col_tag):
                self.report.del_CC(col_tag)
                self.refresh_ui()

            name = self.report.get_metadata()[col_tag]
            values = self.report.get_CC()[name]


            CCDialog(self, on_submit, on_delete, col_tag, name, values)

        elif 'Re' in col_tag:
            
            def on_submit(col_tag, new_name, new_values):
                self.report.edit_Re_name(col_tag, new_name)
                self.refresh_ui()

            def on_delete(col_tag):
                self.report.del_Re(col_tag)
                self.refresh_ui()

            name = self.report.get_metadata()[col_tag]
            ReDialog(self, on_submit, on_delete, col_tag, name)
    


    def set_report(self, report: TestReport):
        self.report = report
        self.refresh_ui()

    def refresh_ui(self):

        

        if not self.report:
            self.test_name_label.config(text="Please create or open a test report.")
            return
        
        # delete all the metadata buttons to be re-written in the next step
        for widget in self.metadata_bar.winfo_children(): #except for refresh button
            widget.destroy()


        self.metadata_button_dict = {}
        self.sheet.set_sheet_data([], reset_col_positions=True, reset_row_positions=True)
        df = pd.DataFrame()


        # update the name of the test
        if self.report.tests == []:
            self.test_name_label.config(text='Please add a new test')
        else:



            self.test_name_label.config(text=f"Test Name: {self.report.selected_test.name}")
                
        
            # create the dict of buttons
            for key in self.report.get_metadata().keys():
                new_butt = ttk.Button(self.metadata_bar, text=key)

                self.metadata_button_dict[key] = new_butt

            if self.metadata_button_dict != {}:
                # pack the dict of buttons
                for key, butt in self.metadata_button_dict.items():
                    print(f"THIS IS THE KEY: {key}")
                    butt.config(command=lambda k=key: self.edit_column(k))
                    butt.pack(side=tk.LEFT)

            print(self.metadata_button_dict.keys())
            print(self.report.get_CC())

            df = self.report.get_root_table()
            self.sheet.set_sheet_data(df.values.tolist())
            self.sheet.headers(df.columns.tolist())
            

            print(self.report.get_root_table().head(5))
        self.sheet.pack(fill='both', expand=True)

        

        # self.after(100, lambda: self.sheet.focus_set())
        print(f"\n\n\n\nTHIS IS THE FOCUS: {self.focus_displayof()}\n\n\n\n")
        print(f"sheet data: {self.sheet.get_column_data(0)}")

        self.sheet.enable_bindings("all")


        
        self.sheet.focus_set()
