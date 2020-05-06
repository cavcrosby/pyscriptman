# Standard Library Imports
import subprocess, os, shutil
from os.path import join, dirname, realpath

# Third Party Imports

# Local Application Imports


def delete_folder_and_contents(dir):
    os.chdir(dir)
    nodes = os.scandir()
    try:
        dir_entry = nodes.__next__()
        while dir_entry:
            if dir_entry.is_dir():
                shutil.rmtree(dir_entry)
                dir_entry = nodes.__next__()
            else:
                os.remove(dir_entry)
                dir_entry = nodes.__next__()
    except StopIteration:
        pass
    finally:
        os.chdir("..")
        os.rmdir(dir)


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
