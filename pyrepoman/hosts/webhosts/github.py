# Standard Library Imports

# Third Party Imports
import requests

# Local Application Imports
from .webhost import WebHost

class GitHub(WebHost):

    def __init__(self, configholder):

        super().__init__()

    @classmethod
    def is_host_type(cls, identifier, configholder):

        if(identifier == cls.__name__.lower() and configholder.get_config_value("webhost")):
            return True

        return False

    def _get_repo_names_and_locations(self):

        """ CURRENTLY FUNCS WILL USE GITHUB's REST API v3"""

        repos = requests.get("https://api.github.com/user/repos", auth=(getattr(self, 'user'), getattr(self, 'api_token')), params=getattr(self, 'payload'))
        return {repo['name']:repo['svn_url'] for repo in repos.json()}
