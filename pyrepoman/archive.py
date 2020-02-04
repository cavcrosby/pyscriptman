# Standard Library Imports
import subprocess

# Third Party Imports

# Local Application Imports
import apis, helpers, backup

TMP_DIR = "./backup_tmp"

def clear_old_bundles(loc):
    subprocess.run(["rm", "-rf", "{0}/*".format(loc)])

def create_bundle(mirror_repo, archive_dir):
    subprocess.run(["git", "--git-dir", mirror_repo, "bundle", "create", f"{archive_dir}.bundle", "--all"])

def load_args(args):


	global USER, API_TOKEN, PAYLOAD, BACKUP_DIR, HOST
	USER, API_TOKEN, PAYLOAD, BACKUP_DIR, HOST = [helpers.get_arg_value(arg) for arg in args]

def remove_tmp_dir():
    subprocess.run(["rm", "-rf", f"{TMP_DIR}"])

def init_backup_dir():

    if(not backup.dir_exist(BACKUP_DIR)):
        backup.create_dir(BACKUP_DIR)
    
    if(not backup.dir_exist(TMP_DIR)):
        backup.create_dir(TMP_DIR)

def main(args):
    load_args(args)
    init_backup_dir()
    repo_names_and_urls = helpers.get_repo_names_and_urls(HOST, 'archive', USER, API_TOKEN, PAYLOAD)
    clear_old_bundles(BACKUP_DIR)
    for repo_name in repo_names_and_urls:
        backup_repo_location = f"{BACKUP_DIR}/{repo_name}"
        backup.create_mirror(repo_names_and_urls[repo_name], f"{TMP_DIR}/{repo_name}")
        create_bundle(f"{TMP_DIR}/{repo_name}", backup_repo_location)
    remove_tmp_dir()