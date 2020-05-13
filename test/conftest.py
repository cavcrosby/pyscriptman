# Standard Library Imports
import subprocess, os
from os.path import expanduser, join

# Third Party Imports
import pytest, requests

# Local Application Imports
from util.githubauth import GitHubAuth
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


@pytest.fixture(scope="function")
def localhost_setup(request, normal_setup):
    git_command = request.param[0]
    configholder = request.param[1]
    target = request.param[2]
    get_localhost_repos(git_command, configholder, target)


@pytest.fixture(scope="function")
def remotehost_setup(request, normal_setup):
    git_command = request.param[0]
    configholder = request.param[1]
    target = request.param[2]
    get_remotehost_repos(git_command, configholder, target)


@pytest.fixture(scope="function")
def github_setup(request, normal_setup):
    repo_owner_type = request.param[0]
    repo_type = request.param[1]
    git_command = request.param[2]
    configholder = request.param[3]
    target = request.param[4]
    return get_github_repos(
        repo_owner_type, repo_type, git_command, configholder, target
    )


def get_localhost_repos(git_command, configholder, target):
    os.chdir(target)
    bare_repos_path = expanduser(configholder.get_config_value("BARE_REPOS_DIR"))
    bare_repos = get_typeof_repo_names_no_path(bare_repos_path, True)
    for bare_repo in bare_repos:
        git_command(bare_repos_path, bare_repo)
    os.chdir("..")


def get_remotehost_repos(git_command, configholder, target):
    os.chdir(target)
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
        git_command(bare_repo)
    os.chdir("..")


def get_github_repos(repo_owner_type, repo_type, git_command, configholder, target):
    os.chdir(target)
    username = configholder.get_config_value("GITHUB_NAME")
    url = (
        "https://api.github.com/user/repos"
        if repo_owner_type == "own"
        else f"https://api.github.com/users/{username}/repos"
    )
    auth = GitHubAuth(configholder.get_config_value("API_TOKEN"))
    response = requests.get(url, auth=auth, params={"type": repo_type})
    for repo in response.json():
        git_command(repo)
    os.chdir("..")

    return (repo_owner_type, repo_type)


def localhost_clone_repo(repo_path, repo):

    subprocess.run(["git", "clone", join(repo_path, repo)])


def remotehost_clone_repo(repo):

    subprocess.run(["git", "clone", expanduser(repo)])


def github_clone_repo(repo):

    subprocess.run(["git", "clone", repo["svn_url"], repo["name"]])
