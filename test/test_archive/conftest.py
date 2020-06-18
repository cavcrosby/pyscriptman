# Standard Library Imports
import os
import shutil
import subprocess
import filecmp
from os.path import join

# Third Party Imports
import pytest

# Local Application Imports
from util.configholder import ConfigHolder
from util.diff import Diff
from global_variables import ROOT_DIR
from test.test_variables import (
    CONFIGURATION_FILE_NAME,
    CONFIGURATION_FILE_PATH,
)
from test.conftest import (
    load_configs,
    delete_configs,
    load_init_configs,
)

configholder = ConfigHolder(CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH)
configholder.load_toml()

ACTION_IDENTIFIER = "archive"


def diff_bundle_contents():
    """Used to compare differences of contents in 'bundles'"""
    dir_package = os.listdir(ARCHIVE_TARGET)
    dir_setup = os.listdir(MODEL_TARGET)
    if dir_package != dir_setup:
        return True
    for bundle in dir_package:
        os.chdir(ARCHIVE_TARGET)
        subprocess.run(["git", "clone", bundle])
        os.chdir("..")
        os.chdir(MODEL_TARGET)
        subprocess.run(["git", "clone", bundle])
        os.chdir("..")
        dcmp = filecmp.dircmp(
            join(ARCHIVE_TARGET, bundle[: bundle.find(".bundle")]),
            join(MODEL_TARGET, bundle[: bundle.find(".bundle")]),
        )
        diff = Diff(dcmp)
        if diff.run():
            return True
    return False


@pytest.fixture(scope="function")
def integration_test_setup(request):
    """To setup a mock environment for integration tests."""
    configs = configholder.table_func_retrieve_additional_configs(
        ACTION_IDENTIFIER, request.function.__name__
    )
    load_configs(configholder, configs)
    os.mkdir(ARCHIVE_TARGET)
    os.mkdir(MODEL_TARGET)

    def integration_test_teardown():
        os.chdir(ROOT_DIR)
        shutil.rmtree(ARCHIVE_TARGET)
        shutil.rmtree(MODEL_TARGET)
        delete_configs(configholder, configs)

    request.addfinalizer(integration_test_teardown)


@pytest.fixture(scope="function")
def unit_test_setup(request):
    """To setup a mock environment for unit tests."""
    configs = configholder.table_func_retrieve_additional_configs(
        ACTION_IDENTIFIER, request.function.__name__
    )
    load_configs(configholder, configs)
    os.mkdir(ARCHIVE_TARGET)

    def unit_test_teardown():
        shutil.rmtree(ARCHIVE_TARGET)

    request.addfinalizer(unit_test_teardown)


load_init_configs(ACTION_IDENTIFIER, configholder)

ARCHIVE_TARGET = configholder.get_config_value("ARCHIVE_TARGET")
MODEL_TARGET = configholder.get_config_value("MODEL_TARGET")
