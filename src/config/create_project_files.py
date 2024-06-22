import os
import click

def create_file(template_path, output_path):
    """Creates a single file from a template."""
    with open(template_path, 'r') as template_file:
        content = template_file.read()

    with open(output_path, 'w') as output_file:
        output_file.write(content)

    print(f'Created {os.path.basename(output_path)} in {os.path.dirname(output_path)}')

def create_env_file(project_path, templates_dir):
    """Creates the .env file."""
    template_path = os.path.join(templates_dir, 'env_template.txt')
    output_path = os.path.join(project_path, '.env')
    create_file(template_path, output_path)

def create_readme_file(project_path, templates_dir):
    """Creates the README.md file."""
    template_path = os.path.join(templates_dir, 'README_template.txt')
    output_path = os.path.join(project_path, 'README.md')
    create_file(template_path, output_path)

def create_gitignore_file(project_path, templates_dir):
    """Creates the .gitignore file."""
    template_path = os.path.join(templates_dir, 'gitignore_template.txt')
    output_path = os.path.join(project_path, '.gitignore')
    create_file(template_path, output_path)

def create_dockerignore_file(project_path, templates_dir):
    """Creates the .dockerignore file."""
    template_path = os.path.join(templates_dir, 'dockerignore_template.txt')
    output_path = os.path.join(project_path, '.dockerignore')
    create_file(template_path, output_path)

def create_requirements_file(project_path, templates_dir):
    """Creates the requirements.txt file."""
    template_path = os.path.join(templates_dir, 'requirements_template.txt')
    output_path = os.path.join(project_path, 'requirements.txt')
    create_file(template_path, output_path)

def create_all_files(project_path, templates_dir):
    """Creates all project files."""
    create_env_file(project_path, templates_dir)
    create_readme_file(project_path, templates_dir)
    create_gitignore_file(project_path, templates_dir)
    create_dockerignore_file(project_path, templates_dir)
    create_requirements_file(project_path, templates_dir)

@click.command()
@click.argument('project_path', type=click.Path())
@click.option('--templates_dir', type=click.Path(), default=os.path.join(os.getcwd(), 'templates'), help='The directory containing the template files.')
def cli(project_path, templates_dir):
    """CLI to create project files from templates."""
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    create_all_files(project_path, templates_dir)

if __name__ == '__main__':
    cli()

