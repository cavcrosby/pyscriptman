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

    REPO_ROOT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip()
    REMOTE_SCRIPT = 'remote_get_dirs.py'
    PACKAGE_AND_REMOTE_SCRIPT = f'pyrepoman/{REMOTE_SCRIPT}' # currently in the pyrepoman package
    endpoint_path = pyrepoman_configs_select_config_value('host_path') # host_path really is endpoint path we are looking to manipulate repos from
    if(endpoint_path == ""):
        endpoint_path = '~/' # default behavior is to look at user's home directory
    REMOTE_SCRIPT_PATH = os.path.join(REPO_ROOT, PACKAGE_AND_REMOTE_SCRIPT)
    REMOTE_SCRIPT_ENDPOINT_PATH = f"{endpoint_path}{REMOTE_SCRIPT}"
    endpoint_path = subprocess.run(['ssh', endpoint, f'python3 -c "import os; print(os.path.expanduser(\\"{endpoint_path}\\"));"'], \
                        stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip()

    scp_results = subprocess.run(['scp', REMOTE_SCRIPT_PATH, f"{endpoint}:{endpoint_path}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
    results_running_script = subprocess.run(['ssh', endpoint, f"python3 {REMOTE_SCRIPT_ENDPOINT_PATH}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
    if(scp_results.stderr != '' or results_running_script.stderr != ''):
        print("Error apis stderr:\n" + scp_results.stderr + "\n" + results_running_script.stderr)
        return dict() # currently, a dict is returned for correct input, empty dict is returned to gracefully exit 

    subprocess.run(['ssh', endpoint, f'python3 -c "import os; path = os.path.expanduser(\\"{REMOTE_SCRIPT_ENDPOINT_PATH}\\"); os.remove(path)"'])
    results_running_script = results_running_script.stdout.split(',') # e.g. 'cs61a_2011,cs61a_2011 - Copy\n'
    results_running_script[-1] = results_running_script[-1].strip()
    return {f"{dir}":f"{endpoint}:{endpoint_path}{dir}" for dir in results_running_script}

SUPPORTED_APIS = {}

add_supported_api("github", " -- github's REST API v3")
add_host_func("github", 'get_repos_and_locations', get_repos_github_restapiv3, "https://api.github.com/user/repos")