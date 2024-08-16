import difflib

def levenshtein_distance(a, b):
    """Calculate the Levenshtein distance between two strings."""
    return difflib.SequenceMatcher(None, a, b).ratio()

def validate_framework_name(framwork_name, framework_list):
    """
    Valide le nom du framework et propose une correction en cas d'erreur.
    
    Args:
        framwork_name (str): Nom du framework à valider.
        framework_list (list): Liste des frameworks supportés.
    
    Returns:
        str: Le nom du framework validé ou corrigé.
    
    Raises:
        ValueError: Si le framework n'est pas supporté et qu'aucune correction n'est acceptée.
    """
    framwork_name = framwork_name.lower()

    if framwork_name not in framework_list:
        closest_match = None
        closest_distance = 0

        # Trouver le framework le plus proche
        for fw in framework_list:
            distance = levenshtein_distance(framwork_name, fw)
            if distance > closest_distance:
                closest_match = fw
                closest_distance = distance

        # Si la distance est acceptable (< 0.8 par exemple, ce qui équivaut à 20% de différence)
        if closest_match and closest_distance > 0.8:
            confirmation = input(f"Did you mean '{closest_match}'? (y/n): ")
            if confirmation.lower() == 'y':
                return closest_match
            else:
                raise ValueError(f"Only frameworks in {framework_list} are supported.")
        else:
            raise ValueError(f"Only frameworks in {framework_list} are supported.")
    return framwork_name