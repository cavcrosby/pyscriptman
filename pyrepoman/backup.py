# Standard Library Imports
import os, datetime, subprocess, requests, smtplib, configparser, collections

# Third Party Imports

# Local Application Imports
import apis, helpers

def dir_exist(dir_name):
    dir_contents = os.listdir()
    return dir_name in dir_contents

def create_dir(dir_name):
    subprocess.run(["mkdir", dir_name])

def create_mirror(url, loc):
    subprocess.run(["git", "clone", "--mirror", url, loc])

def update_mirror(loc):
    subprocess.run(["git", "--git-dir", loc, "remote", "update"])

def clear_old_repos(to_delete):
    collections.deque(
        map(lambda repo: subprocess.run(["rm", "-rf", f"{BACKUP_DIR}/{repo}"]), to_delete),
        maxlen=0
    )
    # collections.deque is used to prevent overhead when executing the map iterator (that is, no output should be recorded/saved).

def remove_from_to_delete(to_delete, repo_name):
    to_delete.remove(repo_name)

def load_args(args):


	global USER, API_TOKEN, PAYLOAD, BACKUP_DIR, HOST
	USER, API_TOKEN, PAYLOAD, BACKUP_DIR, HOST = [helpers.get_arg_value(arg) for arg in args]

def init_backup_dir():

    if(not dir_exist(BACKUP_DIR)):
        create_dir(BACKUP_DIR)

def main(args):
    load_args(args)
    init_backup_dir()
    repo_names_and_urls = helpers.get_repo_names_and_urls(HOST, 'backup', USER, API_TOKEN, PAYLOAD)
    to_delete = os.listdir(BACKUP_DIR)
    for repo_name in repo_names_and_urls:
        backup_content = os.listdir(BACKUP_DIR)
        backup_repo_location = f"{BACKUP_DIR}/{repo_name}"
        if(not repo_name in backup_content):
            create_mirror(repo_names_and_urls[repo_name], backup_repo_location)
        else:
            update_mirror(backup_repo_location)
            remove_from_to_delete(to_delete, repo_name)
    clear_old_repos(to_delete) # TODO should error handling be added?