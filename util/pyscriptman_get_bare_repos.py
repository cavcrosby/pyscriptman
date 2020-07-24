"""This is a script to be copied over by pyscriptman."""
# Standard Library Imports
import os
import subprocess

# Third Party Imports

# Local Application Imports


def get_pwd_local_dir_names():
    """Returns names of directories in the current present working directory.
    
    Returns
    -------
    list of str
        Directory names in the current present working directory.

    """
    root = os.getcwd()
    return [
        item
        for item in os.listdir(root)
        if os.path.isdir(os.path.join(root, item))
    ]


def get_pwd_bare_repo_names():
    """Gets Git repos from a present working directory.

    Returns
    -------
    list of str
        Git repo names (not paths!) concatenated together with a comma
        (e.g. repo1,repo2).
    
    """
    repo_names = list()
    dirs = get_pwd_local_dir_names()
    for dir in dirs:
        os.chdir(dir)
        is_bare_repo = subprocess.run(
            ["git", "rev-parse", "--is-bare-repository"],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )
        in_working_dir = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            encoding="utf-8",
        )
        if (
            is_bare_repo.stderr == ""
            and is_bare_repo.stdout.rstrip() == "true"
            and in_working_dir.stdout.rstrip() == "false"
        ):
            repo_names.append(dir)
        os.chdir("..")
    return ",".join(repo_names)


print(get_pwd_bare_repo_names())
