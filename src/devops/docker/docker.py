from jinja2 import Environment, FileSystemLoader

# Function to generate file from template
def generate_file(template_name, output_path, context):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    file_content = template.render(context)
    with open(output_path, 'w') as f:
        f.write(file_content)
    return output_path


def create_dockerfile(backend_type, output_path):
    """Create a Dockerfile for the specified backend type"""
    template_name = f'{backend_type}.Dockerfile.j2'
    context = {}

    # Setup specific context
    if backend_type == 'dotnet':
        context = {'project_name': 'YourProject'}
    elif backend_type == 'angular':
        context = {'app_name': 'your-angular-app'}

    generate_file(template_name, output_path, context)


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
    
    generate_file(template_name, output_path, context)