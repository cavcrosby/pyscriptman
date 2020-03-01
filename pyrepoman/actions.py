# Standard Library Imports
import os, datetime, subprocess, requests, configparser

# Third Party Imports

# Local Application Imports
import helpers
from apis import get_repo_names_and_locations, SUPPORTED_HOSTS, get_hostname_desc
from pyrepoman_configs import PYREPOMAN_CONFIGS, pyrepoman_configs_select_config_value

def update():

	repo_names = helpers.get_repo_names()
	try:
		for repo_name in repo_names:
			os.chdir(repo_name)
			subprocess.call(["git",  "pull"])
			os.chdir("..")
		print('\nand finished...!\n')
		return 1
	except Exception as e:
		print(e)
		return -1

def backup():

    BACKUP_DIR = pyrepoman_configs_select_config_value('backup_dir')
    helpers.create_dir(BACKUP_DIR)
    repo_names_and_urls = get_repo_names_and_locations()
    to_delete = os.listdir(BACKUP_DIR)
    try:
        for repo_name in repo_names_and_urls:
            backup_content = os.listdir(BACKUP_DIR)
            backup_repo_location = f"{BACKUP_DIR}/{repo_name}"
            if(not repo_name in backup_content):
                helpers.create_mirror(repo_names_and_urls[repo_name], backup_repo_location)
            else:
                helpers.update_mirror(backup_repo_location)
                to_delete.remove(repo_name)
        helpers.clear_old_repos(BACKUP_DIR, to_delete)
    except Exception as e:
        print(e)

def archive():

    BACKUP_DIR, TMP_DIR = pyrepoman_configs_select_config_value('archive_dir'), "archive_tmp"
    helpers.create_dir(BACKUP_DIR)
    helpers.create_dir(TMP_DIR)
    repo_names_and_urls = get_repo_names_and_locations()
    helpers.clearing_folder_contents(BACKUP_DIR)
    try:
        for repo_name in repo_names_and_urls:
            backup_repo_location = f"{BACKUP_DIR}/{repo_name}"
            helpers.create_mirror(repo_names_and_urls[repo_name], f"{TMP_DIR}/{repo_name}")
            helpers.create_bundle(f"{TMP_DIR}/{repo_name}", backup_repo_location)
        helpers.remove_dir(TMP_DIR)
    except Exception as e:
        print(e)

def list_web_hosts():

    for host in SUPPORTED_HOSTS:
        print(f"{host}{get_hostname_desc(host)}")

def fetch():
    
    repo_names_and_urls = get_repo_names_and_locations()
    try:
        for repo_name in repo_names_and_urls:
            subprocess.run(f"git clone {repo_names_and_urls[repo_name]} {repo_name}", shell=True)
        print('\nand finished...!\n')
        return 1
    except Exception as e:
        print(e)
        return -1