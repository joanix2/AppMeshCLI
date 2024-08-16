import os
import subprocess
import ast
from utilis.shell import run_command

def add_installed_app(settings_path, installed_app_name):
    with open(settings_path, 'r+') as f:
        content = f.read()
        content = content.replace("INSTALLED_APPS = [", f"INSTALLED_APPS = [\n    '{installed_app_name}',")
        f.seek(0)
        f.write(content)
        f.truncate()

def create_django_project(path, project_name):
    # Créer le projet Django dans le chemin spécifié
    project_path = os.path.join(path, project_name)
    os.makedirs(project_path, exist_ok=True)
    run_command(['django-admin', 'startproject', project_name, project_path])

    # Chemin du fichier settings.py
    settings_path = os.path.join(project_path, project_name, 'settings.py')
    # Ajout de 'rest_framework' aux applications installées
    add_installed_app(settings_path, "rest_framework")

def append_models(app_path):
    # Créer un modèle simple
    models_path = os.path.join(app_path, "models.py")
    with open(models_path, 'a') as f:
        f.write("\n\nclass Item(models.Model):\n")
        f.write("    name = models.CharField(max_length=100)\n")
        f.write("    description = models.TextField()\n")

def get_models(app_path):
    models_file = os.path.join(app_path, "models.py")

    # Lire le contenu du fichier models.py
    with open(models_file, 'r') as file:
        models_content = file.read()

    # Utiliser ast pour analyser le contenu du fichier
    return ast.parse(models_content) 

def register_models_to_admin(app_path, models_tree):
    models_names = [node.name for node in ast.walk(models_tree) if isinstance(node, ast.ClassDef)]
    admin_file = os.path.join(app_path, "admin.py")

    # Préparer le contenu à ajouter dans admin.py
    admin_content = []
    admin_content.append("from django.contrib import admin")
    admin_content.append(f"from .models import {', '.join(models_names)}\n")

    # Générer les lignes pour enregistrer chaque modèle
    for model_name in models_names:
        admin_content.append(f"admin.site.register({model_name})")

    # Écrire dans le fichier admin.py
    with open(admin_file, 'w') as file:
        file.write('\n'.join(admin_content))
    print(f"Updated {admin_file} with {len(models_names)} models.")

