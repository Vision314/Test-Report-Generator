import tkinter as tk
from tkinter import messagebox, ttk

# Sample nested dictionary
data = {
    'Alice': {'age': 30, 'city': 'NYC'},
    'Bob': {'age': 25}
}

def update_treeview():
    tree.delete(*tree.get_children())
    for name, subdict in data.items():
        parent = tree.insert('', 'end', text=name, values=("", ""))
        for key, value in subdict.items():
            tree.insert(parent, 'end', text="", values=(key, value))

def on_double_click(event):
    region = tree.identify("region", event.x, event.y)
    if region != "cell":
        return

    row_id = tree.identify_row(event.y)
    col = tree.identify_column(event.x)

    if not row_id or col != '#3':  # Only allow editing in "Value" column
        return

    x, y, width, height = tree.bbox(row_id, col)
    item = tree.item(row_id)
    key, old_value = item['values']

    # Identify parent to get name
    parent_id = tree.parent(row_id)
    if not parent_id:
        return  # Don't edit name rows

    name = tree.item(parent_id)['text']

    # Entry widget overlay
    entry = tk.Entry(tree)
    entry.place(x=x, y=y, width=width, height=height)
    entry.insert(0, old_value)
    entry.focus()

    def save_edit(event=None):
        new_value = entry.get()
        entry.destroy()
        data[name][key] = new_value
        update_treeview()

    entry.bind("<Return>", save_edit)
    entry.bind("<FocusOut>", save_edit)

def create_entry():
    name = name_entry.get()
    key = key_entry.get()
    value = value_entry.get()

    if not name or not key:
        messagebox.showwarning("Input Error", "Name and Key are required.")
        return

    if name not in data:
        data[name] = {}
    data[name][key] = value
    update_treeview()

def read_entry():
    name = name_entry.get()
    key = key_entry.get()
    value = data.get(name, {}).get(key)
    if value is not None:
        messagebox.showinfo("Value", f"{name} -> {key}: {value}")
    else:
        messagebox.showwarning("Not Found", "Entry not found.")

def delete_entry():
    name = name_entry.get()
    key = key_entry.get()
    if name in data and key in data[name]:
        del data[name][key]
        if not data[name]:
            del data[name]
        update_treeview()
    else:
        messagebox.showwarning("Not Found", "Entry not found.")

# GUI setup
root = tk.Tk()
root.title("Editable Treeview")

tk.Label(root, text="Name:").grid(row=0, column=0)
tk.Label(root, text="Key:").grid(row=1, column=0)
tk.Label(root, text="Value:").grid(row=2, column=0)

name_entry = tk.Entry(root)
key_entry = tk.Entry(root)
value_entry = tk.Entry(root)

name_entry.grid(row=0, column=1)
key_entry.grid(row=1, column=1)
value_entry.grid(row=2, column=1)

tk.Button(root, text="Create/Update", command=create_entry).grid(row=0, column=2)
tk.Button(root, text="Read", command=read_entry).grid(row=1, column=2)
tk.Button(root, text="Delete", command=delete_entry).grid(row=2, column=2)

# Treeview
tree = ttk.Treeview(root, columns=('Key', 'Value'), show='tree headings')
tree.heading('#0', text='Name')
tree.heading('Key', text='Key')
tree.heading('Value', text='Value')
tree.grid(row=3, column=0, columnspan=3, sticky='nsew')

tree.bind("<Double-1>", on_double_click)

# Layout
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(1, weight=1)

update_treeview()
root.mainloop()
