import tkinter as tk
from tkinter import ttk


from model.test_report import TestReport
from gui.frames.dialogs import CCDialog


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

        
        self.test_name_label = ttk.Label(self, text="Please create or open a test report.")
        self.test_name_label.pack(side=tk.TOP, padx=5, pady=5)



        self.metadata_bar = ttk.Frame(self, relief=tk.RAISED, width=300, height=25)
        self.metadata_bar.pack(side=tk.TOP, pady=10)

        self.metadata_button_dict = {}



    def add_CC(self):
        if not self.report:
            return
        
        def on_submit(name, values):
            self.report.add_CC(name, values)
            self.refresh_ui()

        CCDialog(self, on_submit, '', '')

        print("HIT!")
        print(self.report.get_CC())
        print(self.report.get_metadata())

        # self.refresh_ui()

    def add_Re(self):
        pass

    def add_Ca(self):
        pass

    def add_Sp(self):
        pass


    def edit_column(self, col_tag):
        print(col_tag)
        print(self.report.get_metadata()[col_tag])



        def on_submit(name, values):
            self.report.add_CC(name, values)
            self.refresh_ui()

        name = self.report.get_metadata()[col_tag]
        values = self.report.get_CC()[name]


        CCDialog(self, on_submit, name, values)

    
    def set_report(self, report: TestReport):
        self.report = report
        self.refresh_ui()

    def refresh_ui(self):

        if not self.report:
            self.test_name_label.config(text="Please create or open a test report.")
            return

        # update the name of the test
        self.test_name_label.config(text=f"Test Name: {self.report.selected_test.name}")
        

        # self.metadata_button_list = self.report.get_metadata()

        # delete all the metadata buttons to be re-written in the next step
        for widget in self.metadata_bar.winfo_children():
            widget.destroy()

        self.metadata_button_dict = {}
        
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