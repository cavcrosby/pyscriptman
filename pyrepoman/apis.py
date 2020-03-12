# Standard Library Imports
import os, datetime, subprocess, configparser, requests

# Third Party Imports

# Local Application Imports
from pyrepoman_configs import pyrepoman_configs_select_config_value, PYREPOMAN_CONFIGS

def get_hostname_funcs(hostname):

    return SUPPORTED_APIS[hostname]['funcs']

def get_hostname_desc(hostname):

    return SUPPORTED_APIS[hostname]['desc']

def get_hostname_func_obj(hostname, func_action):

    return get_hostname_funcs(hostname)[func_action][0]

def get_hostname_func_endpoint(hostname, func_action):

    return get_hostname_funcs(hostname)[func_action][1]

def add_supported_api(hostname, desc):

    SUPPORTED_APIS[hostname] = {
        "funcs": {}, "desc": desc 
    }

def add_host_func(hostname, action, func_obj, endpoint):

    get_hostname_funcs(hostname)[action] = [func_obj, endpoint]

def supported_host(host):

    for supported_host in SUPPORTED_APIS:
        if(host == supported_host):
            return True
        
    return False

def get_repo_names_and_locations():
    
    func = 'get_repos_and_locations'
    host = pyrepoman_configs_select_config_value('host')
    if(host not in SUPPORTED_APIS):
        endpoint = host
        return get_repos_local_endpoint(endpoint)
    else:
        endpoint = get_hostname_func_endpoint(host, func)
        return get_hostname_func_obj(host, func)(endpoint)

def get_repos_github_restapiv3(endpoint):

    user, api_token, payload = pyrepoman_configs_select_config_value('user'), \
        pyrepoman_configs_select_config_value('api_token'), \
        pyrepoman_configs_select_config_value('payload')
    try:
        repos = requests.get(endpoint, auth=(user, api_token), params=payload)
        return {repo['name']:repo['svn_url'] for repo in repos.json()}
    except Exception as e:
        print(e)

def get_repos_local_endpoint(endpoint):

    # TODO LIST REQUIREMENTS FOR EACH MACHINE TO PULL REPOS OFF OF, TEST THIS TO

    # OPENSSH SERVER, FIREWALL SHOULD ALLOW PORT 22
    # GIT SHOULD BE INSTALLED
    # PYTHON 3 SHOULD BE INSTALLED
    # PUBLIC KEY AUTHENTICATION ENABLED AND SET (KEYS ARE IN THE PROPER PLACE, WITH CORRECT PERMISSIONS), PASSWORD AUTH DISABLED
    # ENDS FOR LINUX

    POSSIBLE_PY3_INTERPRETER_NAMES = ["python", "py", "python3"]
    results = subprocess.run(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
    REPO_DIR = results.stdout.rstrip()
    REMOTE_SCRIPT_AND_PACKAGE = 'pyrepoman/remote_get_dirs.py' # currently in the pyrepoman
    REMOTE_SCRIPT = 'remote_get_dirs.py'
    ENDPOINT_PATH = pyrepoman_configs_select_config_value('host_path')
    if(ENDPOINT_PATH == ""):
        ENDPOINT_PATH = '~/' # default behavior is to look at user's home directory
    REMOTE_SCRIPT_REPO_PATH = os.path.join(REPO_DIR, REMOTE_SCRIPT_AND_PACKAGE)
    REMOTE_SCRIPT_ENDPOINT_PATH = f"{ENDPOINT_PATH}{REMOTE_SCRIPT}"

    # LINUX PATH SHOULD BE LIKE /usr/local/... default behavior is the same

    # HAVE NO DEPENDENCIES ON WHAT OS IS RUNNING, SO TRY WITH DIFFERENT POSSIBLE PYTHON INTERP NAMES (e.g. py, python3, python)
    # NO ERROR? COOL IT WORKED! SHOULD BE ABLE TO RECONGNIZE ERRORS

    scp_results = subprocess.run(['scp', REMOTE_SCRIPT_REPO_PATH, f"{endpoint}:{ENDPOINT_PATH}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
    for interpreter_name in POSSIBLE_PY3_INTERPRETER_NAMES:
        results_running_script = subprocess.run(['ssh', endpoint, f"{interpreter_name} {REMOTE_SCRIPT_ENDPOINT_PATH}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
        if(results_running_script.stderr != ''):
            continue
        break
    if(scp_results.stderr != '' or results_running_script.stderr != ''):
        print("Error apis stderr:\n" + scp_results.stderr + "\n" + results_running_script.stderr)
        return dict() # currently, a dict is returned for correct input, empty dict is returned to gracefully exit 

    subprocess.run(['ssh', endpoint, f'{interpreter_name} -c "import os; path = os.path.expanduser(\\"{REMOTE_SCRIPT_ENDPOINT_PATH}\\"); os.remove(path)"'])
    results_running_script = results_running_script.stdout.split(',') # e.g. 'cs61a_2011,cs61a_2011 - Copy\n'
    results_running_script[-1] = results_running_script[-1].strip()
    return {f"{dir}":f"{endpoint}:{ENDPOINT_PATH}{dir}" for dir in results_running_script}

SUPPORTED_APIS = {}

add_supported_api("github", " -- github's REST API v3")
add_host_func("github", 'get_repos_and_locations', get_repos_github_restapiv3, "https://api.github.com/user/repos")