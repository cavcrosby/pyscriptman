# Standard Library Imports
import os, subprocess, collections

# Third Party Imports

# Local Application Imports
import apis

def get_repo_names():

	try:
		repos = os.listdir(os.getcwd())
		return [repo for repo in repos if repo.find('.') == -1]
	except Exception as e:
		print(e)

def get_value(store, arg):

    return store[arg]

def load_args(select_args, args):

    to_return = dict()
    for arg in args:
        if arg[0] in select_args:
            to_return[arg[0]] = arg[1]
    
    return to_return

def get_repo_names_and_urls(host, action, other_args):
	
	endpoint = apis.get_hostname_func_endpoint(host, action)
	return apis.get_hostname_func_obj(host, action)(endpoint, other_args)

def clear_old_bundles(loc):

    subprocess.run(["rm", "-rf", "{0}/*".format(loc)])

def remove_dir(dir):

    subprocess.run(["rm", "-rf", dir])

def init_backup_dir(directory):

    if(not dir_exist(directory)):
        create_dir(directory)

def dir_exist(dir_name):

    dir_contents = os.listdir()
    return dir_name in dir_contents

def create_dir(dir_name):

    subprocess.run(["mkdir", dir_name])

def create_mirror(url, loc):

    subprocess.run(["git", "clone", "--mirror", url, loc])

def update_mirror(loc):

    subprocess.run(["git", "--git-dir", loc, "remote", "update"])

def clear_old_repos(backup_dir, to_delete):

    collections.deque(
        map(lambda repo: remove_dir(f"{backup_dir}/{repo}"), to_delete),
        maxlen=0
    )
    # collections.deque is used to prevent overhead when executing the map iterator (that is, no output should be recorded/saved).

def create_bundle(mirror_repo, archive_dir):

    subprocess.run(["git", "--git-dir", mirror_repo, "bundle", "create", f"{archive_dir}.bundle", "--all"])

def not_supported_host(host):
	
	if(not apis.supported_endpoint(host)):
		print("Error: web host passed in is not currently supported")
		return True