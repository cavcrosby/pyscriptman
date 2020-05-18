# Standard Library Imports
import subprocess, os, platform, shutil
from os.path import expanduser, join, basename

# Third Party Imports
import pytest, requests

# Local Application Imports
from util.githubauth import GitHubAuth
from pyrepoman.hosts.localhost import LocalHost
from pyrepoman.hosts.webhosts.github import GitHub
from global_variables import (
    REMOTE_SCRIPT_GET_BARE_REPOS_PATH,
    REMOTE_SCRIPT_GET_BARE_REPOS_NAME,
)
from util.helpers import (
    get_typeof_repo_names_no_path,
    copy_script_to_host,
    execute_script_on_host,
    expand_target_path_on_host,
    remove_script_on_host,
)


def load_configs(configholder, configs):

    for config_name, value in configs.items():
        configholder.add_config(config_name, value)


def delete_configs(configholder, configs):

    for config_name in configs:
        configholder.delete_config(config_name)


def load_init_configs(ACTION_IDENTIFIER, configholder):

    configs = configholder.retrieve_table_defaults("test")
    load_configs(configholder, configs)

    configs = configholder.retrieve_table_defaults(ACTION_IDENTIFIER)
    load_configs(configholder, configs)


def generate_localhost(configholder):

    # see localhost constructor, as it is expecting a configuration called 'path'
    target_path = expanduser(configholder.get_config_value("LOCAL_BARE_REPOS_DIR_PATH"))
    configholder.add_config("path", target_path)
    return LocalHost(configholder)


def generate_github_host(configholder):

    # see github constructor, as it is currently expecting the following configurations
    configholder.add_config("repo_type", GitHub.DEFAULT_REPO_TYPE_OWN)
    configholder.add_config("repo_owner_type", GitHub.OWN_CMD_ARG_NAME)
    configholder.add_config("username", configholder.get_config_value("GITHUB_NAME"))

    return GitHub(configholder)


def fake_get_user_repo_names_and_locations(self):

    self._get_user_repo_names_and_locations()


@pytest.fixture(scope="function")
def localhost_setup(request, integration_test_setup):
    git_command = request.param[0]
    configholder = request.param[1]
    target = request.param[2]
    get_localhost_repos(git_command, configholder, target)


@pytest.fixture(scope="function")
def remotehost_setup(request, integration_test_setup):
    git_command = request.param[0]
    configholder = request.param[1]
    target = request.param[2]
    get_remotehost_repos(git_command, configholder, target)


@pytest.fixture(scope="function")
def github_setup(request, integration_test_setup):
    repo_owner_type = request.param[0]
    repo_type = request.param[1]
    git_command = request.param[2]
    configholder = request.param[3]
    target = request.param[4]
    return get_github_repos(
        repo_owner_type, repo_type, git_command, configholder, target
    )


@pytest.fixture(scope="function")
def filemode_change_setup_win_linux(request, unit_test_setup):
    target = request.param[0]
    permissions = request.param[1]
    win_permissions = request.param[2]
    filemode_binary = os.stat(target).st_mode
    if platform.system().lower() != "linux":
        os.chmod(target, win_permissions)
    else:
        os.chmod(target, permissions)

    def filemode_change_teardown():
        os.chmod(target, filemode_binary)

    request.addfinalizer(filemode_change_teardown)


def get_localhost_repos(git_command, configholder, dest):
    os.chdir(dest)
    BARE_REPOS_DIR_PATH = expanduser(
        configholder.get_config_value("LOCAL_BARE_REPOS_DIR_PATH")
    )
    bare_repos = get_typeof_repo_names_no_path(BARE_REPOS_DIR_PATH, True)
    for bare_repo_name in bare_repos:
        git_command(join(BARE_REPOS_DIR_PATH, bare_repo_name), bare_repo_name)
    os.chdir("..")


def get_remotehost_repos(git_command, configholder, dest):
    os.chdir(dest)
    REMOTE_USER = configholder.get_config_value("REMOTE_USER")
    REMOTE_ADDR = configholder.get_config_value("REMOTE_ADDR")
    REMOTE_BARE_REPOS_DIR_PATH = configholder.get_config_value(
        "REMOTE_BARE_REPOS_DIR_PATH"
    )
    target = f"{REMOTE_USER}@{REMOTE_ADDR}"
    target_path = expand_target_path_on_host(target, REMOTE_BARE_REPOS_DIR_PATH)
    remote_script_target_path = (
        f"{REMOTE_BARE_REPOS_DIR_PATH}{REMOTE_SCRIPT_GET_BARE_REPOS_NAME}"
    )
    copy_script_to_host(target, target_path, REMOTE_SCRIPT_GET_BARE_REPOS_PATH)
    bare_repos = execute_script_on_host(target, target_path, remote_script_target_path)
    remove_script_on_host(target, remote_script_target_path)
    for bare_repo_name in bare_repos:
        git_command(join(f"{target}:{target_path}", bare_repo_name), bare_repo_name)
    os.chdir("..")


def get_github_repos(repo_owner_type, repo_type, git_command, configholder, dest):
    os.chdir(dest)
    username = configholder.get_config_value("GITHUB_NAME")
    url = (
        "https://api.github.com/user/repos"
        if repo_owner_type == GitHub.OWN_CMD_ARG_NAME
        else f"https://api.github.com/users/{username}/repos"
    )
    auth = GitHubAuth(configholder.get_config_value("GITHUB_API_TOKEN"))
    response = requests.get(url, auth=auth, params={"type": repo_type})
    for repo in response.json():
        git_command(repo["svn_url"], repo["name"])
    os.chdir("..")

    return (repo_owner_type, repo_type)
