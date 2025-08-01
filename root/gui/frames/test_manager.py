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
        # self.selected_test = None

        # ttk.Label(self, text="THIS IS THE TEST MANAGER!").pack()

        # Header area (like a group label)
        self.header = ttk.Label(
            self, 
            text="🗄️Test Manager", 
            anchor="w",
            font=("Segoe UI", 10, "bold"),
            background="#e0e0e0",
            relief="raised"
        )
        self.header.pack(fill=tk.X)
        
        toolbar = ttk.Frame(self)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        toolbar.configure(style="Toolbar.TFrame")

        self.add_test_button = ttk.Button(toolbar, text='➕', style='ToolButton.TButton', command=self.add_test)
        self.add_test_button.pack(side=tk.LEFT, padx=1, pady=2)

        self.remove_test_button = ttk.Button(toolbar, text='➖', style='ToolButton.TButton', command=self.remove_test)
        self.remove_test_button.pack(side=tk.LEFT, padx=1, pady=2)



        self.test_tree = ttk.Treeview(self, columns=("Test Name",), show="tree headings")
        self.test_tree.heading('#0', text='Test Category')
        self.test_tree.heading('Test Name', text='Test Name')

        self.test_tree.column('#0', width=50, stretch=True)
        self.test_tree.column('Test Name', width=50, stretch=True)

        # self.test_tree.grid(row=1, column=0, columnspan=2, sticky='nsew')
        self.test_tree.pack(fill=tk.BOTH, expand=True)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.test_tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.test_tree.bind("<Double-1>", self.on_tree_double_click)
        
    def on_tree_double_click(self, event):
        # Get clicked item
        item_id = self.test_tree.identify_row(event.y)
        if not item_id:
            return

        parent_id = self.test_tree.parent(item_id)
        print(f"ITEM ID: {item_id}")
        print(f"PARENT ID: {parent_id}")
        
        # Only proceed if it's a test, not a category
        if parent_id:
            old_name = self.test_tree.item(item_id, 'text')
            category = self.test_tree.item(parent_id, 'text')
            

            new_name = sd.askstring("Rename Test", f"Enter a new name for test '{old_name}':", initialvalue=old_name, parent=self)

            if new_name and new_name.strip():
                self.report.set_test_name(new_name.strip())
                
            self.refresh_ui()

        else:
            old_category = self.test_tree.item(item_id, 'text')
            print(f"OLD CATEGORY: {old_category}")

            new_cat = sd.askstring("Rename Test", f"Enter a new name for category '{old_category}':", initialvalue=old_category, parent=self)

            if new_cat and new_cat.strip():
                self.report.rename_category(old_category, new_cat.strip())
                
            self.refresh_ui()

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
        if not self.report:
            mb.showerror('Remove Test Error', 'You must open or create a test report before removing tests.\nFile -> New Report\nFile -> Open Report')
            return
        
        cat_del = self.report.selected_test.category
        name_del = self.report.selected_test.name

        self.report.remove_test(cat_del, name_del)
        self.refresh_ui()
        

    

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

            self.report.select_test(category, test_name)
            # print(self.report.get_root_table().head(5))

        self.master.test_editor.refresh_ui()
        self.master.equipment_manager.refresh_ui()






    def set_report(self, report: TestReport):
        self.report = report
        # self.test_names = self.report.
        # self.test_categories = self.category_names

        self.refresh_ui()

    def refresh_ui(self):

        if not self.report:
            return

        # save the open categories
        open_categories = set()
        for item in self.test_tree.get_children():
            if self.test_tree.item(item, 'open'):
                open_categories.add(self.test_tree.item(item, 'text'))


        # clear existing items
        for item in self.test_tree.get_children():
            self.test_tree.delete(item)

        
        # group tests by category
        category_map = {}
        for test in self.report.tests:
            category = test.category
            name = test.name

            # create category group if not already added
            if category not in category_map:
                parent_id = self.test_tree.insert('', 'end', text=category, open=(category in open_categories))
                category_map[category] = parent_id

            # add test as child under that category
            # self.test_tree.insert(category_map[category], 'end', text='', values=(name,))
            self.test_tree.insert(category_map[category], 'end', text=name)

        # self.report.select_test(category, name)
        # print(self.report.selected_test.head(5))

            