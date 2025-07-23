from tkinter import *
from tkinter import ttk

root = Tk()
root.geometry('500x500')


my_tree = ttk.Treeview(root, selectmode=BROWSE)

#define columns
my_tree['columns'] = ('Name', 'ID', 'Favorite Pizza')

# format columns
my_tree.column('#0', width=120, minwidth=25)
my_tree.column('Name', anchor=W, width=120)
my_tree.column('ID', anchor=CENTER, width=80)
my_tree.column('Favorite Pizza', anchor=W, width=120)

# create headings
my_tree.heading('#0', text="Label", anchor=W)
my_tree.heading('Name', text='Name', anchor=W)
my_tree.heading('ID', text='ID', anchor=CENTER)
my_tree.heading('Favorite Pizza', text='Fav ZAA', anchor=W)

# add data
my_tree.insert(parent='', index='end', iid=0, text='', values=('John', 1, 'Pepperoni'))
my_tree.insert(parent='', index='end', iid=1, text='', values=('Frank', 2, 'Sausage'))
my_tree.insert(parent='', index='end', iid=2, text='', values=('Sue', 3, 'Chocolate'))
my_tree.insert(parent='', index='end', iid=3, text='', values=('Morgan', 4, 'Ceasar'))
my_tree.insert(parent='', index='end', iid=4, text='', values=('Dexter', 5, 'Chicken'))
my_tree.insert(parent='', index='end', iid=5, text='', values=('Sal', 6, 'BBQ'))

# add child
my_tree.insert(parent='0', index='end', iid=6, text='Child', values=('Steve', 1.2, 'Onion'))
# my_tree.move('6', '0','0')

my_tree.pack(pady=20)

print(my_tree.selection()[0])



root.mainloop()