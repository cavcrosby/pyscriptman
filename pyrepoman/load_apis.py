# Standard Library Imports
import requests, sys # TODO REMOVE SYS WHEN NOT TESTING
import subprocess as sp

sys.path.append("/home/reap2sow1/dev/pyrepoman/test/")

# Third Party Imports

# Local Application Imports
import apis, load_local

def fetch_repos_github_restapiv3(endpoint, user, api_token, payload):

    try:
        repos = requests.get(endpoint, auth=(user, api_token), params=payload)
        return {repo['name']:repo['svn_url'] for repo in repos.json()}
    except Exception as e:
        print(e)

apis.add_supported_api("GitHub", " -- GitHub's REST API v3")
apis.add_host_func("GitHub", 'archive', fetch_repos_github_restapiv3, "https://api.github.com/user/repos")
apis.add_host_func("GitHub", 'backup', fetch_repos_github_restapiv3, "https://api.github.com/user/repos")
apis.add_host_func("GitHub", 'fetch', fetch_repos_github_restapiv3, "https://api.github.com/user/repos")