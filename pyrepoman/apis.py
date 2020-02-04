# Standard Library Imports
import os, datetime, subprocess, requests, configparser

# Third Party Imports

# Local Application Imports

def get_hostname_funcs(hostname):

    return SUPPORTED_HOSTS[hostname]['funcs']

def get_hostname_module_func(hostname, module_action):

    return SUPPORTED_HOSTS[hostname]['funcs'][module_action][0]

def get_hostname_module_func_api(hostname, module_action):

    return SUPPORTED_HOSTS[hostname]['funcs'][module_action][1]

def get_hostname_desc(hostname):

    return SUPPORTED_HOSTS[hostname]['desc']

def supported_endpoint(HOST):

    for supported_host in SUPPORTED_HOSTS:
        if(HOST == supported_host):
            return True
        
    return False

def fetch_repos_github_restapiv3(endpoint, user, api_token, payload):

    try:
        repos = requests.get(endpoint, auth=(user, api_token), params=payload)
        return {repo['name']:repo['svn_url'] for repo in repos.json()}
    except Exception as e:
        print(e)

SUPPORTED_HOSTS = {
    "GitHub": 
        {"funcs": 
            {"fetch": [fetch_repos_github_restapiv3, "https://api.github.com/user/repos"],
            "backup": [fetch_repos_github_restapiv3, "https://api.github.com/user/repos"],
            "archive": [fetch_repos_github_restapiv3, "https://api.github.com/user/repos"]}, 
        "desc": " -- GitHub's REST API v3"}
}