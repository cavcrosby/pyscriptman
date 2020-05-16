# Standard Library Imports
import os, shutil

# Third Party Imports
import pytest

# Local Application Imports
from util.configholder import ConfigHolder
from test.test_variables import (
    CONFIGURATION_FILE_NAME,
    CONFIGURATION_FILE_PATH,
)
from test.conftest import (
    load_configs,
    delete_configs,
    load_init_configs,
)
from global_variables import ROOT_DIR

configholder = ConfigHolder(CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH)
configholder.load_toml()

ACTION_IDENTIFIER = "fetch"


@pytest.fixture(scope="function")
def integration_test_setup(request):
    configs = configholder.table_func_retrieve_additional_configs(
        ACTION_IDENTIFIER, request.function.__name__
    )
    load_configs(configholder, configs)
    os.mkdir(FETCH_TARGET)
    os.mkdir(MODEL_TARGET)

    def normal_teardown():
        os.chdir(ROOT_DIR)
        shutil.rmtree(FETCH_TARGET)
        shutil.rmtree(MODEL_TARGET)
        delete_configs(configholder, configs)

    request.addfinalizer(normal_teardown)


@pytest.fixture(scope="function")
def unit_test_setup(request):
    configs = configholder.table_func_retrieve_additional_configs(
        ACTION_IDENTIFIER, request.function.__name__
    )
    load_configs(configholder, configs)
    os.mkdir(FETCH_TARGET)

    def unit_test_teardown():
        shutil.rmtree(FETCH_TARGET)

    request.addfinalizer(unit_test_teardown)


load_init_configs(ACTION_IDENTIFIER, configholder)

FETCH_TARGET = configholder.get_config_value("FETCH_TARGET")
MODEL_TARGET = configholder.get_config_value("MODEL_TARGET")
