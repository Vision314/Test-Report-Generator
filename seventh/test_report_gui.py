import tkinter as tk
import tkinter.filedialog as fd
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
from tkinter import ttk


from test_report import TestReport
import pickle

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Test Report Generator")
        self.geometry("800x600")

        # initialize when user selects a report
        self.report = None
        self.filepath = None

        # set up the menu bar
        self.menu = AppMenu(self)
        self.config(menu=self.menu) # puts the menu on the screen

        # placeholder frames
        self.tests_manager = TestsManager(self)
        self.test_editor = TestEditor(self)
        self.equipment_manager = EquipmentManager(self)
        self.cover_page_manager = CoverPageManager(self)

        # grid layout
        self.tests_manager.grid(row=0, column=0, rowspan=2, sticky='nsew')
        self.test_editor.grid(row=0, column=1, sticky='nsew')
        self.equipment_manager.grid(row=1, column=1, sticky='nsew')
        self.cover_page_manager.grid(row=0, column=2, rowspan=2, sticky='nsew')

        # Configure grid weights
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1) 

    # def load_report(self, filepath):
    #     with open(filepath, 'rb') as f:
    #         self.report = pickle.load(f)
        
    #     self.tests_manager.set_report(self.report)
    #     self.test_editor.set_report(self.report)
    #     self.equipment_manager.set_report(self.report)
    #     self.cover_page_manager.set_report(self.report)

    def refresh_all(self):
        self.tests_manager.refresh_ui()
        self.test_editor.refresh_ui()
        self.equipment_manager.refresh_ui()
        self.cover_page_manager.refresh_ui()

class AppMenu(tk.Menu):
    def __init__(self, parent: MainApp):
        super().__init__(parent)
        self.parent = parent

        file_menu = tk.Menu(self, tearoff=0) # tearoff=0 disables a feature of 'tearing off' the menu bar
        file_menu.add_command(label='New Report', command=self.new_report)
        file_menu.add_command(label='Open Report', command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.parent.quit)

        self.add_cascade(label='File', menu=file_menu)

    def new_report(self):
        title = sd.askstring("New Report", "Enter a title for the new report:")

        if not title:
            return # user cancelled
        
        filepath = fd.asksaveasfilename(defaultextension='.pickle',
                                        filetypes=[('Pickle Files', '*.pickle')],
                                        title='Save Report As')

        if not filepath:
            return # user cancelled
        
        report = TestReport(title=title)
        

        try:
            self.filepath = filepath
            report.pickle(filepath)
        except Exception as e:
            mb.showerror("ERROR", f"Failed to save report: {e}")

        self.parent.report = report
        self.parent.tests_manager.set_report(report)
        self.parent.test_editor.set_report(report)
        self.parent.equipment_manager.set_report(report)
        self.parent.cover_page_manager.set_report(report)

    def save(self):
        self.report.pickle(self.filepath)

    def open_file(self):
        pass

# ===========================================================================================

# column 0, rows 0 and 1
class TestsManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.report = None
        self.selected_test = None

        self.test_names = None
        self.test_categories = None

        self.test_tree = ttk.Treeview(self, selectmode='browse', columns=
                                      ('Test Category', 'Test Name'))
        
        

    def get_test_names(self):
        test_names = []

        for test in self.report.tests:
            test_names.append(test.name)
        
        self.test_names = test_names

    def get_category_names(self):
        test_categories = []

        for test in self.report.tests:
            test_categories.append(test.category)

        self.test_categories = test_categories
    
    def set_report(self, report: TestReport):
        self.report = report
        self.test_names = self.get_test_names()
        self.test_categories = self.get_category_names()

        self.refresh_ui()

    def refresh_ui(self):

        # my_tree = ttk.Treeview(self, selectmode='browse', columns=self.report.)



        # my_tree.pack(pady=20)

        tk.Label(self, text='THIS IS A LABEL!').pack()




# ==================================================================================

# column 1, row 0
class TestEditor(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.report = None
        self.refresh_ui()
    
    def set_report(self, report: TestReport):
        self.report = report
        self.refresh_ui()

    def refresh_ui(self):
        tk.Label(self, text='THIS IS A LABEL!').pack()


# ======================================================================================

# column 1, row 1
# bottom of screen, will be a list of checkboxes reading from a 
class EquipmentManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.report = None
        self.refresh_ui()
    
    def set_report(self, report: TestReport):
        self.report = report
        self.refresh_ui()

    def refresh_ui(self):
        tk.Label(self, text='THIS IS A LABEL!').pack()



class CoverPageManager(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.report = None


        

    
    def set_report(self, report: TestReport):
        self.report = report
        self.refresh_ui()

    def refresh_ui(self):

        tk.Label(self, text='THIS IS A LABEL!').pack()


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()