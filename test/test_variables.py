# Standard Library Imports
import os, sys

# Third Party Imports

# Local Application Imports
from global_variables import (
    ROOT_DIR,
    CONFIGS_PATH,
)
from util.configholder import ConfigHolder

PYREPOMAN_MAIN_PATH = os.path.join(ROOT_DIR, "pyrepoman/__main__.py")
CONFIGURATION_FILE_NAME = "test_configs.toml"
CONFIGURATION_FILE_PATH = os.path.join(
    ROOT_DIR, os.path.join(CONFIGS_PATH, CONFIGURATION_FILE_NAME)
)

configholder = ConfigHolder(CONFIGURATION_FILE_NAME, CONFIGURATION_FILE_PATH)
configholder.load_toml()
