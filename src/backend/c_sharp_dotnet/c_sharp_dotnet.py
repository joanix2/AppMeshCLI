import os
import click
import subprocess
from jinja2 import Environment, FileSystemLoader

def run_command(command):
    """Runs a shell command and prints the output."""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr)
    result.check_returncode()

def create_solution(solution_name):
    """Creates a new .NET solution."""
    run_command(f'dotnet new sln -n {solution_name}')

def create_api_project(project_name, solution_name):
    """Creates a new .NET API project and adds it to the solution."""
    run_command(f'dotnet new webapi -n {project_name}')
    run_command(f'dotnet sln {solution_name}.sln add {project_name}/{project_name}.csproj')

def add_entity_framework(project_name):
    """Adds Entity Framework Core to the project."""
    run_command(f'dotnet add {project_name}/{project_name}.csproj package Microsoft.EntityFrameworkCore')
    run_command(f'dotnet add {project_name}/{project_name}.csproj package Microsoft.EntityFrameworkCore.SqlServer')
    run_command(f'dotnet add {project_name}/{project_name}.csproj package Microsoft.EntityFrameworkCore.Tools')

# Fonction pour générer des fichiers à partir de modèles
def generate_file(template_name, output_path, context):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    file_content = template.render(context)
    with open(output_path, 'w') as f:
        f.write(file_content)
    return output_path

def create_initial_model(project_name):
    """Creates an initial Entity Framework model."""
    models_dir = os.path.join(project_name, "Models")
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    
    context = {}
    template_name = "ApplicationDbContext.cs.j2"
    output_path = os.path.join(models_dir, "ApplicationDbContext.cs")
    generate_file(template_name, output_path, context)

def update_startup_file(project_name):
    """Updates the Startup.cs file to use Entity Framework."""
    startup_file = os.path.join(project_name, "Startup.cs")
    with open(startup_file, 'r') as f:
        existing_content = f.read()

    context = {'existing_content': existing_content}
    template_name = "Startup.cs.j2"
    new_content = generate_file(template_name, startup_file, context)

    with open(startup_file, 'w') as f:
        f.write(new_content)

def create_appsettings_file(project_name):
    """Creates the appsettings.json file with a default connection string."""
    context = {}
    template_name = "appsettings.json.j2"
    appsettings_file = os.path.join(project_name, "appsettings.json")
    generate_file(template_name, appsettings_file, context)


def initialize_entity_framework_project(solution_name, project_name):
    """Initializes the .NET solution with the specified project and Entity Framework setup."""
    create_solution(solution_name)
    create_api_project(project_name, solution_name)
    add_entity_framework(project_name)
    create_initial_model(project_name)
    update_startup_file(project_name)
    create_appsettings_file(project_name)
    print(f'Successfully created .NET solution {solution_name} with API project {project_name} and Entity Framework setup.')

