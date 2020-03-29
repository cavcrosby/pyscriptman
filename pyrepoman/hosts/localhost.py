# Standard Library Imports
import os, subprocess, platform, pathlib, sys

# Third Party Imports

# Local Application Imports
from .host import Host

class LocalHost(Host):

    def __init__(self, configholder):

        super().__init__()
        self.path = configholder.get_config_value('path')

    @classmethod
    def is_host_type(cls, identifier, configholder):

        path = configholder.get_config_value(identifier)
        expanded_path = os.path.expanduser(path)

        try:
            if(expanded_path != '' and pathlib.Path(expanded_path).exists()):
                return True

            return False
        except PermissionError:
            raise OSError(13, 'Permission denied', expanded_path)

    def get_repo_names_and_locations(self):

        local_path = os.path.expanduser(self.path)
        repos = self._get_pwd_bare_repo_names(local_path)
        return {f"{repo}":os.path.join(local_path, repo) for repo in repos}
