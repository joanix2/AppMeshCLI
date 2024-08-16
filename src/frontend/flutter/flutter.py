import os
from utilis.shell import run_command

def create_flutter_project(project_name, project_path=os.getcwd()):
    """Creates a new Flutter project at the specified path."""
    # Construire le chemin complet où le projet sera créé
    full_project_path = os.path.join(project_path, project_name)
    
    # Exécuter la commande pour créer le projet Flutter
    run_command(f'flutter create {full_project_path}')

def install_dependencies(project_name):
    """Runs flutter pub get to install dependencies."""
    project_path = os.path.join(os.getcwd(), project_name)
    os.chdir(project_path)
    run_command('flutter pub get')

# def add_flutter_firebase(project_name):
#     """Adds Firebase dependencies to the Flutter project."""
#     project_path = os.path.join(os.getcwd(), project_name)
#     os.chdir(project_path)
#     run_command('flutter pub add firebase_core firebase_auth cloud_firestore')

