import click
import requests
import json

BASE_URL = "https://api.figma.com/v1"

def create_figma_file(access_token, team_id, file_name):
    """Creates a new Figma file."""
    headers = {
        "X-Figma-Token": access_token,
        "Content-Type": "application/json"
    }
    data = {
        "name": file_name,
        "description": "Created with CLI",
        "parent_id": team_id
    }
    response = requests.post(f"{BASE_URL}/files", headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        file_id = response.json()['id']
        print(f"File '{file_name}' created successfully with ID {file_id}.")
        return file_id
    else:
        print(f"Failed to create file: {response.text}")
        response.raise_for_status()

def add_component_to_file(access_token, file_id, component_name):
    """Adds a new component to the Figma file."""
    headers = {
        "X-Figma-Token": access_token,
        "Content-Type": "application/json"
    }
    data = {
        "name": component_name,
        "type": "COMPONENT",
        "description": "Component created with CLI"
    }
    response = requests.post(f"{BASE_URL}/files/{file_id}/components", headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        component_id = response.json()['id']
        print(f"Component '{component_name}' added successfully with ID {component_id}.")
    else:
        print(f"Failed to add component: {response.text}")
        response.raise_for_status()

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

if __name__ == '__main__':
    cli()

