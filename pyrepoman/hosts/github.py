# Standard Library Imports
import requests

# Third Party Imports

# Local Application Imports
from .host import Host

class GitHub(Host):

    def __init__(self, configholder):

        super().__init__()
        self.user = configholder.get_config_value('user')
        self.api_token = configholder.get_config_value('api_token')
        self.payload = configholder.get_config_value('payload')

    @classmethod
    def is_host_type(cls, identifier, configholder):

        if(identifier == cls.__name__.lower() and configholder.get_config_value("webhost")):
            return True

        return False

    def get_repo_names_and_locations(self):

        """ CURRENTLY FUNCS WILL USE GITHUB's REST API v3"""

        repos = requests.get("https://api.github.com/user/repos", auth=(self.user, self.api_token), params=self.payload)
        return {repo['name']:repo['svn_url'] for repo in repos.json()}

#TODO SHOULD PULLING CONFIGURATIONS BE DONE HERE OR IN GENERATOR? DELEGATION!
# @classmethod
#     def get_additional_action_arguments(cls, host):

#         """ TASKS ARGUMENTS ARE BASED IN THE CONFIG.INI FILE """

#         config_app = configparser.ConfigParser()
#         config_app.read(f"config_{host}.ini")
#         return [item if item[1] != '' else -1 for item in config_app.items(cls.__name__)]