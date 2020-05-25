"""These are variables that are specfic to the pyrepoman package."""
# Standard Library Imports
import os

# Third Party Imports

# Local Application Imports
from global_variables import ROOT_DIR, CONFIGS_PATH

CONFIGURATION_FILE_NAME = "pyrepoman_configs.toml"
CONFIGURATION_FILE_PATH = os.path.join(
    ROOT_DIR, os.path.join(CONFIGS_PATH, CONFIGURATION_FILE_NAME)
)
