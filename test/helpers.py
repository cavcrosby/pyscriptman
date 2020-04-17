# Standard Library Imports
import subprocess, os, shutil

# Third Party Imports

# Local Application Imports

def delete_folder_and_contents(dir):
    os.chdir(dir)
    nodes = os.scandir()
    dir_entry = nodes.__next__()
    try:
        while(dir_entry):
            if(dir_entry.is_dir()):
                shutil.rmtree(dir_entry)
                dir_entry = nodes.__next__()
            else:
                os.remove(dir_entry)
                dir_entry = nodes.__next__()
    except StopIteration as e:
        pass
    finally:
        os.chdir('..')
        os.rmdir(dir)

def git_add_commit_push(message):
    subprocess.run(['git', 'add', '.'])
    subprocess.run(['git', 'commit', '-m', f"{message}"])
    subprocess.run(['git', 'push', 'origin', 'master'])