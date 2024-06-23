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

def create_angular_project(project_name):
    """Creates a new Angular project."""
    run_command(f'ng new {project_name} --skip-install')

def add_material_to_project(project_name):
    """Adds Angular Material to the project."""
    project_path = os.path.join(os.getcwd(), project_name)
    os.chdir(project_path)
    run_command('ng add @angular/material')

def install_dependencies(project_name):
    """Installs npm dependencies."""
    project_path = os.path.join(os.getcwd(), project_name)
    os.chdir(project_path)
    run_command('npm install')

