# Standard Library Imports
import os, datetime, subprocess, requests, configparser

# Third Party Imports

# Local Application Imports

def get_endpoint_funcs(endpoint):

    return SUPPORTED_APIS[endpoint]['funcs']

def get_endpoint_module_func(endpoint, module_action):

    return SUPPORTED_APIS[endpoint]['funcs'][module_action]

def get_endpoint_desc(endpoint):

    return SUPPORTED_APIS[endpoint]['desc']

def fetch_repos_github_restapiv3(endpoint, user, api_token, payload):

    try:
        repos = requests.get(endpoint, auth=(user, api_token), params=payload)
        return {repo['name']:repo['svn_url'] for repo in repos.json()}
    except Exception as e:
        print(e)

SUPPORTED_APIS = {
    "https://api.github.com/user/repos": 
        {"funcs": {"fetch": fetch_repos_github_restapiv3}, "desc": " -- GitHub's REST API v3"}
}