# Standard Library Imports
import os, subprocess, collections, shutil

# Third Party Imports

# Local Application Imports

def get_repo_names():
    
    try:
        repos = list()
        dirs = os.listdir(os.getcwd())
        dirs = [dir for dir in dirs if dir.find('.') == -1]
        for dir in dirs:
            os.chdir(dir)
            if('.git' in os.listdir()):
                repos.append(dir)
            os.chdir('..')
        return repos
    except Exception as e:
        print(e)

def clearing_folder_contents(loc):
    
    os.chdir(loc)
    file = os.scandir()
    try:
        while(next(file)):
            if(file.is_dir()):
                shutil.rmtree(file)
            else:
                os.remove(file)
    except StopIteration as e:
        pass
    finally:
        os.chdir('..')

def remove_dir(dir):
    
    shutil.rmtree(dir)

def dir_exist(dir_name):
    
    dir_contents = os.listdir()
    return dir_name in dir_contents

def create_dir(dir_name):

    if(not dir_exist(dir_name)):
        os.mkdir(dir_name)

def create_mirror(url, loc):
    
    subprocess.run(["git", "clone", "--mirror", url, loc], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')

def update_mirror(loc):
    
    subprocess.run(["git", "--git-dir", loc, "remote", "update"])

def clear_old_repos(backup_dir, to_delete):
    
    collections.deque(
        map(lambda repo: remove_dir(f"{backup_dir}/{repo}"), to_delete),
        maxlen=0
    )
    # collections.deque is used to prevent overhead when executing the map iterator (that is, no output should be recorded/saved).

def create_bundle(archive_dir, mirror_repo):
    
    subprocess.run(["git", "--git-dir", mirror_repo, "bundle", "create", f"{archive_dir}.bundle", "--all"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')