# Standard Library Imports
import requests, sys # TODO REMOVE SYS WHEN NOT TESTING
import subprocess as sp

sys.path.append("/home/reap2sow1/dev/pyrepoman/test/")

# Third Party Imports

# Local Application Imports
import apis, load_local
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

apis.add_supported_api("GitHub", " -- GitHub's REST API v3")
apis.add_host_func("GitHub", 'get_repos_and_locations', get_repos_github_restapiv3, "https://api.github.com/user/repos")