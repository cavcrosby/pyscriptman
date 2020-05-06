# Standard Library Imports
import subprocess, os, platform, stat
from os.path import expanduser

# Third Party Imports
import pytest, requests

# Local Application Imports
from test.test_variables import configholder
from util.githubauth import GitHubAuth
from test.helpers import (
    git_add_commit_push,
    delete_folder_and_contents,
)

ACTION_IDENTIFIER = "fetch"


def load_configs(configholder, configs):

    for config_name, value in configs.items():
        configholder.add_config(config_name, value)

def load_init_configs():

    configs = configholder.retrieve_table_defaults(ACTION_IDENTIFIER)
    load_configs(configholder, configs)

@pytest.fixture(scope="function")
def normal_setup(request):
    configs = configholder.table_func_retrieve_additional_configs(
        ACTION_IDENTIFIER, request.function.__name__
    )
    load_configs(configholder, configs)
    os.mkdir(FETCH_TARGET)
    os.mkdir(MODEL_TARGET)
    os.chdir(MODEL_TARGET)
    BARE_REPOS_TO_CLONE_PATHS = configholder.get_config_value("BARE_REPOS_TO_CLONE_PATHS")
    for bare_repo in BARE_REPOS_TO_CLONE_PATHS:
        subprocess.run(['git', 'clone', expanduser(bare_repo)])
    os.chdir('..')

    def normal_teardown():
        delete_folder_and_contents(FETCH_TARGET)
        delete_folder_and_contents(MODEL_TARGET)

    request.addfinalizer(normal_teardown)


@pytest.fixture(scope="function")
def github_setup(request):
    configs = configholder.table_func_retrieve_additional_configs(
        ACTION_IDENTIFIER, request.function.__name__
    )
    load_configs(configholder, configs)
    repo_owner_type = request.param[0]
    username = request.param[1]
    repo_type = request.param[2]
    os.mkdir(FETCH_TARGET)
    os.mkdir(MODEL_TARGET)
    os.chdir(MODEL_TARGET)
    url = (
        "https://api.github.com/user/repos"
        if repo_owner_type == "own"
        else f"https://api.github.com/users/{username}/repos"
    )
    auth = (
        GitHubAuth(configholder.get_config_value("api_token"))
        if repo_owner_type == "own"
        else None
    )
    response = requests.get(url, auth=auth, params={"type": repo_type})
    for repo in response.json():
        subprocess.run(['git', 'clone', repo["svn_url"], repo["name"]])
    os.chdir("..")

    def git_bad_permissions_teardown():
        delete_folder_and_contents(FETCH_TARGET)
        delete_folder_and_contents(MODEL_TARGET)

    request.addfinalizer(git_bad_permissions_teardown)
    return (repo_owner_type, username, repo_type)


load_init_configs()

MODEL_TARGET = configholder.get_config_value("MODEL_TARGET")
FETCH_TARGET = configholder.get_config_value("FETCH_TARGET")
