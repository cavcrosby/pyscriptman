# Standard Library Imports
import os, datetime, subprocess, requests, configparser

# Third Party Imports

# Local Application Imports
import helpers
from helpers import load_args, get_arg_value, create_dir
from apis import get_repo_names_and_locations, SUPPORTED_HOSTS, get_hostname_desc

def update(args):

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

def backup(args):

    SELECT_ARGS = ['where', 'backup_dir']
    # TODO, HOW TO DEAL WITH EXTRA ARGS FOR LOCAL COMPUTERS?
    data_store = load_args(SELECT_ARGS, args)
    BACKUP_DIR = get_arg_value(data_store, 'backup_dir')
    create_dir(BACKUP_DIR)
    repo_names_and_urls = get_repo_names_and_locations(get_arg_value(data_store, 'where'), args)
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

def archive(args):

    SELECT_ARGS = ['where', 'backup_dir', 'tmp_dir']
    # TODO, HOW TO DEAL WITH EXTRA ARGS FOR LOCAL COMPUTERS?
    data_store = load_args(SELECT_ARGS, args)
    BACKUP_DIR, TMP_DIR = get_arg_value(data_store, 'backup_dir'), get_arg_value(data_store, 'tmp_dir')
    create_dir(BACKUP_DIR)
    create_dir(TMP_DIR)
    repo_names_and_urls = get_repo_names_and_locations(get_arg_value(data_store, 'where'), args)
    helpers.clearing_folder_contents(BACKUP_DIR)
    try:
        for repo_name in repo_names_and_urls:
            backup_repo_location = f"{BACKUP_DIR}/{repo_name}"
            helpers.create_mirror(repo_names_and_urls[repo_name], f"{TMP_DIR}/{repo_name}")
            helpers.create_bundle(f"{TMP_DIR}/{repo_name}", backup_repo_location)
        helpers.remove_dir(TMP_DIR)
    except Exception as e:
        print(e)

def list_web_hosts(args):

    for host in SUPPORTED_HOSTS:
        print(f"{host}{get_hostname_desc(host)}")

def fetch(args):
    
    SELECT_ARGS = ['host']
    data_store = load_args(SELECT_ARGS, args)
    repo_names_and_urls = get_repo_names_and_locations(get_arg_value(data_store, 'host'), args)
    try:
        for repo_name in repo_names_and_urls:
            subprocess.run("git clone {0} {1}".format(repo_names_and_urls[repo_name], repo_name), shell=True)
        print('\nand finished...!\n')
        return 1
    except Exception as e:
        print(e)
        return -1