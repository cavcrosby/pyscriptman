# Standard Library Imports
import os

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
from global_variables import (
    ROOT_DIR,
)
from util.helpers import (
    delete_folder_and_contents,
)

configholder = ConfigHolder(CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH)
configholder.load_toml()

ACTION_IDENTIFIER = "fetch"


@pytest.fixture(scope="function")
def normal_setup(request):
    configs = configholder.table_func_retrieve_additional_configs(
        ACTION_IDENTIFIER, request.function.__name__
    )
    load_configs(configholder, configs)
    FETCH_TARGET = configholder.get_config_value("FETCH_TARGET")
    MODEL_TARGET = configholder.get_config_value("MODEL_TARGET")
    os.mkdir(FETCH_TARGET)
    os.mkdir(MODEL_TARGET)

    def normal_teardown():
        os.chdir(ROOT_DIR)
        delete_folder_and_contents(FETCH_TARGET)
        delete_folder_and_contents(MODEL_TARGET)
        delete_configs(configholder, configs)

    request.addfinalizer(normal_teardown)

load_init_configs(ACTION_IDENTIFIER, configholder)

FETCH_TARGET = configholder.get_config_value("FETCH_TARGET")
MODEL_TARGET = configholder.get_config_value("MODEL_TARGET")