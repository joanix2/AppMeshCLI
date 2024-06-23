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

