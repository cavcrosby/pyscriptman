# Standard Library Imports
import subprocess, os, shutil
from os.path import join, dirname, realpath

# Third Party Imports

# Local Application Imports
from util.printmessage import PrintMessage


def change_target_filemode_recursive(target, permissions):

    walk_root = dirname(realpath(target))

    for root, dirs, files in os.walk(target):
        walk_parent_dir = join(walk_root, root)
        for name in files:
            os.chmod(join(walk_parent_dir, name), permissions)
        for name in dirs:
            os.chmod(join(walk_parent_dir, name), permissions)
    os.chmod(target, permissions)


def git_add_commit_push(message):
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"{message}"])
    subprocess.run(["git", "push", "origin", "master"])


def get_pwd_local_dir_names():

    root = os.getcwd()
    try:
        return [
            item for item in os.listdir(root) if os.path.isdir(os.path.join(root, item))
        ]
    except PermissionError:
        raise


def get_typeof_repo_names_no_path(host_path, barerepo):

    pred1, pred2 = ("true", "false") if barerepo else ("false", "true")
    repos = list()
    pwd = os.getcwd()
    try:
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
    except PermissionError:
        raise
    except FileNotFoundError:
        raise


def copy_script_to_host(target, target_path, script):

    completed_process = subprocess.run(["scp", script, f"{target}:{target_path}"],)
    completed_process.check_returncode()


def execute_script_on_host(target, target_path, script_path):

    completed_process = subprocess.run(
        ["ssh", target, f"cd {target_path}; python3 {script_path}"],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )
    completed_process.check_returncode()
    repos = completed_process.stdout.split(",")
    repos[-1] = repos[-1].strip()  # e.g. 'repo1,repo1 - Copy\n'
    return repos


def remove_script_on_host(target, script):

    try:
        completed_process = subprocess.run(
            [
                "ssh",
                target,
                f'python3 -c "import os; path = os.path.expanduser(\\"{script}\\"); os.remove(path)"',
            ]
        )
        completed_process.check_returncode()
    except subprocess.CalledProcessError:
        PrintMessage.print_script_removal_fail(target)
        pass


def expand_target_path_on_host(target, target_path):

    completed_process = subprocess.run(
        [
            "ssh",
            target,
            f'python3 -c "import os; print(os.path.join(os.path.expanduser(\\"{target_path}\\"), \\"\\"));"',
        ],
        stderr=subprocess.PIPE,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )
    completed_process.check_returncode()
    return completed_process.stdout.rstrip()
