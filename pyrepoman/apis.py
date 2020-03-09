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

    # FORMAT OF ENDPOINT: Username@IP_ADDR <-- under assumption default shell for windows is git bash, pretty sure I mean the
    # shell that openssh uses.
    # https://stackoverflow.com/questions/53834304/how-do-i-git-clone-from-a-windows-machine-over-ssh <-- setting openssh shell to bash
    # https://winscp.net/eng/docs/guide_windows_openssh_server
    # WILL USE SCRIPT TO ASSIST IN GETTING REPO NAMES AT ENDPOINT, COPY OVER SCRIPT VIA SCP

    # TODO WHAT IF USER WANTS TO DO A ENTIRELY DIFFERENT DIRECTORY? ALLOW THIS AS ANOTHER ARG TO SCRIPT?
    # TODO LIST REQUIREMENTS FOR EACH MACHINE TO PULL REPOS OFF OF, TEST THIS TO

    # OPENSSH SERVER, FIREWALL SHOULD ALLOW PORT 22
    # GIT SHOULD BE INSTALLED
    # PYTHON 3 SHOULD BE INSTALLED
    # PUBLIC KEY AUTHENTICATION ENABLED AND SET (KEYS ARE IN THE PROPER PLACE, WITH CORRECT PERMISSIONS), PASSWORD AUTH DISABLED
    # ENDS FOR LINUX

    # OPENSSH SERVER, FIREWALL SHOULD ALLOW PORT 22
    # GIT SHOULD BE INSTALLED
    # PYTHON 3 SHOULD BE INSTALLED
    # PUBLIC KEY AUTHENTICATION ENABLED AND SET (KEYS ARE IN THE PROPER PLACE, WITH CORRECT PERMISSIONS), PASSWORD AUTH DISABLED
    # IF THE USER ACCOUNT IS AN ADMIN, WILL NEED TO ADD KEY TO GLOBAL ADMIN_AUTHORIZED_KEYS
    #https://superuser.com/questions/1407020/logging-into-windows-10-openssh-server-with-administrator-account-and-public-key
    # IF USER NOT AN ADMIN, JUST NORMAL LOCATION AT HOME DIRECTORY OR DISABLE LINES IN SSHD_CONFIG FILE
    # SET OPENSSH SHELL TO BE BASH
    # ENDS FOR WINDOWS

    #COMMAND = "cd Desktop; python remote_get_repos.py;"
    POSSIBLE_PY3_INTERPRETER_NAMES = ["python", "py", "python3"]
    REMOTE_SCRIPT = 'remote_get_repos.py'
    PATH = pyrepoman_configs_select_config_value('host_path')
    if(PATH == None):
        PATH = '' # default behavior is to look at user's home directory

    # WINDOWS PATH SHOULD BE LIKE SO \\ for root, same as c:\, default is user's home directory
    # LINUX PATH SHOULD BE LIKE /usr/local/... default behavior is the same

    # HAVE NO DEPENDENCIES ON WHAT OS IS RUNNING, SO TRY WITH DIFFERENT POSSIBLE PYTHON INTERP NAMES (e.g. py, python3, python)
    # NO ERROR? COOL IT WORKED! SHOULD BE ABLE TO RECONGNIZE ERRORS

    scp_results = subprocess.run(['scp', REMOTE_SCRIPT, f"{endpoint}:{PATH}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
    for interpreter_name in POSSIBLE_PY3_INTERPRETER_NAMES:
        subprocess_OS = subprocess.run(['ssh', endpoint, f'{interpreter_name} -c "import platform; print(platform.system())"'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
        OS = subprocess_OS.stdout.strip('\n')
        if(OS == 'Windows'):
            path_on_endpoint = f"{PATH}\\{REMOTE_SCRIPT}"
        else:
            path_on_endpoint = f"{PATH}/{REMOTE_SCRIPT}"
        results_running_script = subprocess.run(['ssh', endpoint, f"{interpreter_name} {path_on_endpoint}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')
        if(results_running_script.stderr != ''):
            continue # TODO SHOULD OTHER ERRORS BE ACCOUNTED FOR?, WRITE TO LOG?
        break
    if(scp_results.stderr != '' or results_running_script.stderr != ''):
        print("Error: check logs, something went wrong with communicating with the endpoint")
        return dict() # currently, a dict is returned for correct input, empty dict is returned to gracefully exit 

    results_running_script = results_running_script.stdout.split(',') # e.g. 'cs61a_2011,cs61a_2011 - Copy\n'
    results_running_script[-1] = results_running_script[-1].strip()
    if(OS == 'Windows'):
        return {f"{dir}":f"{endpoint}:{PATH}\\{dir}" for dir in results_running_script}
    else:
        return {f"{dir}":f"{endpoint}:{PATH}/{dir}" for dir in results_running_script}

SUPPORTED_APIS = {}

add_supported_api("github", " -- github's REST API v3")
add_host_func("github", 'get_repos_and_locations', get_repos_github_restapiv3, "https://api.github.com/user/repos")