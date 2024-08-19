import tkinter as tk
from interface.MainFrame import MainCanvas
from interface.TextFrame import DBMLTextEditor

class AppWin(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Class Diagram Editor")
        self.geometry("1200x600")

        # Set minsize for window to ensure there is enough space for both components
        MIN_WIDTH = 600
        self.minsize(MIN_WIDTH, 400)

        # Configure grid weights to allocate space dynamically
        self.grid_columnconfigure(0, weight=1, minsize=MIN_WIDTH//3)  # Minimum size to ensure visibility
        self.grid_columnconfigure(1, weight=2, minsize=(MIN_WIDTH*2)//3)  # Minimum size to ensure visibility
        self.grid_rowconfigure(0, weight=1)

        # Create a DBML text editor instance (1/3 of the screen width)
        self.dbml_editor = DBMLTextEditor(self)
        self.dbml_editor.grid(row=0, column=0, sticky="nsew")

        # Create main canvas area (2/3 of the screen width)
        self.canvas = MainCanvas(self)
        self.canvas.grid(row=0, column=1, sticky="nsew")

# Création et affichage de la fenêtre
if __name__ == "__main__":
    app = AppWin()
    app.mainloop()