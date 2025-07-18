from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title('TITLE HERE')


def open():
    top = Toplevel()
    lbl = Label(top, text='Hlellooooo').pack()
    top.title('bjsdlfkjsldkfj')
    Button(top, text='OPEN WIDNOW', command=open).pack()
    Button(root, text='destroy', command=top.destroy).pack()


b = Button(root, text='OPEN WIDNOW', command=open).pack()



root.mainloop()