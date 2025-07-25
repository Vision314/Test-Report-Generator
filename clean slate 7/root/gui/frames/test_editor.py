import tkinter as tk
from tkinter import ttk
import tksheet
import pandas as pd

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
        
        


        self.sheet.enable_bindings((
                                    "single_click_edit",
                                    "edit_cell",
                                    "arrowkeys",
                                    "copy", "cut", "paste",
                                    "right_click_popup_menu",
                                    "rc_select",
                                    "rc_insert_row",
                                    "rc_delete_row",
                                    "rc_delete_column"
                                ))
        # self.sheet.focus_set()



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

        ReDialog(self, on_submit, '')

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
                pass

            name = self.report.get_metadata()[col_tag]
            values = self.report.get_CC()[name]


            CCDialog(self, on_submit, col_tag, name, values)

        elif 'Re' in col_tag:
            
            def on_submit(col_tag, new_name, new_values):
                self.report.edit_Re(col_tag, new_name)
                self.refresh_ui()

            name = self.report.get_metadata()[col_tag]
            ReDialog(self, on_submit, col_tag, name)
    


    def set_report(self, report: TestReport):
        self.report = report
        self.refresh_ui()

    def refresh_ui(self):

        

        if not self.report:
            self.test_name_label.config(text="Please create or open a test report.")
            return
        
        # delete all the metadata buttons to be re-written in the next step
        for widget in self.metadata_bar.winfo_children():
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
