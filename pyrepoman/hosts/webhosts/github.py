# Standard Library Imports

# Third Party Imports
import requests

# Local Application Imports
from .webhost import WebHost

class GitHub(WebHost):

    def __init__(self, configholder):

        super().__init__(configholder)
        self.payload = configholder.get_config_value('repo_type')

    @classmethod
    def is_host_type(cls, identifier, configholder):

        if(identifier == cls.__name__.lower()):
            return True

        return False

    def _get_repo_names_and_locations(self):

        """ CURRENTLY FUNCS WILL USE GITHUB's REST API v3"""

        repos = requests.get("https://api.github.com/user/repos", auth=(getattr(self, 'user'), getattr(self, 'api_token')), params={"type": self.payload})
        for repo in repos.json():
            self.add_repo_name_and_location(repo['name'], repo['svn_url'])
        return self.repo_names_and_locations
