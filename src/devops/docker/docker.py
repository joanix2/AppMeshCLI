import click
from jinja2 import Environment, FileSystemLoader
import os

# Function to generate Dockerfile
def generate_dockerfile(template_name, output_path, context):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    dockerfile_content = template.render(context)
    with open(output_path, 'w') as f:
        f.write(dockerfile_content)
    click.echo(f"Dockerfile generated at {output_path}")

# CLI setup with click
@click.group()
def cli():
    pass

@cli.command()
@click.argument('backend_type')
@click.argument('output_path', type=click.Path())
def create_dockerfile(backend_type, output_path):
    """Create a Dockerfile for the specified backend type"""
    template_name = f'{backend_type}.Dockerfile.j2'
    context = {}

    # Setup specific context
    if backend_type == 'dotnet':
        context = {'project_name': 'YourProject'}
    elif backend_type == 'angular':
        context = {'app_name': 'your-angular-app'}

    try:
        generate_dockerfile(template_name, output_path, context)
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
    """Create a docker-compose.yml file"""
    template_name = 'docker-compose.yml.j2'
    context = {
        'service_name': service_name,
        'dockerfile_path': dockerfile_path,
        'host_port': host_port,
        'container_port': container_port,
        'db_name': db_name
    }

    try:
        generate_file(template_name, output_path, context)
    except Exception as e:
        click.echo(f"Error: {e}")

if __name__ == '__main__':
    cli()


