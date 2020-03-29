# Standard Library Imports
import subprocess, os

# Third Party Imports

# Local Application Imports
from .action import Action

class Fetch(Action):

    def __init__(self, host):

        super().__init__()
        self.host = host

    def run(self):

        repo_names_and_urls = self.host.get_repo_names_and_locations()
        for repo_name in repo_names_and_urls:
            stderr = subprocess.run(['git', 'clone', f"{repo_names_and_urls[repo_name]}", f"{repo_name}"], stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8').stderr.rstrip()
            if(super()._permission_error(stderr)):
                raise OSError(13, 'Permission denied', os.getcwd())
