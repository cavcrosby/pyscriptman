# Standard Library Imports
import os, subprocess

# Third Party Imports

# Local Application Imports
from global_variables import ROOT_DIR, CONFIGS_PATH, UTIL_PATH

CONFIGURATION_FILE_NAME = "pyrepoman_configs.toml"
REMOTE_SCRIPT_GET_BARE_REPOS_NAME = "pyrepoman_get_brepos.py"
CONFIGURATION_FILE_PATH = os.path.join(
    ROOT_DIR, os.path.join(CONFIGS_PATH, CONFIGURATION_FILE_NAME)
)
REMOTE_SCRIPT_GET_BARE_REPOS_PATH = os.path.join(
    ROOT_DIR, os.path.join(UTIL_PATH, REMOTE_SCRIPT_GET_BARE_REPOS_NAME)
)
