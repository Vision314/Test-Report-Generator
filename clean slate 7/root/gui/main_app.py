import tkinter as tk
# import tkinter.filedialog as fd
# import tkinter.simpledialog as sd
# import tkinter.messagebox as mb
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path

from model.test_report import TestReport
from gui.frames.cover_page_manager import CoverPageManager
from gui.frames.equipment_manager import EquipmentManager
from gui.frames.test_editor import TestEditor
from gui.frames.test_manager import TestsManager
from gui.app_menu import AppMenu


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        style = ttk.Style()
        style.theme_use('clam')

        style.configure('TPanedwindow',
                        sashwidth=10,
                        background='#cccccc')
        
        style.configure('Treeview.Heading',
                        relief='flat',
                        background='#f0f0f0')


        self.title("Test Report Generator")
        self.geometry("1600x600")

        # load logo.png from assets/
        logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
        logo_img = tk.PhotoImage(file=logo_path)
        # set it as window icon
        self.iconphoto(False, logo_img)
        self._icon_img = logo_img # prevent image from being garbage collected


        # initialize when user selects a report
        self.report = None
        self.filepath = None

        # set up the menu bar
        self.menu = AppMenu(self)
        self.config(menu=self.menu) # puts the menu on the screen

        

        # create main horizontal PanedWidonw
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL) # horizontal means they are packed blocks from left to right
        main_paned.pack(fill=tk.BOTH, expand=True) # fill any extra space # expand with the window if it resizes

        # placeholder frames
        self.tests_manager = TestsManager(self)
        main_paned.add(self.tests_manager, weight=1)# left panel (test_manager)

        middle_paned = ttk.PanedWindow(main_paned, orient=tk.VERTICAL)
        main_paned.add(middle_paned, weight=3) # wider weight for right side

        self.test_editor = TestEditor(self)
        self.equipment_manager = EquipmentManager(self)
        # add test_editor at top right
        middle_paned.add(self.test_editor, weight=3)
        middle_paned.add(self.equipment_manager, weight=1)

        self.cover_page_manager = CoverPageManager(self)
        

        main_paned.add(self.cover_page_manager, weight=1)


    def refresh_all(self):
        self.tests_manager.refresh_ui()
        self.test_editor.refresh_ui()
        self.equipment_manager.refresh_ui()
        self.cover_page_manager.refresh_ui()
