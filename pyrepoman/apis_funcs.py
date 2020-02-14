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
