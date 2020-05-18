# Standard Library Imports
import os
import sys

# Third Party Imports

# Local Application Imports

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UTIL_PATH = os.path.join(ROOT_DIR, "util")
CONFIGS_PATH = os.path.join(ROOT_DIR, "etc")

REMOTE_SCRIPT_GET_BARE_REPOS_NAME = "pyrepoman_get_bare_repos.py"
REMOTE_SCRIPT_GET_BARE_REPOS_PATH = os.path.join(
    ROOT_DIR, os.path.join(UTIL_PATH, REMOTE_SCRIPT_GET_BARE_REPOS_NAME)
)

sys.path.insert(0, UTIL_PATH)
sys.path.insert(0, CONFIGS_PATH)
