from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title('TITLE HERE')


def open():
    global my_img

    root.filename = filedialog.askopenfilename(initialdir=path, title='Select A File', filetypes=(('png files', '*.png'), ('all files', '*.*')))
    Label(root, text=root.filename).pack()

    my_img = ImageTk.PhotoImage(Image.open(root.filename))
    Label(root, image=my_img).pack()





path = r"C:\Users\enfxm\Desktop\Python Testing\Test Report Template\Test-Report-Generator\seventh"



my_butt = Button(root, text='open file', command=open).pack()



root.mainloop()