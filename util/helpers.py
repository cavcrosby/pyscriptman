"""Contains useful functions for the entire project.

These functions are meant to be used where
needed in the project.

"""
# Standard Library Imports
import subprocess
import os
import shutil
from os.path import join, dirname, realpath

# Third Party Imports

# Local Application Imports
from util.message import Message


def change_target_filemode_recursive(target, permissions):
    """Changes an entire directory's (including the directory) permissions.
    
    This includes every node (file/directory) that is
    in the tree.

    Parameters
    ----------
    target : str
        Can be a relative/absolute path.
    permissions : int
        Represented in an integer, test cases use
        the stat module to represent permissions.

    """
    walk_root = dirname(realpath(target))

    for root, dirs, files in os.walk(target):
        walk_parent_dir = join(walk_root, root)
        for name in files:
            os.chmod(join(walk_parent_dir, name), permissions)
        for name in dirs:
            os.chmod(join(walk_parent_dir, name), permissions)
    os.chmod(target, permissions)


def git_add_commit_push(message):
    """Does a git-add-commit-push with all files."""
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"{message}"])
    subprocess.run(["git", "push", "origin", "master"])


def clone_repo(repo_path, repo_name):
    """Performs a git clone command."""
    try:
        subprocess.run(["git", "clone", repo_path, repo_name], check=True)
    except subprocess.CalledProcessError:
        raise


def mirror_repo(repo_path, repo_name):
    """Performs a git mirror command. Copying the entire Git repo."""
    try:
        subprocess.run(["git", "clone", "--mirror", repo_path, repo_name], check=True)
    except subprocess.CalledProcessError:
        raise


def bundle_repo(repo_path, repo_name):
    """Like a mirror but archiving the Git repo into one file."""
    try:
        mirror_repo(repo_path, repo_name)
        subprocess.run(
            [
                "git",
                "--git-dir",
                repo_name,
                "bundle",
                "create",
                f"{repo_name}.bundle",
                "--all",
            ],
            check=True,
        )
        shutil.rmtree(repo_name)
    except subprocess.CalledProcessError:
        raise


def get_pwd_local_dir_names():
    """Returns names of directories in the current present working directory.
    
    Returns
    -------
    list of str
        Directory names in the current present working directory.

    """
    root = os.getcwd()
    try:
        return [
            item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))
        ]
    except PermissionError:
        raise


def get_typeof_repo_names(host_path, barerepo):
    """Gets Git repos from a particular path.
    
    Parameters
    ----------
    host_path : str
        This will be the path to search for Git repos.
    barerepo : bool
        Whether or not to search for bare Git repos.

    Returns
    -------
    list of str
        Git repo names (not paths!).
    
    """
    pred1, pred2 = ("true", "false") if barerepo else ("false", "true")
    repo_names = list()
    pwd = os.getcwd()
    try:
        os.chdir(host_path)
        dirs = get_pwd_local_dir_names()
        for dir_node in dirs:
            os.chdir(dir_node)
            is_bare_repo = subprocess.run(
                ["git", "rev-parse", "--is-bare-repository"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                encoding="utf-8",
                check=True,
            )
            in_working_dir = subprocess.run(
                ["git", "rev-parse", "--is-inside-work-tree"],
                stderr=subprocess.PIPE,
                stdout=subprocess.PIPE,
                encoding="utf-8",
                check=True,
            )
            if (
                is_bare_repo.stderr == ""
                and is_bare_repo.stdout.rstrip() == pred1
                and in_working_dir.stdout.rstrip() == pred2
            ):
                repo_names.append(dir_node)
            os.chdir("..")
        os.chdir(pwd)
        return repo_names
    except PermissionError:
        raise
    except FileNotFoundError:
        raise
    except subprocess.CalledProcessError:
        raise


def copy_script_to_host(target, target_path, script):
    """Copies a file over to a remote host."""
    subprocess.run(["scp", script, f"{target}:{target_path}"], check=True)


def execute_script_on_host(target, target_path, script_path):
    """Runs python script on remote host.
    
    This script should search the target_path
    for bare Git repos and print them to standard
    out.

    Returns
    -------
    list of str
        Git repo names (not paths!).
    
    """
    completed_process = subprocess.run(
        ["ssh", target, f"cd {target_path}; python3 {script_path}"],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        encoding="utf-8",
        check=True,
    )
    repos_names = completed_process.stdout.split(",")
    repos_names[-1] = repos_names[-1].strip()  # e.g. 'repo1,repo1 - Copy\n'
    return repos_names


def remove_script_on_host(target, script):
    """Attempts to remove script that was copied to remote host."""
    try:
        subprocess.run(
            [
                "ssh",
                target,
                f'python3 -c "import os; path = os.path.expanduser(\\"{script}\\"); os.remove(path)"',
            ],
            check=True,
        )
    except subprocess.CalledProcessError:
        Message.print_script_removal_fail(target)


def expand_target_path_on_host(target, target_path):
    """Attempts to expand target path on remote host.
    
    This is incase ~ is used.
    
    """
    completed_process = subprocess.run(
        [
            "ssh",
            target,
            f'python3 -c "import os; print(os.path.join(os.path.expanduser(\\"{target_path}\\"), \\"\\"));"',
        ],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        encoding="utf-8",
        check=True,
    )
    return completed_process.stdout.rstrip()
