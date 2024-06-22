import click
from jira import JIRA

def create_jira_project(jira, project_key, project_name):
    """Creates a new Jira project."""
    project_template = 'com.pyxis.greenhopper.jira:gh-simplified-scrum-classic'
    jira.create_project(
        key=project_key,
        name=project_name,
        template_name=project_template,
    )
    print(f'Project {project_name} ({project_key}) created successfully.')

def create_jira_ticket(jira, project_key, summary, description, issue_type='Task'):
    """Creates a new ticket in a Jira project."""
    issue_dict = {
        'project': {'key': project_key},
        'summary': summary,
        'description': description,
        'issuetype': {'name': issue_type},
    }
    issue = jira.create_issue(fields=issue_dict)
    print(f'Ticket {issue.key} created successfully.')

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

if __name__ == '__main__':
    cli()

