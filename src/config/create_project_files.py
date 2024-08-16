import os

def create_file(template_path, output_path):
    """Creates a single file from a template."""
    with open(template_path, 'r') as template_file:
        content = template_file.read()

    with open(output_path, 'w') as output_file:
        output_file.write(content)

    print(f'Created {os.path.basename(output_path)} in {os.path.dirname(output_path)}')

def create_env_file(project_path, templates_dir):
    """Creates the .env file."""
    template_path = os.path.join(templates_dir, 'env.j2')
    output_path = os.path.join(project_path, '.env')
    create_file(template_path, output_path)

def create_readme_file(project_path, templates_dir):
    """Creates the README.md file."""
    template_path = os.path.join(templates_dir, 'README.j2')
    output_path = os.path.join(project_path, 'README.md')
    create_file(template_path, output_path)

def create_gitignore_file(project_path, templates_dir):
    """Creates the .gitignore file."""
    template_path = os.path.join(templates_dir, 'gitignore.j2')
    output_path = os.path.join(project_path, '.gitignore')
    create_file(template_path, output_path)

def create_dockerignore_file(project_path, templates_dir):
    """Creates the .dockerignore file."""
    template_path = os.path.join(templates_dir, 'dockerignore.j2')
    output_path = os.path.join(project_path, '.dockerignore')
    create_file(template_path, output_path)

def create_requirements_file(project_path, templates_dir):
    """Creates the requirements.txt file."""
    template_path = os.path.join(templates_dir, 'requirements.j2')
    output_path = os.path.join(project_path, 'requirements.txt')
    create_file(template_path, output_path)

def create_all_files(project_path, templates_dir):
    """Creates all project files."""
    create_env_file(project_path, templates_dir)
    create_readme_file(project_path, templates_dir)
    create_gitignore_file(project_path, templates_dir)
    create_dockerignore_file(project_path, templates_dir)
    # create_requirements_file(project_path, templates_dir)

