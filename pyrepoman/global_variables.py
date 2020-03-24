# Standard Library Imports
import os, subprocess

# Third Party Imports

# Local Application Imports

REPO_ROOT = subprocess.run(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip()
SCRIPTS_PATH = os.path.join(REPO_ROOT, 'scripts')
CONFIGS_PATH = os.path.join(REPO_ROOT, 'etc')
TOML_FILE_NAME = 'pyrepoman_configs.toml'
REMOTE_SCRIPT_GET_BARE_REPOS_NAME = 'pyrepoman_get_brepos.py'
TOML_FILE_PATH = os.path.join(REPO_ROOT, os.path.join(CONFIGS_PATH, TOML_FILE_NAME))
REMOTE_SCRIPT_GET_BARE_REPOS_PATH = os.path.join(REPO_ROOT, os.path.join(SCRIPTS_PATH, REMOTE_SCRIPT_GET_BARE_REPOS_NAME))