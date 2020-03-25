# Standard Library Imports
import os, subprocess

# Third Party Imports

# Local Application Imports
from .host import Host
from ..global_variables import REMOTE_SCRIPT_GET_BARE_REPOS_NAME, REMOTE_SCRIPT_GET_BARE_REPOS_PATH

class LanServer(Host):

    def __init__(self, configholder):

        super().__init__()
        self.host = configholder.get_config_value('host')
        self.host_path = configholder.get_config_value('host_path')

    @staticmethod
    def expand_user_on_host(host, host_path):

        return subprocess.run(['ssh', host, f'python3 -c "import os; print(os.path.expanduser(\\"{host_path}\\"));"'], \
                        stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip()

    @classmethod
    def is_host_type(cls, identifier, configholder):

        def can_reach_remote_repo(host_path):

            if(subprocess.run(['git', 'ls-remote', host_path], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8').stderr.rstrip() != ""):

                return False

            return True

        expanded_path = cls.expand_user_on_host(identifier, configholder.get_config_value('host_path'))
        if(can_reach_remote_repo(expanded_path)):
            return True

        return False

    def get_repo_names_and_locations(self):

        def copy_script_to_host(host, host_path, script):
            
            return subprocess.run(['scp', script, f"{host}:{host_path}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')

        def execute_script_on_host(host, script):

            return subprocess.run(['ssh', host, f"python3 {script}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')

        def remove_script_on_host(host, script):

            return subprocess.run(['ssh', host, f'python3 -c "import os; path = os.path.expanduser(\\"{script}\\"); os.remove(path)"'])

        HOST = self.host
        host_path = self.expand_user_on_host(HOST, self.host_path) # host_path really is endpoint path we are looking to manipulate repos from
        REMOTE_SCRIPT_HOST_PATH = f"{host_path}{REMOTE_SCRIPT_GET_BARE_REPOS_NAME}"
        copy_script_to_host(HOST, host_path, REMOTE_SCRIPT_GET_BARE_REPOS_NAME)
        repos = execute_script_on_host(HOST, REMOTE_SCRIPT_GET_BARE_REPOS_PATH)
        remove_script_on_host(HOST, REMOTE_SCRIPT_HOST_PATH)
        repos = repos.stdout.split(',') # e.g. 'repo1,repo1 - Copy\n'
        repos[-1] = repos[-1].strip()
        return {f"{repo}":f"{HOST}:{host_path}{repo}" for repo in repos}