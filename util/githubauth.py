"""Class module of GitHubAuth"""
# Standard Library Imports

# Third Party Imports
import requests

# Local Application Imports


class GitHubAuth(requests.auth.AuthBase):
    """Custom HTTPBasicAuth for github.com webhost.

    github.com does not require a username
    and password to use their API. Instead
    an API token is used.

    Parameters
    ----------
    API_TOKEN : str
        Taken from the pyscriptman_configs.toml file.

    """

    def __init__(self, API_TOKEN):

        self.API_TOKEN = API_TOKEN

    def __call__(self, requests_obj):

        requests_obj.headers["Authorization"] = self.auth_header_value()
        return requests_obj

    def auth_header_value(self):
        """Part of OAuth2 authenication.
        
        See the following link:
        https://developer.github.com/v3/#oauth2-token-sent-in-a-header

        """
        return f"token {self.API_TOKEN}"
