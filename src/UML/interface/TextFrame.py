import tkinter as tk
from tkinter import scrolledtext, Frame
from tkinter import font

class DBMLTextEditor(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Define the font to use in the ScrolledText widget
        self.custom_font = font.Font(family="Helvetica", size=14)  # Vous pouvez ajuster la famille et la taille de la police ici

        # Create ScrolledText widget with the custom font
        self.dbml_text = scrolledtext.ScrolledText(self, font=self.custom_font, width=40)
        self.dbml_text.pack(expand=True, fill='both')
        self.dbml_text.bind('<KeyRelease>', self.on_text_change)

    def on_text_change(self, event=None):
        """Simple syntax highlighting for DBML input."""
        self.dbml_text.tag_remove("TableName", '1.0', tk.END)
        self.dbml_text.tag_configure("TableName", foreground="blue")

        lines = self.dbml_text.get("1.0", tk.END).split('\n')
        for i, line in enumerate(lines):
            if line.startswith('Table'):
                start_index = f"{i+1}.0"
                end_index = f"{i+1}.end"
                self.dbml_text.tag_add("TableName", start_index, end_index)