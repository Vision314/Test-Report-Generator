import tkinter as tk
from tkinter import ttk
import tkinter.simpledialog as sd
import tkinter.messagebox as mb

from model.test_report import TestReport


# column 0, rows 0 and 1
class TestsManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        print("TEST MANAGER CONSTRUCTED")

        self.report = None
        self.selected_test = None

        # ttk.Label(self, text="THIS IS THE TEST MANAGER!").pack()
        

        self.add_test_button = ttk.Button(self, text='ADD TEST', command=self.add_test)
        self.add_test_button.grid(row=0, column=0)

        self.remove_test_button = ttk.Button(self, text='REMOVE TEST', command=self.remove_test)
        self.remove_test_button.grid(row=0, column=1)



        self.test_tree = ttk.Treeview(self, columns=("Test Name",), show="tree headings")
        self.test_tree.heading('#0', text='Test Category')
        self.test_tree.heading('Test Name', text='Test Name')

        self.test_tree.column('#0', width=50, stretch=True)
        self.test_tree.column('Test Name', width=50, stretch=True)

        self.test_tree.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.test_tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
    

    def add_test(self):
        if not self.report:
            mb.showerror('Add Test Error', 'You must open or create a test report before adding tests.\nFile -> New Report\nFile -> Open Report')
            return
        
        category = sd.askstring('Test Category', 'Please give this test a category:', parent=self)
        name = sd.askstring('Test Name', 'Please give this test a name:', parent=self)

        if category is not None and name is not None: # might have to switch to None instead of ''
            self.report.add_test(category, name)

        else:
            mb.showerror('Missing Field', 'You are missing a required field!')

        self.refresh_ui()
    
    def remove_test(self):
        pass
    

    def on_tree_select(self, event):
        selected_item = self.test_tree.selection()

        if not selected_item:
            return
        
        item_id = selected_item[0]
        parent_id = self.test_tree.parent(item_id)

        if parent_id == '':
            # this is a category
            category = self.test_tree.item(item_id, 'text')
            print(f"Selected Category: {category}")

        else:
            # this is a test
            category = self.test_tree.item(parent_id, 'text')
            test_name = self.test_tree.item(item_id, 'text')

            print(F"Selected Test: {test_name} | Category: {category}")






    def set_report(self, report: TestReport):
        self.report = report
        # self.test_names = self.report.
        # self.test_categories = self.category_names

        self.refresh_ui()

    def refresh_ui(self):

        # clear existing items
        for item in self.test_tree.get_children():
            self.test_tree.delete(item)

        if not self.report:
            return
        
        # group tests by category
        category_map = {}
        for test in self.report.tests:
            category = test.category
            name = test.name

            # create category group if not already added
            if category not in category_map:
                parent_id = self.test_tree.insert('', 'end', text=category)
                category_map[category] = parent_id

            # add test as child under that category
            # self.test_tree.insert(category_map[category], 'end', text='', values=(name,))
            self.test_tree.insert(category_map[category], 'end', text=name)