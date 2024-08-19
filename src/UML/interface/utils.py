import inspect
import json

def class_to_dict(cls, to_json = False):
    class_data = {
        "name": cls.__name__,
        "functions": []
    }

    # Obtenir toutes les méthodes de la classe qui ne commencent pas par '__'
    methods = [m for m in inspect.getmembers(cls, inspect.isfunction) if not m[0].startswith('__')]
    for name, method in methods:
        output_signature = inspect.signature(method).return_annotation

        method_data = {
            "name": name,
            "parameters": [],
            "return_type": str(output_signature.__name__) if output_signature != inspect.Signature.empty and output_signature is not None else "None"
        }

        # Obtenir les paramètres pour chaque méthode
        params = inspect.signature(method).parameters
        for param_name, param in params.items():
            param_data = {
                "name": param_name,
                "type": param.annotation.__name__ if param.annotation != inspect.Parameter.empty and param.annotation is not None else "None",
                "is_input": True,  # Vous pouvez ajuster cette logique selon vos besoins
                "value": param.default if param.default != inspect.Parameter.empty else None
            }
            method_data["parameters"].append(param_data)

        class_data["functions"].append(method_data)

    if to_json:
        return json.dumps(class_data, indent=4)
    else :
        return class_data
