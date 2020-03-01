# Standard Library Imports
import requests
import subprocess as sp

# Third Party Imports

# Local Application Imports
import apis
from pyrepoman_configs import pyrepoman_configs_select_config_value

def get_repos_github_restapiv3(endpoint):

    user, api_token, payload = pyrepoman_configs_select_config_value('user'), \
        pyrepoman_configs_select_config_value('api_token'), \
        pyrepoman_configs_select_config_value('payload')
    try:
        repos = requests.get(endpoint, auth=(user, api_token), params=payload)
        return {repo['name']:repo['svn_url'] for repo in repos.json()}
    except Exception as e:
        print(e)

def get_repos_local_computers(endpoint):

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
    REMOTE_SCRIPT = 'remote_get_repos.py'
    PATH = pyrepoman_configs_select_config_value('path')
    if(PATH == None):
        PATH = '~' # default behavior is to look at user's home directory

    sp.run(['scp', 'remote_get_repos.py', f"{endpoint}:{PATH}"])
    what_os = sp.run(['ssh', endpoint, '-i', '~/.ssh/id_rsa', 'uname'], stdout=sp.PIPE, encoding='utf-8').stdout.strip('\n')
    if(what_os != 'Linux'):
        results = sp.run(['ssh', endpoint, fr"python {PATH}\{REMOTE_SCRIPT}"], stdout=sp.PIPE, encoding='utf-8')
    else:
        results = sp.run(['ssh', endpoint, f"python3 {PATH}/{REMOTE_SCRIPT}"], stdout=sp.PIPE, encoding='utf-8')
    #results = sp.run(['ssh', endpoint, '-i', '~/.ssh/id_rsa', COMMAND], stdout=sp.PIPE, encoding='utf-8')
    results = results.stdout.split(',') # 'cs61a_2011,cs61a_2011 - Copy\n' e.g.
    results[-1] = results[-1].strip()
    return {f"'{dir}'":f"'{endpoint}:{dir}'" for dir in results}


