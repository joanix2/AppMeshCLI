import os
import click
from jira import JIRA # type: ignore

from utilis.format_text import to_snake_case
from settings import BACK_FRAMEWORK, FRONT_FRAMEWORK
from utilis.json_save import JsonDict
from utilis.similarity import validate_framework_name
from backend.c_sharp_dotnet.c_sharp_dotnet import initialize_entity_framework_project
from backend.python.django.django import append_models, create_django_project, get_models, register_models_to_admin
from devops.git.git import create_git_branch, create_git_project, merge_git_branches
from frontend.angular.angular import add_material_to_project, create_angular_project, install_dependencies
from frontend.flutter.flutter import create_flutter_project
from project_management.figma.figma import add_component_to_file, create_figma_file
from config.create_project_files import create_all_files
from project_management.jira_management.jira_lib import create_jira_project, create_jira_ticket

import subprocess


# ---------------------------- Init CLI ---------------------------- #

@click.group()
def cli():
    pass

# -------------------------- Project Init -------------------------- #

@cli.command()
@click.argument('full_path', type=click.Path())
@click.option('--front', type=str, default='flutter', help='Framework front-end à utiliser.')
@click.option('--back', type=str, default='django', help='Framework back-end à utiliser.')
@click.option('--api', type=str, default='graphql', help='Type d\'API à utiliser.')
@click.option('--database', type=str, default='postgres', help='Base de données à utiliser.')
@click.option('--templates_dir', type=click.Path(), default=os.path.join(os.path.dirname(__file__), 'config', 'templates'), help='The directory containing the template files.')
def init(full_path, front, back, api, database, templates_dir):
    """
    CLI to create project files from templates.
    
    Arguments:
    full_path -- The full path where the project will be created, including the project name.
    
    Options:
    --front      -- Framework front-end to use (default: flutter).
    --back       -- Framework back-end to use (default: django).
    --api        -- Type of API to use (default: graphql).
    --database   -- Database to use (default: postgres).
    --templates_dir -- Directory containing the template files.
    """

    # Split the full path into directory path and project name
    project_path, project_name = os.path.split(full_path)
    
    # If the user provided only the project name without a path
    if not project_path:
        project_path = os.getcwd()  # Use the current directory
    
    # Construire le chemin complet du projet
    full_project_path = os.path.join(project_path, project_name)
    
    # Création du répertoire du projet si nécessaire
    if not os.path.exists(full_project_path):
        os.makedirs(full_project_path)

    # Path to the configuration file
    config_file = os.path.join(full_project_path, 'config.json')
    
    # Load the configuration using JsonDict
    config = JsonDict(config_file)
    
    # Update the configuration with the current settings
    config.update({
        "project_path": full_project_path,
        "front": front,
        "back": back,
        "api": api,
        "database": database,
        "templates_dir": templates_dir
    })
    
    # Afficher les paramètres pour vérifier
    print(f"Creating project '{project_name}' at '{full_project_path}'")
    print(f"Front-end framework: {front}")
    print(f"Back-end framework: {back}")
    print(f"API type: {api}")
    print(f"Database: {database}")
    print(f"Templates directory: {templates_dir}")

    # Exemple d'étapes supplémentaires pour initialiser le projet
    # - Initialisation du dépôt Git
    create_git_project(full_project_path)
    
    # - Initialisation du projet front-end
    front_project_name = f"{to_snake_case(project_name)}_front"
    front_framwork_name = create_front(front_project_name, front, full_project_path)
    
    # - Initialisation du projet back-end
    back_project_name = f"{to_snake_case(project_name)}_back"
    back_framwork_name = create_back(back_project_name, back, full_project_path)

    # - Création des fichiers à partir des templates
    create_all_files(full_project_path, templates_dir)


def create_front(project_name, framwork_name, path):
    """
    Initialisation d'un projet front
    """
    framwork_name = validate_framework_name(framwork_name, FRONT_FRAMEWORK)
    
    # Initialisation du projet en fonction du framework choisi
    if framwork_name == 'flutter':
        create_flutter_project(project_name, path)
    elif framwork_name == 'angular':
        subprocess.run(['ng', 'new', 'my_angular_app'])
    elif framwork_name == 'react':
        subprocess.run(['npx', 'create-react-app', 'my_react_app'])
    elif framwork_name == 'vue':
        subprocess.run(['npx', 'vue', 'create', 'my_vue_app'])
    elif framwork_name == 'svelte':
        subprocess.run(['npx', 'degit', 'sveltejs/template', 'my_svelte_app'])
    else:
        raise ValueError(f"Unsupported framework: {framwork_name}")

    print(f"{framwork_name.capitalize()} project initialized successfully.")

    return framwork_name

def create_back(project_name, framwork_name, path):
    """
    Initialisation d'un projet back-end
    """
    framwork_name = validate_framework_name(framwork_name, BACK_FRAMEWORK)
    
    # Initialisation du projet en fonction du framework choisi
    if framwork_name == 'django':
        """Create a new Django project and add rest_framework to INSTALLED_APPS."""
        create_django_project(path, project_name)
        click.echo(f"Created Django project {project_name} at {path}")
    elif framwork_name == 'flask':
        subprocess.run(['flask', 'start', 'my_flask_project'])
    elif framwork_name == 'express':
        subprocess.run(['npx', 'express-generator', 'my_express_project'])
    elif framwork_name == 'spring':
        subprocess.run(['spring', 'init', '--dependencies=web', 'my_spring_project'])
    elif framwork_name == 'laravel':
        subprocess.run(['composer', 'create-project', '--prefer-dist', 'laravel/laravel', 'my_laravel_project'])
    elif framwork_name == 'rails':
        subprocess.run(['rails', 'new', 'my_rails_project'])
    elif framwork_name == 'dotnet':
        # Commandes pour créer un projet .NET avec Entity Framework
        subprocess.run(['dotnet', 'new', 'webapi', '-o', 'MyDotNetProject'])
        subprocess.run(['dotnet', 'add', 'MyDotNetProject', 'package', 'Microsoft.EntityFrameworkCore'])
        subprocess.run(['dotnet', 'add', 'MyDotNetProject', 'package', 'Microsoft.EntityFrameworkCore.SqlServer'])
        subprocess.run(['dotnet', 'add', 'MyDotNetProject', 'package', 'Microsoft.EntityFrameworkCore.Tools'])
    else:
        raise ValueError(f"Unsupported framework: {framwork_name}")

    print(f"{framwork_name.capitalize()} project initialized successfully.")

    return framwork_name

# -------------------------- Django -------------------------- #

# @click.command()
# @click.argument('app_path')
# def add_model(app_path):
#     """Append a simple model to the models.py file of the given app."""
#     append_models(app_path)
#     click.echo(f"Added model to {app_path}/models.py")

# @click.command()
# @click.argument('app_path')
# def register_models(app_path):
#     """Register models in the admin site."""
#     models_tree = get_models(app_path)
#     register_models_to_admin(app_path, models_tree)
#     click.echo(f"Registered models from {app_path}/models.py in admin site")

# -------------------------- Entity Framework -------------------------- #

@click.command()
@click.argument('solution_name')
@click.argument('project_name')
def create_dotnet(solution_name, project_name):
    """CLI to initialize a .NET server with Entity Framework."""
    try:
        initialize_entity_framework_project(solution_name, project_name)
    except Exception as e:
        click.echo(f"Error: {e}")

# -------------------------- Flutter -------------------------- #

@click.command()
@click.argument('project_name')
def create_flutter(project_name, add_firebase):
    """CLI to initialize a Flutter project."""
    create_flutter_project(project_name)
    install_dependencies(project_name)
    print(f'Successfully created Flutter project {project_name}.')

# -------------------------- Angular -------------------------- #

@click.command()
@click.argument('project_name')
@click.option('--add-material', is_flag=True, help='Add Angular Material to the project.')
def create_angular(project_name, add_material):
    """CLI to initialize an Angular project."""
    create_angular_project(project_name)
    if add_material:
        add_material_to_project(project_name)
    install_dependencies(project_name)
    print(f'Successfully created Angular project {project_name}.')


# -------------------------- Figma -------------------------- #

# @click.group()
# @click.option('--access_token', prompt='Figma access token', help='Your Figma access token.')
# @click.pass_context
# def init_figma(ctx, access_token):
#     """CLI to manage Figma projects and files."""
#     ctx.ensure_object(dict)
#     ctx.obj['access_token'] = access_token

# @click.command()
# @click.argument('team_id')
# @click.argument('file_name')
# @click.pass_context
# def create_file(ctx, team_id, file_name):
#     """Creates a new Figma file."""
#     access_token = ctx.obj['access_token']
#     create_figma_file(access_token, team_id, file_name)

# @click.command()
# @click.argument('file_id')
# @click.argument('component_name')
# @click.pass_context
# def add_component(ctx, file_id, component_name):
#     """Adds a new component to a Figma file."""
#     access_token = ctx.obj['access_token']
#     add_component_to_file(access_token, file_id, component_name)

# -------------------------- Jira -------------------------- #

# @click.group()
# @click.option('--server', prompt='Jira server URL', help='The URL of the Jira server.')
# @click.option('--username', prompt='Jira username', help='Your Jira username.')
# @click.option('--password', prompt=True, hide_input=True, help='Your Jira password.')
# @click.pass_context
# def init_jira(ctx, server, username, password):
#     """CLI to manage Jira projects and tickets."""
#     options = {'server': server}
#     jira = JIRA(options, basic_auth=(username, password))
#     ctx.obj = jira

# @click.command()
# @click.argument('project_key')
# @click.argument('project_name')
# @click.pass_context
# def create_project(ctx, project_key, project_name):
#     """Creates a new Jira project."""
#     jira = ctx.obj
#     create_jira_project(jira, project_key, project_name)

# @click.command()
# @click.argument('project_key')
# @click.argument('summary')
# @click.argument('description')
# @click.option('--issue_type', default='Task', help='The type of the Jira issue (e.g., Task, Bug, Story).')
# @click.pass_context
# def create_ticket(ctx, project_key, summary, description, issue_type):
#     """Creates a new Jira ticket."""
#     jira = ctx.obj
#     create_jira_ticket(jira, project_key, summary, description, issue_type)

# -------------------------- Git -------------------------- #

@click.command()
@click.argument('project_name')
def create_project(project_name):
    """Create a new Git project"""
    git_dir = create_git_project(project_name)
    click.echo(f'Initialized empty Git repository in {git_dir}')

@click.command()
@click.argument('branch_name')
def create_branch(branch_name):
    """Create a new branch"""
    branch = create_git_branch(branch_name)
    click.echo(f'Created branch {branch}')

@click.command()
@click.argument('source_branch')
@click.argument('target_branch')
def merge_branches(source_branch, target_branch):
    """Merge one branch into another"""
    source, target = merge_git_branches(source_branch, target_branch)
    click.echo(f'Merged {source} into {target}')

# -------------------------- Docker -------------------------- #


@click.command()
@click.argument('backend_type')
@click.argument('output_path', type=click.Path())
def create_dockerfile(backend_type, output_path):
    try:
        create_dockerfile(backend_type, output_path)
        click.echo(f"Dockerfile generated at {output_path}")
    except Exception as e:
        click.echo(f"Error: {e}")
        click.echo("Unsupported backend type. Supported types are 'django', 'dotnet', 'angular', and 'flutter'.")

@click.command()
@click.argument('service_name')
@click.argument('dockerfile_path')
@click.argument('host_port')
@click.argument('container_port')
@click.argument('db_name')
@click.argument('output_path', type=click.Path())
def create_docker_compose(service_name, dockerfile_path, host_port, container_port, db_name, output_path):
    try:
        create_docker_compose(service_name, dockerfile_path, host_port, container_port, db_name, output_path)
        click.echo(f"docker-compose.yml generated at {output_path}")
    except Exception as e:
        click.echo(f"Error: {e}")

if __name__ == '__main__':
    cli()
