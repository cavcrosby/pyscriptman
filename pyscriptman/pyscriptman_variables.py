"""These are variables that are specfic to the pyscriptman package."""
# Standard Library Imports
import os

# Third Party Imports

# Local Application Imports
from global_variables import ROOT_DIR, CONFIGS_PATH

CONFIGURATION_FILE_NAME = "pyscriptman_configs.toml"
CONFIGURATION_FILE_PATH = os.path.join(
    ROOT_DIR, os.path.join(CONFIGS_PATH, CONFIGURATION_FILE_NAME)
)
REQUIRE_SUBCOMMANDS = True
