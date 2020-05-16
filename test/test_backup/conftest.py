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

ACTION_IDENTIFIER = "backup"


@pytest.fixture(scope="function")
def integration_test_setup(request):
    configs = configholder.table_func_retrieve_additional_configs(
        ACTION_IDENTIFIER, request.function.__name__
    )
    load_configs(configholder, configs)
    os.mkdir(BACKUP_TARGET)
    os.mkdir(MODEL_TARGET)

    def normal_teardown():
        os.chdir(ROOT_DIR)
        shutil.rmtree(BACKUP_TARGET)
        shutil.rmtree(MODEL_TARGET)
        delete_configs(configholder, configs)

    request.addfinalizer(normal_teardown)


@pytest.fixture(scope="function")
def unit_test_setup(request):
    configs = configholder.table_func_retrieve_additional_configs(
        ACTION_IDENTIFIER, request.function.__name__
    )
    load_configs(configholder, configs)
    os.mkdir(BACKUP_TARGET)

    def unit_test_teardown():
        shutil.rmtree(BACKUP_TARGET)

    request.addfinalizer(unit_test_teardown)


load_init_configs(ACTION_IDENTIFIER, configholder)

BACKUP_TARGET = configholder.get_config_value("BACKUP_TARGET")
MODEL_TARGET = configholder.get_config_value("MODEL_TARGET")
