import os
import click
from jira import JIRA # type: ignore

from backend.c_sharp_dotnet.c_sharp_dotnet import initialize_entity_framework_project
from backend.python.django.django import append_models, create_django_project, get_models, register_models_to_admin
from devops.git.git import create_git_branch, create_git_project, merge_git_branches
from frontend.angular.angular import add_material_to_project, create_angular_project, install_dependencies
from frontend.flutter.flutter import add_flutter_firebase, create_flutter_project
from project_management.figma.figma import add_component_to_file, create_figma_file
from config.create_project_files import create_all_files
from project_management.jira_management.jira_lib import create_jira_project, create_jira_ticket


# -------------------------- Project Init -------------------------- #

@click.command()
@click.argument('project_path', default='.', type=click.Path())
@click.option('--templates_dir', type=click.Path(), default=os.path.join(os.getcwd(), 'templates'), help='The directory containing the template files.')
def cli(project_path, templates_dir):
    """CLI to create project files from templates."""
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    create_all_files(project_path, templates_dir)

# -------------------------- Django -------------------------- #

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

# -------------------------- Entity Framework -------------------------- #

@click.command()
@click.argument('solution_name')
@click.argument('project_name')
def cli(solution_name, project_name):
    """CLI to initialize a .NET server with Entity Framework."""
    try:
        initialize_entity_framework_project(solution_name, project_name)
    except Exception as e:
        click.echo(f"Error: {e}")

# -------------------------- Flutter -------------------------- #

@click.command()
@click.argument('project_name')
@click.option('--add-firebase', is_flag=True, help='Add Firebase to the project.')
def cli(project_name, add_firebase):
    """CLI to initialize a Flutter project."""
    create_flutter_project(project_name)
    install_dependencies(project_name)
    if add_firebase:
        add_flutter_firebase(project_name)
    print(f'Successfully created Flutter project {project_name}.')

# -------------------------- Angular -------------------------- #

@click.command()
@click.argument('project_name')
@click.option('--add-material', is_flag=True, help='Add Angular Material to the project.')
def cli(project_name, add_material):
    """CLI to initialize an Angular project."""
    create_angular_project(project_name)
    if add_material:
        add_material_to_project(project_name)
    install_dependencies(project_name)
    print(f'Successfully created Angular project {project_name}.')


# -------------------------- Figma -------------------------- #

@click.group()
@click.option('--access_token', prompt='Figma access token', help='Your Figma access token.')
@click.pass_context
def cli(ctx, access_token):
    """CLI to manage Figma projects and files."""
    ctx.ensure_object(dict)
    ctx.obj['access_token'] = access_token

@cli.command()
@click.argument('team_id')
@click.argument('file_name')
@click.pass_context
def create_file(ctx, team_id, file_name):
    """Creates a new Figma file."""
    access_token = ctx.obj['access_token']
    create_figma_file(access_token, team_id, file_name)

@cli.command()
@click.argument('file_id')
@click.argument('component_name')
@click.pass_context
def add_component(ctx, file_id, component_name):
    """Adds a new component to a Figma file."""
    access_token = ctx.obj['access_token']
    add_component_to_file(access_token, file_id, component_name)

# -------------------------- Jira -------------------------- #

@click.group()
@click.option('--server', prompt='Jira server URL', help='The URL of the Jira server.')
@click.option('--username', prompt='Jira username', help='Your Jira username.')
@click.option('--password', prompt=True, hide_input=True, help='Your Jira password.')
@click.pass_context
def cli(ctx, server, username, password):
    """CLI to manage Jira projects and tickets."""
    options = {'server': server}
    jira = JIRA(options, basic_auth=(username, password))
    ctx.obj = jira

@cli.command()
@click.argument('project_key')
@click.argument('project_name')
@click.pass_context
def create_project(ctx, project_key, project_name):
    """Creates a new Jira project."""
    jira = ctx.obj
    create_jira_project(jira, project_key, project_name)

@cli.command()
@click.argument('project_key')
@click.argument('summary')
@click.argument('description')
@click.option('--issue_type', default='Task', help='The type of the Jira issue (e.g., Task, Bug, Story).')
@click.pass_context
def create_ticket(ctx, project_key, summary, description, issue_type):
    """Creates a new Jira ticket."""
    jira = ctx.obj
    create_jira_ticket(jira, project_key, summary, description, issue_type)

# -------------------------- Git -------------------------- #

@cli.command()
@click.argument('project_name')
def create_project(project_name):
    """Create a new Git project"""
    git_dir = create_git_project(project_name)
    click.echo(f'Initialized empty Git repository in {git_dir}')

@cli.command()
@click.argument('branch_name')
def create_branch(branch_name):
    """Create a new branch"""
    branch = create_git_branch(branch_name)
    click.echo(f'Created branch {branch}')

@cli.command()
@click.argument('source_branch')
@click.argument('target_branch')
def merge_branches(source_branch, target_branch):
    """Merge one branch into another"""
    source, target = merge_git_branches(source_branch, target_branch)
    click.echo(f'Merged {source} into {target}')

# -------------------------- Docker -------------------------- #


@cli.command()
@click.argument('backend_type')
@click.argument('output_path', type=click.Path())
def create_dockerfile(backend_type, output_path):
    try:
        create_dockerfile(backend_type, output_path)
        click.echo(f"Dockerfile generated at {output_path}")
    except Exception as e:
        click.echo(f"Error: {e}")
        click.echo("Unsupported backend type. Supported types are 'django', 'dotnet', 'angular', and 'flutter'.")

@cli.command()
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