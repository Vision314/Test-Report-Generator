import tkinter as tk
import tkinter.simpledialog as sd
import tkinter.messagebox as mb
import tkinter.filedialog as fd

from model.test_report import TestReport





class AppMenu(tk.Menu):
    def __init__(self, parent): # parent will be MainApp
        super().__init__(parent)
        self.parent = parent

        file_menu = tk.Menu(self, tearoff=0) # tearoff=0 disables a feature of 'tearing off' the menu bar
        file_menu.add_command(label='New Report', command=self.new_report)
        file_menu.add_command(label='Open Report', command=self.open_report)
        file_menu.add_separator()
        file_menu.add_command(label='Save', command=self.save)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.parent.quit)

        edit_menu = tk.Menu(self, tearoff=0)
        edit_menu.add_command(label='Refresh UI', command=self.parent.refresh_all)

        self.add_cascade(label='File', menu=file_menu)
        self.add_cascade(label='Edit', menu=edit_menu)

    def new_report(self):
        title = sd.askstring("New Report", "Enter a title for the new report:")

        if not title:
            mb.showerror('Missing Field', 'You are missing a required field!')
            return # user cancelled
        
        filepath = fd.asksaveasfilename(defaultextension='.pickle',
                                        filetypes=[('Pickle Files', '*.pickle')],
                                        title='Save Report As')

        if not filepath:
            return # user cancelled
        
        report = TestReport(title=title)

        
        

        try:
            self.parent.filepath = filepath
            report.pickle(filepath)
        except Exception as e:
            mb.showerror("ERROR", f"Failed to save report: {e}")

        self.parent.report = report
        self.parent.tests_manager.set_report(report)
        self.parent.test_editor.set_report(report)
        self.parent.equipment_manager.set_report(report)
        self.parent.cover_page_manager.set_report(report)
        self.parent.image_viewer.set_report(report)

        self.master.refresh_all()

    def save(self):
        self.parent.report.pickle(self.parent.filepath)

    def open_report(self):
        filepath = fd.askopenfilename(title="Open Test Report",
                                      filetypes=[("Pickle files", "*.pickle"), 
                                                 ("All Files", "*.*")])
        
        if not filepath:
            return
        
        try:
            report = TestReport.unpickle(filepath)
            self.parent.report = report
            self.parent.filepath = filepath

            self.parent.tests_manager.set_report(report)
            self.parent.test_editor.set_report(report)
            self.parent.equipment_manager.set_report(report)
            self.parent.cover_page_manager.set_report(report)
            self.parent.refresh_all()

        except Exception as e:
            mb.showerror("Error", f"Could not load report: \n{e}")
            print(e)