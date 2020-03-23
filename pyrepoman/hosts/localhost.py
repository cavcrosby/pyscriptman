# Standard Library Imports
import os, subprocess, platform, pathlib

# Third Party Imports

# Local Application Imports
from .host import Host

class LocalHost(Host):

    def __init__(self, configholder):

        super().__init__()
        self.host = configholder.get_config_value('host')

    @classmethod
    def is_host_type(cls, identifier, configholder):

        if(pathlib.Path(identifier).exists() and configholder.get_config_value('local')):
            return True

        return False

    def get_repo_names_and_locations(self):

        def expand_user_on_host(intreperter_name, host_path):

            return subprocess.run([intreperter_name, '-c', f'import os; print(os.path.expanduser(\\"{host_path}\\"));"'], \
                            stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8').stdout.rstrip()

        INTREPERTER = 'python3'
        if(platform.system() != 'Linux'):
            INTREPERTER = 'python'
        #TODO CREATE CUSTOM EXCEPTION, INCASE CANNOT FIND PYTHON INTREPERTER
        host_path = expand_user_on_host(INTREPERTER, self.host)
        repos = self._get_pwd_all_repo_names(host_path)
        return {f"{repo}":os.path.join(host_path, repo) for repo in repos}
