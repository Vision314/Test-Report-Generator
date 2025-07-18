from tkinter import *
from PIL import ImageTK, Image

root = Tk()
root.title('TITLE HERE')

button_quit = Button(root, text='EXIT PROGRAM', command=root.quit)
button_quit.pack()

root.mainloop()