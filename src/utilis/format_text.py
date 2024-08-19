import re

def to_snake_case(text):
    """
    Convertit n'importe quel texte au format snake_case.
    """
    # Remplace les espaces, tirets et autres séparateurs par des underscores
    text = re.sub(r'[\s\-]+', '_', text)
    
    # Ajoute un underscore avant chaque majuscule (sauf en début de chaîne) et convertit en minuscules
    text = re.sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
    
    # Remplace les caractères non alphanumériques (sauf underscore) par des underscores
    text = re.sub(r'[^a-z0-9_]', '', text)
    
    return text

def get_project_description():
    """
    Demande à l'utilisateur d'entrer la description du projet.
    Continue à demander tant qu'une description valide (non vide) n'est pas fournie.
    """
    while True:
        description = input("Veuillez entrer la description du projet : ").strip()
        
        if description:
            return description
        else:
            print("La description ne peut pas être vide. Veuillez réessayer.")

