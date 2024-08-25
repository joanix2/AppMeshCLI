import os
from utilis.json_save import JsonDict

def get_description():
    # Path to the configuration file
    config_file = os.path.join(os.getcwd(), 'config.json')
    
    # Load the configuration using JsonDict
    config = JsonDict(config_file)

    return config["description"]

def compile_text(text):
    try:
        # Tenter d'évaluer la chaîne comme un f-string
        result = eval(f"f'''{text}'''")
        return result
    except Exception as e:
        # Si une erreur se produit, renvoyer la chaîne d'origine
        return text


def main():
    string = "description : {get_description()}"
    
    print(compile_text(string))

if __name__ == "__main__":
    main()