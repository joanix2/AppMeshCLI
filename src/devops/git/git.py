import os
from git import Repo

def create_git_project(project_name):
    """Create a new Git project"""
    os.makedirs(project_name, exist_ok=True)
    repo = Repo.init(project_name)
    return repo.git_dir

def create_git_branch(branch_name):
    """Create a new branch"""
    repo = Repo('.')
    new_branch = repo.create_head(branch_name)
    return branch_name

def merge_git_branches(source_branch, target_branch):
    """Merge one branch into another"""
    repo = Repo('.')
    repo.git.checkout(target_branch)
    repo.git.merge(source_branch)
    return source_branch, target_branch
