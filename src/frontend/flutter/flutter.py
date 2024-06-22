import os
import click
import subprocess

def run_command(command):
    """Runs a shell command and prints the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    result.check_returncode()

def create_flutter_project(project_name):
    """Creates a new Flutter project."""
    run_command(f'flutter create {project_name}')

def install_dependencies(project_name):
    """Runs flutter pub get to install dependencies."""
    project_path = os.path.join(os.getcwd(), project_name)
    os.chdir(project_path)
    run_command('flutter pub get')

def add_flutter_firebase(project_name):
    """Adds Firebase dependencies to the Flutter project."""
    project_path = os.path.join(os.getcwd(), project_name)
    os.chdir(project_path)
    run_command('flutter pub add firebase_core firebase_auth cloud_firestore')

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

if __name__ == '__main__':
    cli()

