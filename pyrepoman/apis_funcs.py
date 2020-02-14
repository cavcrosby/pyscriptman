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
    # FORMAT OF ENDPOINT: Username@IP_ADDR:/c/Users/xxx/Desktop/foo <-- under assumption default shell for windows is git bash
    # also means git needs to be installed...
    # TODO FIGURE OUT IF CAN RUN PYTHON CODE ON REMOTE SERVERS, TO FIND OUT WHAT DIRS ARE GIT DIRS
    # https://stackoverflow.com/questions/53834304/how-do-i-git-clone-from-a-windows-machine-over-ssh
    # https://winscp.net/eng/docs/guide_windows_openssh_server

