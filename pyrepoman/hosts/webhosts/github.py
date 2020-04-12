# Standard Library Imports

# Third Party Imports
import requests

# Local Application Imports
from .webhost import WebHost


class GitHub(WebHost):

    HELP_DESC = "a popular web hosting for git repos"

    def __init__(self, configholder):

        super().__init__(configholder)
        self.payload = configholder.get_config_value("repo_type")
        self.repo_owner_type = configholder.get_config_value("repo_owner_type")
        self.username = configholder.get_config_value("username")

    @classmethod
    def is_host_type(cls, identifier):

        return identifier == cls.__name__.lower()

    @classmethod
    def _modify_parser(cls, parser):

        repo_types_own = ["all", "public", "private"]
        default_own = "all"
        repo_types_other = ["all", "owner", "member"]
        default_other = "owner"

        subparser_github_container = parser.add_subparsers(
            title="available repo-owner-types",
            metavar="repo-owner-type [options ...]",
            dest="repo_owner_type",
        )
        subparser_github_container.required = True

        own = subparser_github_container.add_parser(
            "own", help="interact with your own git repo(s)", allow_abbrev=False
        )
        own.add_argument(
            "--repo-type",
            metavar="TYPE",
            default=default_own,
            choices=repo_types_own,
            help=f"specifies the type of repos to work on, choices are (default: {default_own}): "
            + ", ".join(repo_types_own),
        )

        other = subparser_github_container.add_parser(
            "other",
            help="interact with another user's public git repo(s)",
            allow_abbrev=False,
        )
        other.add_argument(
            "username", help="name of user whos repos you wish to interact with"
        )
        other.add_argument(
            "--repo-type",
            metavar="TYPE",
            default=default_other,
            choices=repo_types_other,
            help=f"specifies the type of repos to work on, choices are (default: {default_other}): "
            + ", ".join(repo_types_other),
        )

        return parser

    def _get_user_repo_names_and_locations(self):

        """ CURRENTLY FUNCS WILL USE GITHUB's REST API v3"""
        url = (
            "https://api.github.com/user/repos"
            if self.repo_owner_type == "own"
            else f"https://api.github.com/users/{self.username}/repos"
        )
        try:
            auth = (
                GitHubAuth(getattr(self, "api_token"))
                if self.repo_owner_type == "own"
                else None
            )
            repos = requests.get(url, auth=auth, params={"type": self.payload})
            repos.raise_for_status()
            for repo in repos.json():
                self.add_repo_name_and_location(repo["name"], repo["svn_url"])
            return self.repo_names_and_locations
        except AttributeError:
            print(
                f"Error: no api token exists in the configuration file for {type(self).__name__.lower()}"
            )
            raise SystemExit()
        except (requests.exceptions.ConnectionError):
            print(
                "Error: could not connect to GitHub, check network settings or try again later"
            )
            raise SystemExit()
        except requests.HTTPError:
            print(
                f"Error: communicating with GitHub failed; Reason: {repos.json()['message']}"
            )
            raise SystemExit()


class GitHubAuth(requests.auth.AuthBase):
    def __init__(self, api_token):

        self.api_token = api_token

    def __call__(self, requests_obj):

        requests_obj.headers["Authorization"] = self.auth_header_value()
        return requests_obj

    def auth_header_value(self):

        return f"token {self.api_token}"
