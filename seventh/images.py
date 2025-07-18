from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox

root = Tk()
root.title('TITLE HERE')

# showinfo, showwarning, showerror, askquestion, askokcancel, askyesno

def info():
    resp = messagebox.showinfo(title='This is my popup!', message='Hello World!')
    Label(root, text=resp).pack()

def warning():
    resp = messagebox.showwarning(title='This is my popup!', message='Hello World!')
    Label(root, text=resp).pack()

def error():
    resp = messagebox.showerror(title='This is my popup!', message='Hello World!')
    Label(root, text=resp).pack()

def ayn():
    resp = messagebox.askyesno(title='This is my popup!', message='Hello World!')
    Label(root, text=resp).pack()

def aoc():
    resp = messagebox.askokcancel(title='This is my popup!', message='Hello World!')

    Label(root, text=resp).pack()

def aq():
    resp = messagebox.askokcancel(title='This is my popup!', message='Hello World!')

    Label(root, text=resp).pack()


Button(root, text='showinfo', command=info).pack()
Button(root, text='showerror', command=error).pack()
Button(root, text='showwarning', command=warning).pack()
Button(root, text='askyesno', command=ayn).pack()
Button(root, text='askquesiton', command=aq).pack()
Button(root, text='askcancel', command=aoc).pack()






root.mainloop()