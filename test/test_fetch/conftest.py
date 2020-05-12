# Standard Library Imports
import subprocess, os
from os.path import expanduser, join

# Third Party Imports
import pytest, requests

# Local Application Imports
from util.configholder import ConfigHolder
from util.githubauth import GitHubAuth
from test.test_variables import (
    CONFIGURATION_FILE_NAME,
    CONFIGURATION_FILE_PATH,
)
from global_variables import (
    ROOT_DIR,
    REMOTE_SCRIPT_GET_BARE_REPOS_PATH,
    REMOTE_SCRIPT_GET_BARE_REPOS_NAME,
)
from util.helpers import (
    git_add_commit_push,
    delete_folder_and_contents,
    get_typeof_repo_names_no_path,
    copy_script_to_host,
    execute_script_on_host,
    expand_target_path_on_host,
    remove_script_on_host,
)

configholder = ConfigHolder(CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH)
configholder.load_toml()

ACTION_IDENTIFIER = "fetch"


def load_configs(configholder, configs):

    for config_name, value in configs.items():
        configholder.add_config(config_name, value)


def delete_configs(configholder, configs):

    for config_name in configs:
        configholder.delete_config(config_name)


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

    def normal_teardown():
        os.chdir(ROOT_DIR)
        delete_folder_and_contents(FETCH_TARGET)
        delete_folder_and_contents(MODEL_TARGET)
        delete_configs(configholder, configs)

    request.addfinalizer(normal_teardown)


@pytest.fixture(scope="function")
def localhost_setup(request, normal_setup):
    bare_repos_path = expanduser(configholder.get_config_value("BARE_REPOS_DIR"))
    bare_repos = get_typeof_repo_names_no_path(bare_repos_path, True)
    for bare_repo in bare_repos:
        subprocess.run(["git", "clone", join(bare_repos_path, bare_repo)])
    os.chdir("..")


@pytest.fixture(scope="function")
def remotehost_setup(request, normal_setup):
    REMOTE_USER = configholder.get_config_value("REMOTE_USER")
    REMOTE_ADDR = configholder.get_config_value("REMOTE_ADDR")
    REMOTE_BARE_REPOS_DIR = configholder.get_config_value("REMOTE_BARE_REPOS_DIR")
    target = f"{REMOTE_USER}@{REMOTE_ADDR}"
    target_path = expand_target_path_on_host(target, REMOTE_BARE_REPOS_DIR)
    remote_script_target_path = (
        f"{REMOTE_BARE_REPOS_DIR}{REMOTE_SCRIPT_GET_BARE_REPOS_NAME}"
    )
    copy_script_to_host(target, target_path, REMOTE_SCRIPT_GET_BARE_REPOS_PATH)
    bare_repos = execute_script_on_host(target, remote_script_target_path)
    remove_script_on_host(target, remote_script_target_path)
    for bare_repo in bare_repos:
        subprocess.run(["git", "clone", expanduser(bare_repo)])
    os.chdir("..")


@pytest.fixture(scope="function")
def github_setup(request):
    configs = configholder.table_func_retrieve_additional_configs(
        ACTION_IDENTIFIER, request.function.__name__
    )
    load_configs(configholder, configs)
    repo_owner_type = request.param[0]
    repo_type = request.param[1]
    username = configholder.get_config_value("GITHUB_NAME")
    os.mkdir(FETCH_TARGET)
    os.mkdir(MODEL_TARGET)
    os.chdir(MODEL_TARGET)
    url = (
        "https://api.github.com/user/repos"
        if repo_owner_type == "own"
        else f"https://api.github.com/users/{username}/repos"
    )
    auth = GitHubAuth(configholder.get_config_value("API_TOKEN"))
    response = requests.get(url, auth=auth, params={"type": repo_type})
    for repo in response.json():
        subprocess.run(["git", "clone", repo["svn_url"], repo["name"]])
    os.chdir("..")

    def git_setup_teardown():
        delete_folder_and_contents(FETCH_TARGET)
        delete_folder_and_contents(MODEL_TARGET)

    request.addfinalizer(git_setup_teardown)
    return (repo_owner_type, repo_type)


load_init_configs()

MODEL_TARGET = configholder.get_config_value("MODEL_TARGET")
FETCH_TARGET = configholder.get_config_value("FETCH_TARGET")
