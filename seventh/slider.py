from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.geometry('400x400')


class elder:
    def __init__(self, master):
        myFrame = Frame(master)
        myFrame.pack()

        self.myButton = Button(master, text='click me', command=self.clicker)

        self.myButton.pack(pady=20)

        options = ['mondya', 'tues', 'wed', 'thur', 'fri']

        clicked = StringVar()
        clicked.set(options[0])

        drop = OptionMenu(master, clicked, *options)
        drop.pack(pady=20)

        
    
    def clicker(self):
        print('HIII')






e = elder(root)


root.mainloop()