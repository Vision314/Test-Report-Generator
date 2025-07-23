import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.username = 'FRANKIE'


        frame_main = ttk.Frame(self)
        frame_main.pack(fill=tk.BOTH, expand=True)

        btn_show_username = ttk.Button(frame_main,
                                       text='Show username',
                                       command=self.show_username)
        
        btn_show_username.pack(padx=10, pady=10)

    def show_username(self):
        username_window = UsernameWindow(self, 
                                         self.username)

class UsernameWindow(tk.Toplevel):
    def __init__(self, master, username):
        super().__init__(master)
        self.username = username

        self.frame_main = ttk.Frame(self)
        self.frame_main.pack(fill=tk.BOTH, expand=True)

        lbl = ttk.Label(self.frame_main,
                        text=f"USERNAM: {self.username}")
        
        lbl.pack(padx=50,pady=50)

if __name__ == '__main__':
    main_window = MainWindow()
    main_window.mainloop()