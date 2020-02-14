# Standard Library Imports
import requests
import subprocess as sp

# Third Party Imports

# Local Application Imports
import apis
from helpers import load_args, get_arg_value

def get_repos_github_restapiv3(endpoint, other_args):

    SELECT_ARGS = ['user', 'api_token', 'payload']
    data_store = load_args(SELECT_ARGS, other_args)
    user, api_token, payload = get_arg_value(data_store, 'user'), get_arg_value(data_store, 'api_token'), get_arg_value(data_store, 'payload')
    try:
        repos = requests.get(endpoint, auth=(user, api_token), params=payload)
        return {repo['name']:repo['svn_url'] for repo in repos.json()}
    except Exception as e:
        print(e)

def get_repos_local_computers(endpoint, other_args):

    # SSH Server needs to be setup for any local computer
    # FORMAT OF ENDPOINT: Username@IP_ADDR <-- under assumption default shell for windows is git bash
    # also means git needs to be installed...
    # https://stackoverflow.com/questions/53834304/how-do-i-git-clone-from-a-windows-machine-over-ssh
    # https://winscp.net/eng/docs/guide_windows_openssh_server
    # WILL USE SCRIPT TO ASSIST IN GETTING REPO NAMES AT ENDPOINT, COPY OVER SCRIPT VIA SCP
    # TODO WHAT IF USER WANTS TO DO A ENTIRELY DIFFERENT DIRECTORY? ALLOW THIS AS ANOTHER ARG TO SCRIPT?
    # TODO LIST REQUIREMENTS FOR EACH MACHINE TO PULL REPOS OFF OF
    
    # OPENSSH SERVER, FIREWALL SHOULD ALLOW PORT 22
    # PUBLIC KEY AUTHENTICATION ENABLED AND SET (KEYS ARE IN THE PROPER PLACE, WITH CORRECT PERMISSIONS), PASSWORD AUTH DISABLED
    # ENDS FOR LINUX

    # OPENSSH SERVER, FIREWALL SHOULD ALLOW PORT 22
    # PUBLIC KEY AUTHENTICATION ENABLED AND SET (KEYS ARE IN THE PROPER PLACE, WITH CORRECT PERMISSIONS), PASSWORD AUTH DISABLED
    # IF THE USER ACCOUNT IS AN ADMIN, WILL NEED TO ADD KEY TO GLOBAL ADMIN_AUTHORIZED_KEYS
    #https://superuser.com/questions/1407020/logging-into-windows-10-openssh-server-with-administrator-account-and-public-key
    # IF USER NOT AN ADMIN, JUST NORMAL LOCATION AT HOME DIRECTORY OR DISABLE LINES IN SSHD_CONFIG FILE
    # SET OPENSSH SHELL TO BE BASH


    # ENDS FOR LINUX
    # TODO FOR WINDOWS, DOES ALIAS NEED TO BE ASSIGNED TO USE COMMAND?

    HOST = endpoint
    #COMMAND = "cd Desktop; python remote_get_repos.py;"
    REMOTE_SCRIPT = 'remote_get_repos.py'

    sp.run(['scp', 'remote_get_repos.py', f"{HOST}:"])
    what_os = sp.run(['ssh', HOST, '-i', '~/.ssh/id_rsa', 'uname'], stdout=sp.PIPE, encoding='utf-8').stdout.strip('\n')
    if(what_os != 'Linux'):
        results = sp.run(['ssh', HOST, f"python {REMOTE_SCRIPT}"], stdout=sp.PIPE, encoding='utf-8')
    else:
        results = sp.run(['ssh', HOST, f"python3 {REMOTE_SCRIPT}"], stdout=sp.PIPE, encoding='utf-8')
    #results = sp.run(['ssh', HOST, '-i', '~/.ssh/id_rsa', COMMAND], stdout=sp.PIPE, encoding='utf-8')
    results = results.stdout.split(',') # 'cs61a_2011,cs61a_2011 - Copy\n' e.g.
    results[-1] = results[-1].strip()
    return {f"'{dir}'":f"'{HOST}:{dir}'" for dir in results}


