import tkinter as tk
from tksheet import Sheet

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

def create_sheet_block(parent, title_text, subtitle_text, data):
    # Title
    title = tk.Label(parent, text=title_text, font=("Helvetica", 14, "bold"))
    title.pack(anchor="w", pady=(10, 0), padx=10)

    # Subtitle
    subtitle = tk.Label(parent, text=subtitle_text, font=("Helvetica", 10, "italic"))
    subtitle.pack(anchor="w", padx=10)

    # Sheet
    sheet = Sheet(parent, data=data, width=500, height=150)
    sheet.enable_bindings()
    sheet.pack(pady=(0, 20), padx=10)

    return sheet

# Main window
root = tk.Tk()
root.title("Multiple tksheets with Titles and Scroll")

# Scrollable frame
scrollable_container = ScrollableFrame(root)
scrollable_container.pack(fill="both", expand=True)

# Create 5 sheets with headers
for i in range(5):
    title = f"Table {i + 1}: Sample Data"
    subtitle = f"This is a description of Table {i + 1}"
    data = [[f"R{r}C{c}" for c in range(5)] for r in range(5)]
    create_sheet_block(scrollable_container.scrollable_frame, title, subtitle, data)

root.mainloop()
