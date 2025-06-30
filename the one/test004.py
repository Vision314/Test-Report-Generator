import tkinter as tk
from tkinter import ttk

# Root window
root = tk.Tk()
root.title("My App")

# Menu bar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Open")
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

# Toolbar (Frame with buttons)
toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
tool_button = tk.Button(toolbar, text="Tool")
tool_button.pack(side=tk.LEFT, padx=2, pady=2)
toolbar.pack(side=tk.TOP, fill=tk.X)

# Main frame
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# Widgets inside main_frame
label = tk.Label(main_frame, text="Enter text:")
label.grid(row=0, column=0, padx=5, pady=5)

entry = tk.Entry(main_frame)
entry.grid(row=0, column=1, padx=5, pady=5)

text = tk.Text(main_frame, height=5)
text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# Run the app
root.mainloop()
