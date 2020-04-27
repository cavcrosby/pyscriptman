# Standard Library Imports
import os, sys

# Third Party Imports

# Local Application Imports

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UTIL_PATH = os.path.join(ROOT_DIR, "util")
CONFIGS_PATH = os.path.join(ROOT_DIR, "etc")

sys.path.insert(0, UTIL_PATH)
sys.path.insert(0, CONFIGS_PATH)
