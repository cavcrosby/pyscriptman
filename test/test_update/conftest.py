# Standard Library Imports
import subprocess, os, platform, stat

# Third Party Imports
import pytest, toml

# Local Application Imports
from test.helpers import (
    git_add_commit_push,
    delete_folder_and_contents,
)
from test.test_variables import configholder

def load_configs(configholder, configs):

    for config, value in configs.items():
        configholder.add_config(config, value)

def pytest_runtest_setup(item):
    configs = configholder.table_func_retrieve_additional_configs(action, item.function.__name__)
    load_configs(configholder, configs)
    BARE_REPO_TO_COPY_PATH = configholder.get_config_value("BARE_REPO_TO_COPY_PATH") 
    subprocess.run(["git", "clone", BARE_REPO_TO_COPY_PATH, UPDATE_TARGET])
    subprocess.run(["git", "clone", BARE_REPO_TO_COPY_PATH, MODEL_TARGET])
    os.chdir(MODEL_TARGET)
    with open(ADDITIONAL_FILE1, "a") as f:
        f.write("testing update by adding file")
    git_add_commit_push("testing commit...")
    os.chdir("..")

def pytest_runtest_teardown(item, nextitem):
    os.chdir(MODEL_TARGET)
    os.remove(ADDITIONAL_FILE1)
    git_add_commit_push("test done, now deleting any additional files added...")
    os.chdir("..")
    delete_folder_and_contents(UPDATE_TARGET)
    delete_folder_and_contents(MODEL_TARGET)

action = "update"
configs = configholder.retrieve_table_defaults(action)
load_configs(configholder, configs)

MODEL_TARGET = configholder.get_config_value("MODEL_TARGET")
UPDATE_TARGET = configholder.get_config_value("UPDATE_TARGET")
ADDITIONAL_FILE1 = configholder.get_config_value("ADDITIONAL_FILE1")   