import click
import git
from git import Repo
import os

@click.group()
def cli():
    """Git CLI Tool"""
    pass

@cli.command()
@click.argument('project_name')
def create_project(project_name):
    """Create a new Git project"""
    os.makedirs(project_name, exist_ok=True)
    repo = Repo.init(project_name)
    click.echo(f'Initialized empty Git repository in {repo.git_dir}')

@cli.command()
@click.argument('branch_name')
def create_branch(branch_name):
    """Create a new branch"""
    repo = Repo('.')
    new_branch = repo.create_head(branch_name)
    click.echo(f'Created branch {branch_name}')

@cli.command()
@click.argument('source_branch')
@click.argument('target_branch')
def merge_branches(source_branch, target_branch):
    """Merge one branch into another"""
    repo = Repo('.')
    repo.git.checkout(target_branch)
    repo.git.merge(source_branch)
    click.echo(f'Merged {source_branch} into {target_branch}')

if __name__ == '__main__':
    cli()
