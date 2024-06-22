import os
import subprocess
import click
import ast

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
    subprocess.run(['django-admin', 'startproject', project_name, project_path])

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

@click.group()
def cli():
    pass

@cli.command()
@click.argument('path')
@click.argument('project_name')
def create_project(path, project_name):
    """Create a new Django project and add rest_framework to INSTALLED_APPS."""
    create_django_project(path, project_name)
    click.echo(f"Created Django project {project_name} at {path}")

@cli.command()
@click.argument('app_path')
def add_model(app_path):
    """Append a simple model to the models.py file of the given app."""
    append_models(app_path)
    click.echo(f"Added model to {app_path}/models.py")

@cli.command()
@click.argument('app_path')
def register_models(app_path):
    """Register models in the admin site."""
    models_tree = get_models(app_path)
    register_models_to_admin(app_path, models_tree)
    click.echo(f"Registered models from {app_path}/models.py in admin site")

if __name__ == '__main__':
    cli()

