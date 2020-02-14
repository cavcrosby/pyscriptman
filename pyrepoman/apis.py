# Standard Library Imports
import os, datetime, subprocess, configparser

# Third Party Imports

# Local Application Imports
import apis_funcs

def get_hostname_funcs(hostname):

    return SUPPORTED_HOSTS[hostname]['funcs']

def get_hostname_func_obj(hostname, func_action):

    return SUPPORTED_HOSTS[hostname]['funcs'][func_action][0]

def get_hostname_func_endpoint(hostname, func_action):

    return SUPPORTED_HOSTS[hostname]['funcs'][func_action][1]

def get_hostname_desc(hostname):

    return SUPPORTED_HOSTS[hostname]['desc']

def add_supported_api(hostname, desc):

    SUPPORTED_HOSTS[hostname] = {
        "funcs": {}, "desc": desc 
    }

def add_host_func(hostname, action, func_obj, endpoint):

    get_hostname_funcs(hostname)[action] = [func_obj, endpoint]

def supported_endpoint(host):

    for supported_host in SUPPORTED_HOSTS:
        if(host == supported_host):
            return True
        
    return False

def get_repo_names_and_locations(host, other_args):
    
    action = 'get_repos_and_locations'
    if(host not in SUPPORTED_HOSTS):
        endpoint = host
        host = 'local_computer'
    else:
        endpoint = get_hostname_func_endpoint(host, action)
    return get_hostname_func_obj(host, action)(endpoint, other_args)

SUPPORTED_HOSTS = {}

add_supported_api("GitHub", " -- GitHub's REST API v3")
add_host_func("GitHub", 'get_repos_and_locations', apis_funcs.get_repos_github_restapiv3, "https://api.github.com/user/repos")

add_supported_api("local_computer", " -- linux and windows directories are supported for actions, see docs")