# Standard Library Imports
import subprocess
import os
import shutil

# Third Party Imports
import pytest

# Local Application Imports
from util.configholder import ConfigHolder
from test.conftest import (
    load_configs,
    delete_configs,
    load_init_configs,
)
from test.test_variables import (
    CONFIGURATION_FILE_NAME,
    CONFIGURATION_FILE_PATH,
)
from util.helpers import git_add_commit_push

configholder = ConfigHolder(CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH)
configholder.load_toml()

ACTION_IDENTIFIER = "update"


@pytest.fixture(scope="function")
def integration_test_setup(request):
    configs = configholder.table_func_retrieve_additional_configs(
        ACTION_IDENTIFIER, request.function.__name__
    )
    load_configs(configholder, configs)
    UPDATE_TARGET = configholder.get_config_value("UPDATE_TARGET")
    MODEL_TARGET = configholder.get_config_value("MODEL_TARGET")
    os.mkdir(MODEL_TARGET)

    def integration_test_teardown():
        os.chdir(MODEL_TARGET)
        for repo in os.listdir():
            os.chdir(repo)
            os.remove(ADDITIONAL_FILE1)
            git_add_commit_push("test done, now deleting any additional files added...")
            os.chdir("..")
        os.chdir("..")
        shutil.rmtree(UPDATE_TARGET)
        shutil.rmtree(MODEL_TARGET)
        delete_configs(configholder, configs)

    request.addfinalizer(integration_test_teardown)


@pytest.fixture(scope="function")
def unit_test_setup(request):
    configs = configholder.table_func_retrieve_additional_configs(
        ACTION_IDENTIFIER, request.function.__name__
    )
    load_configs(configholder, configs)
    os.mkdir(UPDATE_TARGET)
    os.chdir(UPDATE_TARGET)
    subprocess.run(["git", "init"])
    os.chdir("..")

    def unit_test_teardown():
        shutil.rmtree(UPDATE_TARGET)

    request.addfinalizer(unit_test_teardown)


def finish_setup():
    shutil.copytree(MODEL_TARGET, UPDATE_TARGET)
    add_additional_file()


def add_additional_file():
    os.chdir(MODEL_TARGET)
    for repo in os.listdir():
        os.chdir(repo)
        with open(ADDITIONAL_FILE1, "a") as f:
            f.write("testing update by adding file")
        git_add_commit_push("testing commit...")
        os.chdir("..")
    os.chdir("..")


load_init_configs(ACTION_IDENTIFIER, configholder)

UPDATE_TARGET = configholder.get_config_value("UPDATE_TARGET")
MODEL_TARGET = configholder.get_config_value("MODEL_TARGET")
ADDITIONAL_FILE1 = configholder.get_config_value("ADDITIONAL_FILE1")
