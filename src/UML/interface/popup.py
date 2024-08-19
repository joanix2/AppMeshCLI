import tkinter as tk
from tkinter import messagebox
from typing import Optional, List
from interface.models import ModelDTO, ParameterDTO

class ParameterFrame(tk.Frame):
    def __init__(self, parent, protection_levels=None, types=None, remove_callback=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        if protection_levels is None:
            protection_levels = ['Public', 'Private', 'Protected']
        if types is None:
            types = ['String', 'Integer', 'Float', 'Boolean', 'Date']

        self.remove_callback = remove_callback  # Function to call when the parameter is removed

        # Protection Level Dropdown
        self.protection_var = tk.StringVar(value=protection_levels[0])
        protection_menu = tk.OptionMenu(self, self.protection_var, *protection_levels)
        protection_menu.pack(side='left', padx=5)

        # Parameter Name
        self.param_name_entry = tk.Entry(self)
        self.param_name_entry.pack(side='left', fill='x', expand=True, padx=5)

        # Parameter Type Dropdown
        self.param_type_var = tk.StringVar(value=types[0])
        type_menu = tk.OptionMenu(self, self.param_type_var, *types)
        type_menu.pack(side='left', fill='x', expand=True, padx=5)

        # Remove Button
        remove_button = tk.Button(self, text="x", command=self.remove_parameter, fg="red")
        remove_button.pack(side='left', padx=5)

    def get_parameter(self):
        """Returns the parameter details as a dictionary."""
        return {
            "protection": self.protection_var.get(),
            "name": self.param_name_entry.get(),
            "type": self.param_type_var.get()
        }

    def remove_parameter(self):
        """Removes the parameter frame from the parent container."""
        if self.remove_callback:
            self.remove_callback(self)

class ModelCreationPopup(tk.Toplevel):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Create New Model")
        self.result: Optional[ModelDTO] = None  # To store the DTO after validation
        
        # Main container
        container = tk.Frame(self)
        container.pack(padx=10, pady=10, fill="both", expand=True)

        # Nom du modèle
        tk.Label(container, text="Model Name:").pack(anchor="w")
        self.model_name_entry = tk.Entry(container)
        self.model_name_entry.pack(fill="x", pady=5)

        # Ajout des paramètres
        self.params_frame = tk.Frame(container)
        self.params_frame.pack(fill="both", expand=True, pady=10)
        
        self.params = []
        self.add_parameter()  # Ensure at least one parameter is present initially

        self.add_param_button = tk.Button(container, text="Add Parameter", command=self.add_parameter)
        self.add_param_button.pack(fill="x", pady=5)

        # Buttons in a horizontal frame
        button_frame = tk.Frame(container)
        button_frame.pack(fill="x", pady=10)

        self.submit_button = tk.Button(button_frame, text="Create Model", command=self.submit)
        self.submit_button.pack(side="right", padx=5)
        
        self.cancel_button = tk.Button(button_frame, text="Cancel", command=self.destroy)
        self.cancel_button.pack(side="right", padx=5)

    def add_parameter(self):
        param_frame = ParameterFrame(self.params_frame, remove_callback=self.remove_parameter)
        param_frame.pack(fill='x', pady=5)
        self.params.append(param_frame)

    def remove_parameter(self, param_frame):
        """Removes a parameter from the params list if more than one parameter exists."""
        if len(self.params) > 1:
            self.params.remove(param_frame)
            param_frame.destroy()
        else:
            tk.messagebox.showerror("Error", "At least one parameter is required.")

    def submit(self):
        model_name = self.model_name_entry.get()
        if not model_name:
            tk.messagebox.showerror("Error", "Model name cannot be empty.")
            return

        parameters = []
        for param_frame in self.params:
            param = param_frame.get_parameter()
            if not param["name"]:
                tk.messagebox.showerror("Error", "All parameters must have a name.")
                return
            parameters.append(ParameterDTO(protection=param["protection"], name=param["name"], type=param["type"]))

        if len(parameters) < 1:
            tk.messagebox.showerror("Error", "At least one parameter is required.")
            return

        # Création du ModelDTO
        self.result = ModelDTO(name=model_name, parameters=parameters)
        
        # Fermer la fenêtre après validation
        self.destroy()

    def get_result(self) -> Optional[ModelDTO]:
        """Returns the ModelDTO after the popup is closed, or None if canceled."""
        self.wait_window()  # Wait until the window is closed
        return self.result

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    popup = ModelCreationPopup(root)
    result = popup.get_result()

    if result:
        print(result)
    else:
        print("Model creation was canceled.")
