# Standard Library Imports
import subprocess, os, platform, stat
from os.path import expanduser

# Third Party Imports
import pytest

# Local Application Imports
from test.test_variables import configholder
from test.helpers import (
    git_add_commit_push,
    delete_folder_and_contents,
)

ACTION_IDENTIFIER = "update"


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
    BARE_REPO_TO_CLONE_PATH = expanduser(configholder.get_config_value("BARE_REPO_TO_CLONE_PATH"))
    subprocess.run(["git", "clone", BARE_REPO_TO_CLONE_PATH, UPDATE_TARGET])
    subprocess.run(["git", "clone", BARE_REPO_TO_CLONE_PATH, MODEL_TARGET])
    os.chdir(MODEL_TARGET)
    with open(ADDITIONAL_FILE1, "a") as f:
        f.write("testing update by adding file")
    git_add_commit_push("testing commit...")
    os.chdir("..")

    def normal_teardown():
        os.chdir(MODEL_TARGET)
        os.remove(ADDITIONAL_FILE1)
        git_add_commit_push("test done, now deleting any additional files added...")
        os.chdir("..")
        delete_folder_and_contents(UPDATE_TARGET)
        delete_folder_and_contents(MODEL_TARGET)

    request.addfinalizer(normal_teardown)


@pytest.fixture(scope="function")
def change_filemode_win_linux(normal_setup, request):

    target = request.param[0]
    permissions = request.param[1]
    win_permissions = request.param[2]

    filemode_binary = os.stat(target).st_mode
    if platform.system().lower() != "linux":
        os.chmod(target, win_permissions)
    else:
        os.chmod(target, permissions)

    def git_bad_permissions_teardown():
        os.chmod(target, filemode_binary)

    request.addfinalizer(git_bad_permissions_teardown)

load_init_configs()

MODEL_TARGET = configholder.get_config_value("MODEL_TARGET")
UPDATE_TARGET = configholder.get_config_value("UPDATE_TARGET")
ADDITIONAL_FILE1 = configholder.get_config_value("ADDITIONAL_FILE1")
