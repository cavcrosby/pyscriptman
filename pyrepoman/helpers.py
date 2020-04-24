# Standard Library Imports
import os, subprocess
from os.path import realpath

# Third Party Imports

# Local Application Imports


def get_pwd_local_dir_names():

    root = os.getcwd()
    return [
        item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))
    ]


def get_pwd_typeof_repo_names(host_path, barerepo):

    pred1, pred2 = ("true", "false") if barerepo else ("false", "true")
    repos = list()
    pwd = os.getcwd()
    os.chdir(host_path)
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
            and is_bare_repo.stdout.rstrip() == pred1
            and in_working_dir.stdout.rstrip() == pred2
        ):
            repos.append(dir)
        os.chdir("..")
    os.chdir(pwd)
    return repos
