# Standard Library Imports

# Third Party Imports
import requests

# Local Application Imports


class GitHubAuth(requests.auth.AuthBase):
    def __init__(self, API_TOKEN):

        self.API_TOKEN = API_TOKEN

    def __call__(self, requests_obj):

        requests_obj.headers["Authorization"] = self.auth_header_value()
        return requests_obj

    def auth_header_value(self):

        return f"token {self.API_TOKEN}"
