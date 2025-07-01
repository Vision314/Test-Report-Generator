
import os
import json
import tkinter as tk
from tkinter import ttk

ROOT_PATH = r"C:\Users\enfxm\Desktop\Python Testing\Test Report Template\Test-Report-Generator\the_two\TEMPLATE FORMAT"  # Adjust to your folder root
STATE_FILE = "test_selections.json"

test_selection = {}           # Maps tree ID to checked state
test_metadata = {}            # Maps tree ID to (category, test) raw names

# ------------------------------
# Format display name from folder name
# ------------------------------
def display_name(folder_name):
    return folder_name.replace('_', ' ').title()

# ------------------------------
# Handle click on checkbox area
# ------------------------------
def on_click(event):
    region = tree.identify("region", event.x, event.y)
    column = tree.identify_column(event.x)
    row_id = tree.identify_row(event.y)

    if region == "tree" and column == "#0" and row_id in test_selection:
        toggle_test(row_id)

def toggle_test(test_id):
    current = test_selection.get(test_id, True)
    test_selection[test_id] = not current
    icon = "✅" if not current else "❌"
    tree.item(test_id, text=icon)
    tree.tag_configure(test_id, foreground='black' if not current else 'gray')

    test_name = tree.item(test_id, 'values')[0]
    status = "checked" if not current else "unchecked"
    print(f"{test_name} is {status}")

# ------------------------------
# Build the tree structure
# ------------------------------
def build_tree():
    for category in os.listdir(ROOT_PATH):
        category_path = os.path.join(ROOT_PATH, category)
        if not os.path.isdir(category_path):
            continue

        cat_display = display_name(category)
        cat_id = tree.insert('', 'end', text='', open=True, values=(cat_display,))

        for test in os.listdir(category_path):
            test_path = os.path.join(category_path, test)
            if not os.path.isdir(test_path):
                continue

            csv_path = os.path.join(test_path, 'csv')
            if not os.path.isdir(csv_path):
                continue

            test_display = display_name(test)
            test_id = tree.insert(cat_id, 'end', text='✅', values=(test_display,), tags=(test,))
            test_selection[test_id] = True
            test_metadata[test_id] = (category, test)  # raw names
            tree.tag_configure(test_id, foreground='black')

# ------------------------------
# Save/load checkbox state using raw folder names
# ------------------------------
def save_checkbox_state(filepath=STATE_FILE):
    data = {}
    for test_id, checked in test_selection.items():
        category, test = test_metadata[test_id]
        key = f"{category}:{test}"
        data[key] = checked
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Saved checkbox state to {filepath}")

def load_checkbox_state(filepath=STATE_FILE):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r') as f:
        data = json.load(f)

    for test_id in test_selection.keys():
        category, test = test_metadata[test_id]
        key = f"{category}:{test}"
        checked = data.get(key, True)
        test_selection[test_id] = checked
        icon = "✅" if checked else "❌"
        tree.item(test_id, text=icon)
        tree.tag_configure(test_id, foreground='black' if checked else 'gray')

# ------------------------------
# GUI setup
# ------------------------------
root = tk.Tk()
root.title("Test File Manager")

tree = ttk.Treeview(root, columns=('label',), show='tree headings')
tree.heading('#0', text='Include')
tree.heading('label', text='Test Name')

tree.column('#0', width=60, anchor='center')
tree.column('label', width=300)

tree.pack(fill='both', expand=True)
tree.bind("<Button-1>", on_click)

# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

save_btn = tk.Button(btn_frame, text="Save", command=save_checkbox_state)
save_btn.pack(side='left', padx=5)

load_btn = tk.Button(btn_frame, text="Load", command=load_checkbox_state)
load_btn.pack(side='left', padx=5)

# Build tree and load saved state
build_tree()
load_checkbox_state()

root.mainloop()
