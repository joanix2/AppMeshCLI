from art import text2art
from PIL import Image, ImageDraw, ImageFont
import textwrap

def generer_ascii_art(texte):
    ascii_art = text2art(texte)
    return ascii_art

def generer_contour_ascii(texte):
    lignes = texte.split('\n')  # Divise le texte en lignes
    longueur_max = max(len(ligne) for ligne in lignes)  # Trouve la longueur maximale parmi toutes les lignes

    contour_ascii = []
    contour_ascii.append("┌" + "─" * (longueur_max + 2) + "┐")  # Ligne supérieure

    lignes = [""] + lignes[:]

    for ligne in lignes:
        espaces_blancs = " " * (longueur_max - len(ligne))  # Ajoute des espaces pour aligner le texte à droite
        contour_ascii.append(f"│ {ligne}{espaces_blancs} │")

    contour_ascii.append("└" + "─" * (longueur_max + 2) + "┘")  # Ligne inférieure

    return "\n".join(contour_ascii)

def lire_fichier_texte(nom_fichier):
    try:
        with open(nom_fichier, 'r', encoding='utf-8') as fichier:
            contenu = fichier.read()
            return contenu
    except FileNotFoundError:
        return f"Le fichier '{nom_fichier}' n'a pas été trouvé."
    except Exception as e:
        return f"Une erreur s'est produite : {str(e)}"

def texte_to_image(texte: str, nom_fichier_image: str, font_size: int = 30, couleur_fond: str = 'black', couleur_texte: str = 'yellow'):
    """
    Convertit un texte en une image avec du texte.

    Args:
        texte (str): Le texte à afficher sur l'image.
        nom_fichier_image (str): Le nom du fichier image à sauvegarder.
        font_size (int): La taille de la police. Par défaut, 30.
        couleur_fond (str): La couleur du fond de l'image. Par défaut, 'white'.
        couleur_texte (str): La couleur du texte. Par défaut, 'black'.
    """
    # Définir la taille de l'image et la police
    font = ImageFont.truetype("fonts/Ubuntu_Mono/UbuntuMono-Regular.ttf", font_size)
    lignes = texte.split('\n')
    max_ligne_longueur = max(font.getbbox(ligne)[2] for ligne in lignes)
    max_ligne_hauteur = font.getbbox(lignes[0])[3]
    largeur_image = max_ligne_longueur + 20  # marges
    hauteur_image = max_ligne_hauteur * len(lignes) + 20  # marges

    # Créer une image avec un fond de couleur spécifiée
    image = Image.new('RGB', (largeur_image, hauteur_image), color=couleur_fond)
    draw = ImageDraw.Draw(image)

    # Dessiner le texte sur l'image
    y_text = 10
    for ligne in lignes:
        draw.text((10, y_text), ligne, font=font, fill=couleur_texte)
        y_text += max_ligne_hauteur

    # Sauvegarder l'image
    image.save(nom_fichier_image)

def main():
    texte_a_afficher = "App Mesh CLI"
    ascii_art_resultat = generer_ascii_art(texte_a_afficher)

    contour_ascii = generer_contour_ascii(ascii_art_resultat)
    print(contour_ascii)

    # Convertir l'ASCII art en image
    nom_fichier_image = "ascii_art_image.png"
    texte_to_image(contour_ascii, nom_fichier_image)
    print(f"L'image a été sauvegardée sous le nom '{nom_fichier_image}'.")

if __name__ == "__main__":
    main()

